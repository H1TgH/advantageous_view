from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.feedbacks.schemas import CreateFeedbackSchema, FeedbackSchema, SellerReliabilitySchema
from core.feedbacks.entities import CreateFeedbackDTO
from core.feedbacks.exceptions import InvalidFeedbackDataException
from core.feedbacks.services import FeedbackService, get_feedback_service
from core.users.entities import AuthUserDTO
from dependencies import get_current_user


feedback_router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@feedback_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=FeedbackSchema,
)
async def create_feedback(
    data: CreateFeedbackSchema,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: FeedbackService = Depends(get_feedback_service),
) -> FeedbackSchema:
    try:
        dto = CreateFeedbackDTO(**data.model_dump())
        feedback = await service.create(current_user.id, dto)
        return FeedbackSchema(**vars(feedback))
    except InvalidFeedbackDataException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e


@feedback_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[FeedbackSchema],
)
async def get_my_feedbacks(
    current_user: AuthUserDTO = Depends(get_current_user),
    service: FeedbackService = Depends(get_feedback_service),
) -> list[FeedbackSchema]:
    feedbacks = await service.get_my_feedbacks(current_user.id)
    return [FeedbackSchema(**vars(f)) for f in feedbacks]


@feedback_router.get(
    "/seller-reliability",
    status_code=status.HTTP_200_OK,
    response_model=SellerReliabilitySchema,
)
async def get_seller_reliability(
    seller: str = Query(..., description="Имя продавца"),
    marketplace: str = Query(default="wb"),
    current_user: AuthUserDTO = Depends(get_current_user),
    service: FeedbackService = Depends(get_feedback_service),
) -> SellerReliabilitySchema:
    reliability = await service.get_seller_reliability(seller, marketplace)
    return SellerReliabilitySchema(**vars(reliability))
