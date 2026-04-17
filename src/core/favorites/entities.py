from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class FavoriteDTO:
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


@dataclass
class AddFavoriteDTO:
    product_id: str
    title: str
    brand: str
    price: float
    rating: float
    feedbacks: int
    seller: str
    marketplace: str
    url: str
