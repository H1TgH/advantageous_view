from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateFeedbackSchema(BaseModel):
    product_id: str
    seller: str = ""
    marketplace: str = "wb"
    product_matched_description: bool | None = None
    delivery_on_time: bool | None = None
    overall_rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = None


class FeedbackSchema(BaseModel):
    id: UUID
    product_id: str
    seller: str
    marketplace: str
    product_matched_description: bool | None
    delivery_on_time: bool | None
    overall_rating: int | None
    comment: str | None
    created_at: datetime


class SellerReliabilitySchema(BaseModel):
    seller: str
    total_feedbacks: int
    description_match_rate: float
    delivery_accuracy_rate: float
    avg_overall_rating: float
