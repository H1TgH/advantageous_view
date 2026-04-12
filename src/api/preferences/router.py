from fastapi import APIRouter, Depends, status

from api.preferences.schemas import UserPreferencesResponseSchema, UserPreferencesSchema
from core.preferences.entities import UserPreferencesDTO
from core.preferences.services import UserPreferencesService, get_preferences_service
from core.users.entities import AuthUserDTO
from dependencies import get_current_user


preferences_router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"],
)


@preferences_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserPreferencesResponseSchema,
)
async def get_preferences(
    current_user: AuthUserDTO = Depends(get_current_user),
    service: UserPreferencesService = Depends(get_preferences_service),
) -> UserPreferencesResponseSchema:
    prefs = await service.get(current_user.id)
    return UserPreferencesResponseSchema(
        price_weight=prefs.price_weight,
        rating_weight=prefs.rating_weight,
        feedbacks_weight=prefs.feedbacks_weight,
    )


@preferences_router.put(
    "/",
    status_code=status.HTTP_200_OK,
)
async def update_preferences(
    data: UserPreferencesSchema,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: UserPreferencesService = Depends(get_preferences_service),
) -> None:
    dto = UserPreferencesDTO(
        user_id=current_user.id,
        price_weight=data.price_weight,
        rating_weight=data.rating_weight,
        feedbacks_weight=data.feedbacks_weight,
    )
    await service.update(dto)
