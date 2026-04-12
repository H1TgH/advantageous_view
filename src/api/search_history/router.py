from fastapi import APIRouter, Depends, status

from api.search_history.schemas import SearchHistoryItemSchema
from core.search_history.services import SearchHistoryService, get_search_history_service
from core.users.entities import AuthUserDTO
from dependencies import get_current_user


search_history_router = APIRouter(
    prefix="/search-history",
    tags=["Search History"],
)


@search_history_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[SearchHistoryItemSchema],
)
async def get_search_history(
    current_user: AuthUserDTO = Depends(get_current_user),
    service: SearchHistoryService = Depends(get_search_history_service),
) -> list[SearchHistoryItemSchema]:
    items = await service.get(current_user.id)
    return [
        SearchHistoryItemSchema(
            id=item.id,
            query=item.query,
            created_at=item.created_at,
        )
        for item in items
    ]


@search_history_router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_search_history(
    current_user: AuthUserDTO = Depends(get_current_user),
    service: SearchHistoryService = Depends(get_search_history_service),
) -> None:
    await service.clear(current_user.id)
