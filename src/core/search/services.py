import logging

from core.search.entities import ProductDTO
from infrastructure.marketplaces.wb import WBClient


logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, wb_client: WBClient) -> None:
        self._wb = wb_client

    async def search(self, query: str) -> list[ProductDTO]:
        try:
            return await self._wb.search(query)
        except Exception as e:
            logger.warning("WB search failed: %s", e)
            return []


def get_search_service() -> SearchService:
    return SearchService(wb_client=WBClient())
