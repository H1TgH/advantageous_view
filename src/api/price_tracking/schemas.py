from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateSubscriptionSchema(BaseModel):
    product_id: str
    title: str
    url: str
    marketplace: str = "wb"
    current_price: float
    target_price: float | None = None
    notify_in_app: bool = True
    notify_email: bool = False


class UpdateSubscriptionNotificationsSchema(BaseModel):
    notify_in_app: bool
    notify_email: bool


class PriceSubscriptionSchema(BaseModel):
    id: UUID
    product_id: str
    title: str
    url: str
    marketplace: str
    target_price: float | None
    is_active: bool
    notify_in_app: bool
    notify_email: bool
    created_at: datetime


class PriceHistoryItemSchema(BaseModel):
    id: UUID
    subscription_id: UUID
    price: float
    created_at: datetime