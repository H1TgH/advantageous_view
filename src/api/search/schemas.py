from pydantic import BaseModel, Field, computed_field


class ProductSchema(BaseModel):
    id: str
    title: str
    brand: str = ""
    price: float
    rating: float
    feedbacks: int
    seller: str
    marketplace: str
    url: str
    score: float | None = Field(default=None, ge=0, le=100)
    delivery_days: int | None = None
    delivery_price: int | None = None
    delivery_free: bool | None = None
    reliability: str | None = None
    @computed_field
    @property
    def total_price(self) -> float:
        return self.price + (self.delivery_price or 0)
