from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.price_tracking.schemas import CreateSubscriptionSchema, PriceHistoryItemSchema, PriceSubscriptionSchema
from core.price_tracking.entities import CreateSubscriptionDTO
from core.price_tracking.exceptions import SubscriptionAlreadyExistsException, SubscriptionNotFoundException
from core.price_tracking.services import PriceTrackingService, get_price_tracking_service
from core.users.entities import AuthUserDTO
from dependencies import get_current_user


price_tracking_router = APIRouter(
    prefix="/price-tracking",
    tags=["Price Tracking"],
)


@price_tracking_router.post(
    "/subscriptions",
    status_code=status.HTTP_201_CREATED,
    response_model=PriceSubscriptionSchema,
)
async def subscribe(
    data: CreateSubscriptionSchema,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: PriceTrackingService = Depends(get_price_tracking_service),
) -> PriceSubscriptionSchema:
    try:
        dto = CreateSubscriptionDTO(**data.model_dump())
        subscription = await service.subscribe(current_user.id, dto)
        return PriceSubscriptionSchema(**vars(subscription))
    except SubscriptionAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e


@price_tracking_router.get(
    "/subscriptions",
    status_code=status.HTTP_200_OK,
    response_model=list[PriceSubscriptionSchema],
)
async def get_subscriptions(
    current_user: AuthUserDTO = Depends(get_current_user),
    service: PriceTrackingService = Depends(get_price_tracking_service),
) -> list[PriceSubscriptionSchema]:
    subscriptions = await service.get_subscriptions(current_user.id)
    return [PriceSubscriptionSchema(**vars(s)) for s in subscriptions]


@price_tracking_router.delete(
    "/subscriptions/{subscription_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unsubscribe(
    subscription_id: UUID,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: PriceTrackingService = Depends(get_price_tracking_service),
) -> None:
    try:
        await service.unsubscribe(current_user.id, subscription_id)
    except SubscriptionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@price_tracking_router.get(
    "/subscriptions/{subscription_id}/history",
    status_code=status.HTTP_200_OK,
    response_model=list[PriceHistoryItemSchema],
)
async def get_price_history(
    subscription_id: UUID,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: PriceTrackingService = Depends(get_price_tracking_service),
) -> list[PriceHistoryItemSchema]:
    try:
        history = await service.get_price_history(current_user.id, subscription_id)
        return [PriceHistoryItemSchema(**vars(h)) for h in history]
    except SubscriptionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
