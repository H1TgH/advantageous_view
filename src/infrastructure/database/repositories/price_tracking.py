from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.price_tracking.entities import CreateSubscriptionDTO, PriceHistoryItemDTO, PriceSubscriptionDTO
from infrastructure.database.models.price_tracking import PriceHistoryModel, PriceSubscriptionModel


class PriceTrackingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_subscription(self, user_id: UUID, dto: CreateSubscriptionDTO) -> PriceSubscriptionDTO:
        model = PriceSubscriptionModel(
            user_id=user_id,
            product_id=dto.product_id,
            title=dto.title,
            url=dto.url,
            marketplace=dto.marketplace,
            target_price=dto.target_price,
            is_active=True,
        )
        self.session.add(model)
        await self.session.flush()
        return self._sub_to_dto(model)

    async def add_price_history(self, subscription_id: UUID, price: float) -> PriceHistoryItemDTO:
        model = PriceHistoryModel(subscription_id=subscription_id, price=price)
        self.session.add(model)
        await self.session.flush()
        return self._hist_to_dto(model)

    async def get_subscriptions_by_user_id(self, user_id: UUID) -> list[PriceSubscriptionDTO]:
        stmt = (
            select(PriceSubscriptionModel)
            .where(PriceSubscriptionModel.user_id == user_id)
            .order_by(PriceSubscriptionModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return [self._sub_to_dto(m) for m in result.scalars().all()]

    async def get_subscription_by_user_and_product(self, user_id: UUID, product_id: str) -> PriceSubscriptionDTO | None:
        stmt = select(PriceSubscriptionModel).where(
            PriceSubscriptionModel.user_id == user_id,
            PriceSubscriptionModel.product_id == product_id,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._sub_to_dto(model) if model else None

    async def get_subscription_by_id_and_user(
        self,
        subscription_id: UUID,
        user_id: UUID
    ) -> PriceSubscriptionDTO | None:
        stmt = select(PriceSubscriptionModel).where(
            PriceSubscriptionModel.id == subscription_id,
            PriceSubscriptionModel.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._sub_to_dto(model) if model else None

    async def delete_subscription(self, subscription_id: UUID) -> None:
        stmt = delete(PriceSubscriptionModel).where(PriceSubscriptionModel.id == subscription_id)
        await self.session.execute(stmt)

    async def get_price_history(self, subscription_id: UUID) -> list[PriceHistoryItemDTO]:
        stmt = (
            select(PriceHistoryModel)
            .where(PriceHistoryModel.subscription_id == subscription_id)
            .order_by(PriceHistoryModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return [self._hist_to_dto(m) for m in result.scalars().all()]

    @staticmethod
    def _sub_to_dto(model: PriceSubscriptionModel) -> PriceSubscriptionDTO:
        return PriceSubscriptionDTO(
            id=model.id,
            product_id=model.product_id,
            title=model.title,
            url=model.url,
            marketplace=model.marketplace,
            target_price=model.target_price,
            is_active=model.is_active,
            created_at=model.created_at,
        )

    @staticmethod
    def _hist_to_dto(model: PriceHistoryModel) -> PriceHistoryItemDTO:
        return PriceHistoryItemDTO(
            id=model.id,
            subscription_id=model.subscription_id,
            price=model.price,
            created_at=model.created_at,
        )
