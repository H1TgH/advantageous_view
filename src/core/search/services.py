import asyncio
import logging
from uuid import UUID

from fastapi import Request

from core.preferences.entities import DEFAULT_PREFERENCES, UserPreferencesDTO
from core.preferences.services import UserPreferencesService
from core.search.entities import ProductDTO
from core.search.ranker import ProductRanker
from core.search_history.services import SearchHistoryService
from infrastructure.database.uow import UnitOfWork
from infrastructure.marketplaces.wb import WBClient
from infrastructure.marketplaces.ym import YandexMarketClient
from core.feedbacks.entities import SellerReliabilityDTO
from core.feedbacks.services import FeedbackService


logger = logging.getLogger(__name__)


class SearchService:
    def __init__(
        self,
        wb_client: WBClient,
        ym_client: YandexMarketClient,
        preferences_service: UserPreferencesService,
        history_service: SearchHistoryService,
        feedback_service: FeedbackService,
    ) -> None:
        self._wb = wb_client
        self._ym = ym_client
        self._preferences_service = preferences_service
        self._history_service = history_service
        self._ranker = ProductRanker()
        self._feedback_service = feedback_service

    async def search(self, query: str, user_id: UUID | None = None) -> list[ProductDTO]:
        wb_task = asyncio.create_task(
            self._safe_search(self._wb, query, "wb")
        )
        ym_task = asyncio.create_task(
            self._safe_search(self._ym, query, "ym")
        )

        wb_products, ym_products = await asyncio.gather(wb_task, ym_task)

        products = [*wb_products, *ym_products]

        if not products:
            return []

        preferences = await self._get_preferences(user_id)
        ranked = self._ranker.rank(products, preferences)
        await self._enrich_reliability(ranked)
        self._assign_badges(ranked)

        if user_id:
            await self._history_service.add(user_id, query)

        return ranked

    @staticmethod
    async def _safe_search(client, query: str, marketplace: str) -> list[ProductDTO]:
        try:
            return await client.search(query)
        except Exception as e:
            logger.warning("%s search failed: %s", marketplace, e)
            return []

    async def _get_preferences(self, user_id: UUID | None) -> UserPreferencesDTO:
        if not user_id:
            return DEFAULT_PREFERENCES
        return await self._preferences_service.get(user_id)

    async def _enrich_reliability(self, products: list[ProductDTO]) -> None:
        unique_sellers = list({(p.seller, p.marketplace) for p in products if p.seller})
        results = await asyncio.gather(
            *[self._feedback_service.get_seller_reliability(s, m) for s, m in unique_sellers]
        )
        reliability_map = {unique_sellers[i]: results[i] for i in range(len(unique_sellers))}
        for product in products:
            dto = reliability_map.get((product.seller, product.marketplace))
            if dto and dto.total_feedbacks > 0:
                product.reliability = self._reliability_label(dto)

    @staticmethod
    def _reliability_label(dto: SellerReliabilityDTO) -> str:
        if (
            dto.avg_overall_rating >= 4.5
            and dto.description_match_rate >= 0.8
            and dto.delivery_accuracy_rate >= 0.8
        ):
            return "Высокая"
        if (
            dto.avg_overall_rating >= 3.5
            or dto.description_match_rate >= 0.6
            or dto.delivery_accuracy_rate >= 0.6
        ):
            return "Средняя"
        return "Низкая"
    
    @staticmethod
    def _assign_badges(products: list[ProductDTO]) -> None:
        if not products:
            return

        for p in products:
            p.badges = []

        products[0].badges.append("Лучшее предложение")

        cheapest = min(products, key=lambda p: p.price + (p.delivery_price or 0))
        cheapest.badges.append("Самый дешёвый")

        with_delivery = [p for p in products if p.delivery_days is not None]
        if with_delivery:
            fastest = min(with_delivery, key=lambda p: p.delivery_days)
            fastest.badges.append("Быстрая доставка")

def get_search_service(request: Request) -> SearchService:
    return SearchService(
        wb_client=request.app.state.wb_client,
        ym_client=request.app.state.ym_client,
        preferences_service=UserPreferencesService(UnitOfWork()),
        history_service=SearchHistoryService(UnitOfWork()),
        feedback_service=FeedbackService(UnitOfWork()),
    )
