from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserPreferencesDTO:
    user_id: UUID
    price_weight: float
    rating_weight: float
    feedbacks_weight: float

    def normalized(self) -> "UserPreferencesDTO":
        total = self.price_weight + self.rating_weight + self.feedbacks_weight

        if total == 0:
            return UserPreferencesDTO(
                user_id=self.user_id,
                price_weight=0.5,
                rating_weight=0.25,
                feedbacks_weight=0.25,
            )

        return UserPreferencesDTO(
            user_id=self.user_id,
            price_weight=self.price_weight / total,
            rating_weight=self.rating_weight / total,
            feedbacks_weight=self.feedbacks_weight / total,
        )


DEFAULT_PREFERENCES = UserPreferencesDTO(
    user_id=UUID(int=0),
    price_weight=0.5,
    rating_weight=0.3,
    feedbacks_weight=0.2,
)
