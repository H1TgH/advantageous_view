from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserPreferencesDTO:
    user_id: UUID
    price_weight: float
    rating_weight: float
    feedbacks_weight: float
    speed_weight: float = 0.2

    def normalized(self) -> "UserPreferencesDTO":
        total = self.price_weight + self.rating_weight + self.feedbacks_weight + self.speed_weight

        if total == 0:
            return UserPreferencesDTO(
                user_id=self.user_id,
                price_weight=0.4,
                rating_weight=0.25,
                feedbacks_weight=0.15,
                speed_weight=0.2,
            )

        return UserPreferencesDTO(
            user_id=self.user_id,
            price_weight=self.price_weight / total,
            rating_weight=self.rating_weight / total,
            feedbacks_weight=self.feedbacks_weight / total,
            speed_weight=self.speed_weight / total,
        )


DEFAULT_PREFERENCES = UserPreferencesDTO(
    user_id=UUID(int=0),
    price_weight=0.4,
    rating_weight=0.25,
    feedbacks_weight=0.15,
    speed_weight=0.2,
)
