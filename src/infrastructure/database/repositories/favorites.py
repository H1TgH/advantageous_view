from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.favorites.entities import AddFavoriteDTO, FavoriteDTO
from infrastructure.database.models.favorites import FavoriteModel


class FavoriteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user_id: UUID, dto: AddFavoriteDTO) -> FavoriteDTO:
        model = FavoriteModel(
            user_id=user_id,
            product_id=dto.product_id,
            title=dto.title,
            brand=dto.brand,
            price=dto.price,
            rating=dto.rating,
            feedbacks=dto.feedbacks,
            seller=dto.seller,
            marketplace=dto.marketplace,
            url=dto.url,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_dto(model)

    async def get_by_user_id(self, user_id: UUID) -> list[FavoriteDTO]:
        stmt = (
            select(FavoriteModel)
            .where(FavoriteModel.user_id == user_id)
            .order_by(FavoriteModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return [self._to_dto(m) for m in result.scalars().all()]

    async def get_by_user_and_product(self, user_id: UUID, product_id: str) -> FavoriteDTO | None:
        stmt = select(FavoriteModel).where(
            FavoriteModel.user_id == user_id,
            FavoriteModel.product_id == product_id,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_dto(model) if model else None

    async def delete(self, user_id: UUID, product_id: str) -> None:
        stmt = delete(FavoriteModel).where(
            FavoriteModel.user_id == user_id,
            FavoriteModel.product_id == product_id,
        )
        await self.session.execute(stmt)

    @staticmethod
    def _to_dto(model: FavoriteModel) -> FavoriteDTO:
        return FavoriteDTO(
            id=model.id,
            product_id=model.product_id,
            title=model.title,
            brand=model.brand,
            price=model.price,
            rating=model.rating,
            feedbacks=model.feedbacks,
            seller=model.seller,
            marketplace=model.marketplace,
            url=model.url,
            created_at=model.created_at,
        )
