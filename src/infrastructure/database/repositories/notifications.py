from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.notifications.entities import CreateNotificationDTO, NotificationDTO
from infrastructure.database.models.notifications import NotificationModel


class NotificationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, dto: CreateNotificationDTO) -> NotificationDTO:
        model = NotificationModel(
            user_id=dto.user_id,
            subscription_id=dto.subscription_id,
            title=dto.title,
            message=dto.message,
            is_read=False,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_dto(model)

    async def get_by_user_id(self, user_id: UUID, unread_only: bool = False) -> list[NotificationDTO]:
        stmt = (
            select(NotificationModel)
            .where(NotificationModel.user_id == user_id)
            .order_by(NotificationModel.created_at.desc())
        )
        if unread_only:
            stmt = stmt.where(NotificationModel.is_read.is_(False))

        result = await self.session.execute(stmt)
        return [self._to_dto(m) for m in result.scalars().all()]

    async def mark_read(self, notification_id: UUID, user_id: UUID) -> NotificationDTO | None:
        stmt = (
            update(NotificationModel)
            .where(
                NotificationModel.id == notification_id,
                NotificationModel.user_id == user_id,
            )
            .values(is_read=True)
            .returning(NotificationModel)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_dto(model) if model else None

    async def mark_all_read(self, user_id: UUID) -> None:
        stmt = (
            update(NotificationModel)
            .where(
                NotificationModel.user_id == user_id,
                NotificationModel.is_read.is_(False),
            )
            .values(is_read=True)
        )
        await self.session.execute(stmt)

    @staticmethod
    def _to_dto(model: NotificationModel) -> NotificationDTO:
        return NotificationDTO(
            id=model.id,
            user_id=model.user_id,
            subscription_id=model.subscription_id,
            title=model.title,
            message=model.message,
            is_read=model.is_read,
            created_at=model.created_at,
        )