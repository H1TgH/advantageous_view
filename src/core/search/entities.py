from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProductDTO:

    id: str

    title: str

    brand: Optional[str] = ""

    price: float = 0.0

    rating: float = 0.0

    feedbacks: int = 0

    seller: str = ""

    marketplace: str = ""

    url: str = ""

    score: Optional[float] = None

    delivery_days: Optional[int] = None

    delivery_price: Optional[int] = None

    delivery_free: Optional[bool] = None

    reliability: Optional[str] = None

    badges: list[str] = field(default_factory=list)