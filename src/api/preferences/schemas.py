from pydantic import BaseModel, Field


class UserPreferencesSchema(BaseModel):
    price_weight: float = Field(ge=0, le=1)
    rating_weight: float = Field(ge=0, le=1)
    feedbacks_weight: float = Field(ge=0, le=1)
    speed_weight: float = Field(ge=0, le=1, default=0.2)


class UserPreferencesResponseSchema(UserPreferencesSchema):
    pass
