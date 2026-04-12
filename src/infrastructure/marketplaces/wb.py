import asyncio
import random

import httpx

from core.search.entities import ProductDTO


class WBClient:
    BASE_URL = "https://search.wb.ru/exactmatch/ru/common/v18/search"

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(5.0),
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0",
                "Accept": "application/json,text/plain,*/*",
                "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
                "Origin": "https://www.wildberries.ru",
                "Referer": "https://www.wildberries.ru/",
            },
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def search(self, query: str, page: int = 1) -> list[ProductDTO]:
        params = {
            "appType": 1,
            "curr": "rub",
            "dest": -1257786,
            "lang": "ru",
            "page": page,
            "query": query,
            "resultset": "catalog",
            "sort": "popular",
            "spp": 30,
        }

        data = await self._request_with_retry(params)
        products = data.get("products", [])

        return [self._map_product(p) for p in products]

    async def _request_with_retry(self, params: dict, retries: int = 2) -> dict:
        last_exc: Exception | None = None

        for attempt in range(retries + 1):
            try:
                await asyncio.sleep(random.uniform(0.5, 1.5))

                resp = await self._client.get(self.BASE_URL, params=params)

                if resp.status_code in (429, 403, 307):
                    raise httpx.HTTPStatusError(
                        f"Blocked or throttled: {resp.status_code}",
                        request=resp.request,
                        response=resp,
                    )

                resp.raise_for_status()
                return resp.json()

            except Exception as e:
                last_exc = e
                await asyncio.sleep(0.5 * (2**attempt))

        raise RuntimeError(f"WB request failed after retries: {last_exc}")

    def _map_product(self, p: dict) -> ProductDTO:
        sizes = p.get("sizes") or []
        price = 0.0

        if sizes:
            price = sizes[0].get("price", {}).get("product", 0) / 100

        product_id = p.get("id", "")

        return ProductDTO(
            id=str(product_id),
            title=p.get("name", ""),
            brand=p.get("brand", ""),
            price=price,
            rating=float(p.get("rating") or 0),
            feedbacks=int(p.get("feedbacks") or 0),
            seller=p.get("supplier", ""),
            marketplace="wb",
            url=f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx",
        )
