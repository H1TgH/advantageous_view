from pydantic import BaseModel


class ProductSchema(BaseModel):
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
    brand: str | None = ""
