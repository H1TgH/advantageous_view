from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AddFavoriteSchema(BaseModel):
    product_id: str
    title: str
    brand: str = ""
    price: float
    rating: float = 0.0
    feedbacks: int = 0
    seller: str = ""
    marketplace: str = "wb"
    url: str


class FavoriteSchema(BaseModel):
    id: UUID
    product_id: str
    title: str
    brand: str
    price: float
    rating: float
    feedbacks: int
    seller: str
    marketplace: str
    url: str
    created_at: datetime
