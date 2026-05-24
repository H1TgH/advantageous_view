from dataclasses import dataclass


@dataclass
class ProductDTO:
    id: str
    title: str
    brand: str
    price: float
    rating: float
    feedbacks: int
    seller: str
    marketplace: str
    url: str
    score: float | None = None
    delivery_days: int | None = None
    delivery_price: int | None = None
    delivery_free: bool | None = None
    reliability: str | None = None
    badges: list[str] | None = None
