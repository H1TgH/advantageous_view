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
    notify_in_app: bool
    notify_email: bool
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
    notify_in_app: bool = True
    notify_email: bool = False


@dataclass
class UpdateSubscriptionNotificationsDTO:
    notify_in_app: bool
    notify_email: bool


@dataclass
class UpdateSubscriptionTargetDTO:
    target_price: float | None


@dataclass
class PriceCheckAlert:
    subscription_id: UUID
    user_id: UUID
    email: str
    new_price: float
    old_price: float
    title: str
    url: str
    reason: str
    notify_in_app: bool
    notify_email: bool
