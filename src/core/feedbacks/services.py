from uuid import UUID

from core.feedbacks.entities import CreateFeedbackDTO, FeedbackDTO, SellerReliabilityDTO
from core.feedbacks.exceptions import InvalidFeedbackDataException
from infrastructure.database.repositories.feedbacks import FeedbackRepository
from infrastructure.database.uow import UnitOfWork


class FeedbackService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def create(self, user_id: UUID, dto: CreateFeedbackDTO) -> FeedbackDTO:
        self._validate(dto)
        async with self._uow() as session:
            repo = FeedbackRepository(session)
            return await repo.add(user_id, dto)

    async def get_my_feedbacks(self, user_id: UUID) -> list[FeedbackDTO]:
        async with self._uow() as session:
            repo = FeedbackRepository(session)
            return await repo.get_by_user_id(user_id)

    async def get_seller_reliability(self, seller: str, marketplace: str) -> SellerReliabilityDTO:
        async with self._uow() as session:
            repo = FeedbackRepository(session)
            return await repo.get_seller_reliability(seller, marketplace)

    @staticmethod
    def _validate(dto: CreateFeedbackDTO) -> None:
        if dto.overall_rating is not None and not (1 <= dto.overall_rating <= 5):
            raise InvalidFeedbackDataException("overall_rating must be between 1 and 5")
        all_none = (
            dto.product_matched_description is None
            and dto.delivery_on_time is None
            and dto.overall_rating is None
            and not dto.comment
        )
        if all_none:
            raise InvalidFeedbackDataException("Feedback must contain at least one non-empty field")


def get_feedback_service() -> FeedbackService:
    return FeedbackService(UnitOfWork())
