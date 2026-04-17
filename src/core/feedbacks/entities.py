from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class FeedbackDTO:
    id: UUID
    user_id: UUID
    product_id: str
    seller: str
    marketplace: str
    product_matched_description: bool | None
    delivery_on_time: bool | None
    overall_rating: int | None
    comment: str | None
    created_at: datetime


@dataclass
class CreateFeedbackDTO:
    product_id: str
    seller: str
    marketplace: str
    product_matched_description: bool | None
    delivery_on_time: bool | None
    overall_rating: int | None
    comment: str | None


@dataclass
class SellerReliabilityDTO:
    seller: str
    total_feedbacks: int
    description_match_rate: float
    delivery_accuracy_rate: float
    avg_overall_rating: float
