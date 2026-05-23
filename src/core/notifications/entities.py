from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class NotificationDTO:
    id: UUID
    user_id: UUID
    subscription_id: UUID | None
    title: str
    message: str
    is_read: bool
    created_at: datetime


@dataclass
class CreateNotificationDTO:
    user_id: UUID
    subscription_id: UUID | None
    title: str
    message: str
