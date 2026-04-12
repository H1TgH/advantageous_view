from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.preferences.entities import UserPreferencesDTO
from infrastructure.database.models.preferences import UserPreferencesModel


class UserPreferencesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_user_id(self, user_id: UUID) -> UserPreferencesDTO | None:
        stmt = select(UserPreferencesModel).where(UserPreferencesModel.user_id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return UserPreferencesDTO(
            user_id=model.user_id,
            price_weight=model.price_weight,
            rating_weight=model.rating_weight,
            feedbacks_weight=model.feedbacks_weight,
        )

    async def upsert(self, dto: UserPreferencesDTO) -> None:
        stmt = select(UserPreferencesModel).where(UserPreferencesModel.user_id == dto.user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            model.price_weight = dto.price_weight
            model.rating_weight = dto.rating_weight
            model.feedbacks_weight = dto.feedbacks_weight
        else:
            self.session.add(UserPreferencesModel(
                user_id=dto.user_id,
                price_weight=dto.price_weight,
                rating_weight=dto.rating_weight,
                feedbacks_weight=dto.feedbacks_weight,
            ))
