from fastapi import APIRouter, Depends, status

from api.search.schemas import ProductSchema
from core.search.services import SearchService, get_search_service
from core.users.entities import AuthUserDTO
from dependencies import get_optional_user


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
    current_user: AuthUserDTO | None = Depends(get_optional_user),
    service: SearchService = Depends(get_search_service),
) -> list[ProductSchema]:

    products = await service.search(
        query,
        user_id=current_user.id if current_user else None
    )

    return [
        ProductSchema(**vars(p))
        for p in products
    ]