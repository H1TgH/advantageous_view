from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class PriceSubscriptionDTO:
    id: UUID
    product_id: str
    title: str
    url: str
    marketplace: str
    target_price: float | None
    is_active: bool
    created_at: datetime


@dataclass
class PriceHistoryItemDTO:
    id: UUID
    subscription_id: UUID
    price: float
    created_at: datetime


@dataclass
class CreateSubscriptionDTO:
    product_id: str
    title: str
    url: str
    marketplace: str
    current_price: float
    target_price: float | None = field(default=None)
