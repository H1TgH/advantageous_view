import logging
from uuid import UUID

from core.preferences.entities import DEFAULT_PREFERENCES, UserPreferencesDTO
from core.preferences.services import UserPreferencesService
from core.search.entities import ProductDTO
from core.search.ranker import ProductRanker
from core.search_history.services import SearchHistoryService
from infrastructure.database.uow import UnitOfWork
from infrastructure.marketplaces.wb import WBClient


logger = logging.getLogger(__name__)


class SearchService:
    def __init__(
        self,
        wb_client: WBClient,
        preferences_service: UserPreferencesService,
        history_service: SearchHistoryService,
    ) -> None:
        self._wb = wb_client
        self._preferences_service = preferences_service
        self._history_service = history_service
        self._ranker = ProductRanker()

    async def search(self, query: str, user_id: UUID | None = None) -> list[ProductDTO]:
        try:
            products = await self._wb.search(query)
        except Exception as e:
            logger.warning("WB search failed: %s", e)
            return []

        preferences = await self._get_preferences(user_id)
        ranked = self._ranker.rank(products, preferences)

        if user_id:
            await self._history_service.add(user_id, query)

        return ranked

    async def _get_preferences(self, user_id: UUID | None) -> UserPreferencesDTO:
        if not user_id:
            return DEFAULT_PREFERENCES
        return await self._preferences_service.get(user_id)


def get_search_service() -> SearchService:
    return SearchService(
        wb_client=WBClient(),
        preferences_service=UserPreferencesService(UnitOfWork()),
        history_service=SearchHistoryService(UnitOfWork()),
    )
