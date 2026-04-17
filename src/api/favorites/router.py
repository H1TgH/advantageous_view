from fastapi import APIRouter, Depends, HTTPException, status

from api.favorites.schemas import AddFavoriteSchema, FavoriteSchema
from core.favorites.entities import AddFavoriteDTO
from core.favorites.exceptions import FavoriteAlreadyExistsException, FavoriteNotFoundException
from core.favorites.services import FavoriteService, get_favorite_service
from core.users.entities import AuthUserDTO
from dependencies import get_current_user


favorites_router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"],
)


@favorites_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=FavoriteSchema,
)
async def add_favorite(
    data: AddFavoriteSchema,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: FavoriteService = Depends(get_favorite_service),
) -> FavoriteSchema:
    try:
        dto = AddFavoriteDTO(**data.model_dump())
        favorite = await service.add(current_user.id, dto)
        return FavoriteSchema(**vars(favorite))
    except FavoriteAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e


@favorites_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[FavoriteSchema],
)
async def get_favorites(
    current_user: AuthUserDTO = Depends(get_current_user),
    service: FavoriteService = Depends(get_favorite_service),
) -> list[FavoriteSchema]:
    favorites = await service.get(current_user.id)
    return [FavoriteSchema(**vars(f)) for f in favorites]


@favorites_router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_favorite(
    product_id: str,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: FavoriteService = Depends(get_favorite_service),
) -> None:
    try:
        await service.remove(current_user.id, product_id)
    except FavoriteNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
