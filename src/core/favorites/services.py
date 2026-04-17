from uuid import UUID

from core.favorites.entities import AddFavoriteDTO, FavoriteDTO
from core.favorites.exceptions import FavoriteAlreadyExistsException, FavoriteNotFoundException
from infrastructure.database.repositories.favorites import FavoriteRepository
from infrastructure.database.uow import UnitOfWork


class FavoriteService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def add(self, user_id: UUID, dto: AddFavoriteDTO) -> FavoriteDTO:
        async with self._uow() as session:
            repo = FavoriteRepository(session)
            existing = await repo.get_by_user_and_product(user_id, dto.product_id)
            if existing:
                raise FavoriteAlreadyExistsException("Product already in favorites")
            return await repo.add(user_id, dto)

    async def get(self, user_id: UUID) -> list[FavoriteDTO]:
        async with self._uow() as session:
            repo = FavoriteRepository(session)
            return await repo.get_by_user_id(user_id)

    async def remove(self, user_id: UUID, product_id: str) -> None:
        async with self._uow() as session:
            repo = FavoriteRepository(session)
            existing = await repo.get_by_user_and_product(user_id, product_id)
            if not existing:
                raise FavoriteNotFoundException("Favorite not found")
            await repo.delete(user_id, product_id)


def get_favorite_service() -> FavoriteService:
    return FavoriteService(UnitOfWork())
