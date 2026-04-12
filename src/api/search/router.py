from fastapi import APIRouter, Depends, status

from api.search.schemas import ProductSchema
from core.search.services import SearchService, get_search_service


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
    service: SearchService = Depends(get_search_service),
) -> list[ProductSchema]:
    products = await service.search(query)
    return [ProductSchema(**vars(p)) for p in products]
