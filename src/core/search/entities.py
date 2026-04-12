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
