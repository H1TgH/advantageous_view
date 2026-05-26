from uuid import UUID

from core.notifications.entities import NotificationDTO
from core.notifications.exceptions import NotificationNotFoundException
from infrastructure.database.repositories.notifications import NotificationRepository
from infrastructure.database.uow import UnitOfWork


class NotificationService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_list(self, user_id: UUID, unread_only: bool = False) -> list[NotificationDTO]:
        async with self._uow() as session:
            repo = NotificationRepository(session)
            return await repo.get_by_user_id(user_id, unread_only=unread_only)

    async def mark_read(self, user_id: UUID, notification_id: UUID) -> NotificationDTO:
        async with self._uow() as session:
            repo = NotificationRepository(session)
            notification = await repo.mark_read(notification_id, user_id)
            if not notification:
                raise NotificationNotFoundException("Notification not found")
            return notification

    async def mark_all_read(self, user_id: UUID) -> None:
        async with self._uow() as session:
            repo = NotificationRepository(session)
            await repo.mark_all_read(user_id)


def get_notification_service() -> NotificationService:
    return NotificationService(UnitOfWork())