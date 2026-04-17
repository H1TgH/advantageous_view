from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.feedbacks.entities import CreateFeedbackDTO, FeedbackDTO, SellerReliabilityDTO
from infrastructure.database.models.feedbacks import FeedbackModel


class FeedbackRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user_id: UUID, dto: CreateFeedbackDTO) -> FeedbackDTO:
        model = FeedbackModel(
            user_id=user_id,
            product_id=dto.product_id,
            seller=dto.seller,
            marketplace=dto.marketplace,
            product_matched_description=dto.product_matched_description,
            delivery_on_time=dto.delivery_on_time,
            overall_rating=dto.overall_rating,
            comment=dto.comment,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_dto(model)

    async def get_by_user_id(self, user_id: UUID, limit: int = 50) -> list[FeedbackDTO]:
        stmt = (
            select(FeedbackModel)
            .where(FeedbackModel.user_id == user_id)
            .order_by(FeedbackModel.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return [self._to_dto(m) for m in result.scalars().all()]

    async def get_seller_reliability(self, seller: str, marketplace: str) -> SellerReliabilityDTO:
        stmt = select(FeedbackModel).where(
            FeedbackModel.seller == seller,
            FeedbackModel.marketplace == marketplace,
        )
        result = await self.session.execute(stmt)
        feedbacks = result.scalars().all()

        total = len(feedbacks)
        if total == 0:
            return SellerReliabilityDTO(
                seller=seller,
                total_feedbacks=0,
                description_match_rate=0.0,
                delivery_accuracy_rate=0.0,
                avg_overall_rating=0.0,
            )

        desc_votes = [f.product_matched_description for f in feedbacks if f.product_matched_description is not None]
        delivery_votes = [f.delivery_on_time for f in feedbacks if f.delivery_on_time is not None]
        ratings = [f.overall_rating for f in feedbacks if f.overall_rating is not None]

        return SellerReliabilityDTO(
            seller=seller,
            total_feedbacks=total,
            description_match_rate=sum(desc_votes) / len(desc_votes) if desc_votes else 0.0,
            delivery_accuracy_rate=sum(delivery_votes) / len(delivery_votes) if delivery_votes else 0.0,
            avg_overall_rating=sum(ratings) / len(ratings) if ratings else 0.0,
        )

    @staticmethod
    def _to_dto(model: FeedbackModel) -> FeedbackDTO:
        return FeedbackDTO(
            id=model.id,
            user_id=model.user_id,
            product_id=model.product_id,
            seller=model.seller,
            marketplace=model.marketplace,
            product_matched_description=model.product_matched_description,
            delivery_on_time=model.delivery_on_time,
            overall_rating=model.overall_rating,
            comment=model.comment,
            created_at=model.created_at,
        )
