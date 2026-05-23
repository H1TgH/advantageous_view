from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.notifications.schemas import NotificationSchema
from core.notifications.exceptions import NotificationNotFoundException
from core.notifications.services import NotificationService, get_notification_service
from core.users.entities import AuthUserDTO
from dependencies import get_current_user


notifications_router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@notifications_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[NotificationSchema],
)
async def get_notifications(
    unread_only: bool = Query(default=False),
    current_user: AuthUserDTO = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> list[NotificationSchema]:
    notifications = await service.get_list(current_user.id, unread_only=unread_only)
    return [NotificationSchema(**vars(n)) for n in notifications]


@notifications_router.patch(
    "/{notification_id}/read",
    status_code=status.HTTP_200_OK,
    response_model=NotificationSchema,
)
async def mark_notification_read(
    notification_id: UUID,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> NotificationSchema:
    try:
        notification = await service.mark_read(current_user.id, notification_id)
        return NotificationSchema(**vars(notification))
    except NotificationNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@notifications_router.post(
    "/read-all",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def mark_all_notifications_read(
    current_user: AuthUserDTO = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> None:
    await service.mark_all_read(current_user.id)
