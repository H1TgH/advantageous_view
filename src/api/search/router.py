from fastapi import APIRouter, Depends, status

from api.search.schemas import ProductSchema
from core.search.services import SearchService, get_search_service
from core.users.entities import AuthUserDTO
from core.users.services import UserService, get_user_service
from dependencies import get_current_user


search_router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@search_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProductSchema],
)
async def search(
    query: str,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: SearchService = Depends(get_search_service),
    user_service: UserService = Depends(get_user_service),
) -> list[ProductSchema]:
    products = await service.search(query, user_id=current_user.id)

    return [ProductSchema(**vars(p)) for p in products]
