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


class PriceSubscriptionSchema(BaseModel):
    id: UUID
    product_id: str
    title: str
    url: str
    marketplace: str
    target_price: float | None
    is_active: bool
    created_at: datetime


class PriceHistoryItemSchema(BaseModel):
    id: UUID
    subscription_id: UUID
    price: float
    created_at: datetime
