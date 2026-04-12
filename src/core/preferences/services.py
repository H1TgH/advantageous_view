from uuid import UUID

from core.preferences.entities import DEFAULT_PREFERENCES, UserPreferencesDTO
from infrastructure.database.repositories.preferences import UserPreferencesRepository
from infrastructure.database.uow import UnitOfWork


class UserPreferencesService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get(self, user_id: UUID) -> UserPreferencesDTO:
        async with self._uow() as session:
            repo = UserPreferencesRepository(session)
            prefs = await repo.get_by_user_id(user_id)
            return prefs or DEFAULT_PREFERENCES

    async def update(self, dto: UserPreferencesDTO) -> None:
        prefs = dto.normalized()
        async with self._uow() as session:
            repo = UserPreferencesRepository(session)
            await repo.upsert(prefs)


def get_preferences_service() -> UserPreferencesService:
    return UserPreferencesService(UnitOfWork())
