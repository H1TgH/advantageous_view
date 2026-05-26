from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NotificationSchema(BaseModel):
    id: UUID
    subscription_id: UUID | None
    title: str
    message: str
    is_read: bool
    created_at: datetime