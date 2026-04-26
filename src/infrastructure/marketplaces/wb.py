
import httpx

from core.search.entities import ProductDTO
from settings import settings


class WBClient:
    BASE_URL = "http://wb.apisystem.name/search"

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0),
        )
        self._api_key = settings.apisystem_key

    async def search(self, query: str, page: int = 1) -> list[ProductDTO]:
        resp = await self._client.get(
            self.BASE_URL,
            params={
                "text": query,
                "page": page,
                "count": 30,
                "format": "json",
                "api_key": self._api_key,
            },
        )

        resp.raise_for_status()
        data = resp.json()

        offers = data.get("offers") or []
        return [self._map_offer(o) for o in offers]

    def _map_offer(self, o: dict) -> ProductDTO:
        return ProductDTO(
            id=str(o.get("model_id") or o.get("offer_id")),
            title=o.get("offer_name", ""),
            brand=o.get("brand", ""),
            price=float(o.get("price") or 0),
            rating=float(o.get("product_rating") or 0),
            feedbacks=int(o.get("reviews") or 0),
            seller=o.get("shop_name") or "",
            marketplace="wb",
            url=o.get("url") or "",
        )
