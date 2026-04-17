from uuid import UUID

from core.price_tracking.entities import CreateSubscriptionDTO, PriceHistoryItemDTO, PriceSubscriptionDTO
from core.price_tracking.exceptions import SubscriptionAlreadyExistsException, SubscriptionNotFoundException
from infrastructure.database.repositories.price_tracking import PriceTrackingRepository
from infrastructure.database.uow import UnitOfWork


class PriceTrackingService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def subscribe(self, user_id: UUID, dto: CreateSubscriptionDTO) -> PriceSubscriptionDTO:
        async with self._uow() as session:
            repo = PriceTrackingRepository(session)
            existing = await repo.get_subscription_by_user_and_product(user_id, dto.product_id)
            if existing:
                raise SubscriptionAlreadyExistsException("Already subscribed to this product")
            subscription = await repo.add_subscription(user_id, dto)
            await repo.add_price_history(subscription.id, dto.current_price)
            return subscription

    async def get_subscriptions(self, user_id: UUID) -> list[PriceSubscriptionDTO]:
        async with self._uow() as session:
            repo = PriceTrackingRepository(session)
            return await repo.get_subscriptions_by_user_id(user_id)

    async def unsubscribe(self, user_id: UUID, subscription_id: UUID) -> None:
        async with self._uow() as session:
            repo = PriceTrackingRepository(session)
            subscription = await repo.get_subscription_by_id_and_user(subscription_id, user_id)
            if not subscription:
                raise SubscriptionNotFoundException("Subscription not found")
            await repo.delete_subscription(subscription_id)

    async def get_price_history(self, user_id: UUID, subscription_id: UUID) -> list[PriceHistoryItemDTO]:
        async with self._uow() as session:
            repo = PriceTrackingRepository(session)
            subscription = await repo.get_subscription_by_id_and_user(subscription_id, user_id)
            if not subscription:
                raise SubscriptionNotFoundException("Subscription not found")
            return await repo.get_price_history(subscription_id)


def get_price_tracking_service() -> PriceTrackingService:
    return PriceTrackingService(UnitOfWork())
