from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.search_history.entities import SearchHistoryItemDTO
from infrastructure.database.models.search_history import SearchHistoryModel


class SearchHistoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user_id: UUID, query: str) -> None:
        self.session.add(SearchHistoryModel(user_id=user_id, query=query))

    async def get_by_user_id(self, user_id: UUID, limit: int = 20) -> list[SearchHistoryItemDTO]:
        stmt = (
            select(SearchHistoryModel)
            .where(SearchHistoryModel.user_id == user_id)
            .order_by(SearchHistoryModel.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [
            SearchHistoryItemDTO(
                id=m.id,
                query=m.query,
                created_at=m.created_at,
            )
            for m in models
        ]

    async def clear(self, user_id: UUID) -> None:
        stmt = delete(SearchHistoryModel).where(SearchHistoryModel.user_id == user_id)
        await self.session.execute(stmt)


    async def delete_by_id(self, item_id: UUID, user_id: UUID) -> bool:
        stmt = select(SearchHistoryModel).where(
            SearchHistoryModel.id == item_id,
            SearchHistoryModel.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return False
        await self.session.delete(model)
        return True
