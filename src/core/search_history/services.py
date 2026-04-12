from uuid import UUID

from core.search_history.entities import SearchHistoryItemDTO
from infrastructure.database.repositories.search_history import SearchHistoryRepository
from infrastructure.database.uow import UnitOfWork


class SearchHistoryService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def add(self, user_id: UUID, query: str) -> None:
        async with self._uow() as session:
            repo = SearchHistoryRepository(session)
            await repo.add(user_id, query)

    async def get(self, user_id: UUID, limit: int = 20) -> list[SearchHistoryItemDTO]:
        async with self._uow() as session:
            repo = SearchHistoryRepository(session)
            return await repo.get_by_user_id(user_id, limit)

    async def clear(self, user_id: UUID) -> None:
        async with self._uow() as session:
            repo = SearchHistoryRepository(session)
            await repo.clear(user_id)


def get_search_history_service() -> SearchHistoryService:
    return SearchHistoryService(UnitOfWork())
