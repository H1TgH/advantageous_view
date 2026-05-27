from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.users.entities import UserNotificationSettingsDTO
from infrastructure.database.models.user_notification_settings import UserNotificationSettingsModel


class UserNotificationSettingsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_user_id(self, user_id: UUID) -> UserNotificationSettingsDTO | None:
        stmt = select(UserNotificationSettingsModel).where(UserNotificationSettingsModel.user_id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._to_dto(model)

    async def upsert(self, dto: UserNotificationSettingsDTO) -> UserNotificationSettingsDTO:
        stmt = select(UserNotificationSettingsModel).where(UserNotificationSettingsModel.user_id == dto.user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.notifications_enabled = dto.notifications_enabled
            model.subscription_price_changes = dto.subscription_price_changes
            model.subscription_new_features = dto.subscription_new_features
            model.notify_in_app = dto.notify_in_app
            model.notify_email = dto.notify_email
        else:
            model = UserNotificationSettingsModel(
                user_id=dto.user_id,
                notifications_enabled=dto.notifications_enabled,
                subscription_price_changes=dto.subscription_price_changes,
                subscription_new_features=dto.subscription_new_features,
                notify_in_app=dto.notify_in_app,
                notify_email=dto.notify_email,
            )
            self.session.add(model)
        await self.session.flush()
        return self._to_dto(model)

    @staticmethod
    def _to_dto(model: UserNotificationSettingsModel) -> UserNotificationSettingsDTO:
        return UserNotificationSettingsDTO(
            user_id=model.user_id,
            notifications_enabled=model.notifications_enabled,
            subscription_price_changes=model.subscription_price_changes,
            subscription_new_features=model.subscription_new_features,
            notify_in_app=model.notify_in_app,
            notify_email=model.notify_email,
        )
