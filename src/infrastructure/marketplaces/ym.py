import logging
import re

import httpx

from core.search.entities import ProductDTO
from settings import settings


logger = logging.getLogger(__name__)


class YandexMarketClient:
    SEARCH_URL = "http://market.apisystem.name/search"
    MODELS_URL = "http://market.apisystem.name/models"

    def __init__(self) -> None:
        self._api_key = settings.apisystem_key
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0),
            headers={"Accept": "application/json"},
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def search(self, query: str, page: int = 1) -> list[ProductDTO]:
        if not self._api_key:
            logger.warning("YM: APISYSTEM_KEY not set, skipping")
            return []

        try:
            resp = await self._client.get(
                self.SEARCH_URL,
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
        except Exception as e:
            logger.warning("YM search failed: %s", e)
            return []

        if data.get("status") != "OK":
            return []

        offers = data.get("offers") or []
        return [self._map_offer(o) for o in offers]

    async def get_model_offers(self, model_id: str) -> list[ProductDTO]:
        if not self._api_key:
            logger.warning("YM: APISYSTEM_KEY not set, skipping")
            return []

        try:
            resp = await self._client.get(
                f"{self.MODELS_URL}/{model_id}/offers",
                params={
                    "format": "json",
                    "api_key": self._api_key,
                    "count": 30,
                    "sort": "aprice",
                },
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.warning("YM get_model_offers failed for model %s: %s", model_id, e)
            return []

        if data.get("status") != "OK":
            return []

        offers = data.get("offers") or []
        return [self._map_offer(o) for o in offers]

    @staticmethod
    def _parse_rating(raw: str | None) -> float:
        if not raw:
            return 0.0
        match = re.search(r"([\d.]+)", raw)
        return float(match.group(1)) if match else 0.0

    @staticmethod
    def _parse_feedbacks(raw: str | None) -> int:
        if not raw:
            return 0
        match = re.search(r"\(([\d.]+)K\)", raw.upper())
        if match:
            return int(float(match.group(1)) * 1000)
        match = re.search(r"([\d.]+)K", raw.upper())
        if match:
            return int(float(match.group(1)) * 1000)
        return 0

    @classmethod
    def _map_offer(cls, o: dict) -> ProductDTO:
        rating_raw = o.get("product_rating")
        return ProductDTO(
            id=str(o.get("market_sku") or o.get("offer_id") or ""),
            title=o.get("offer_name", ""),
            brand="",
            price=float(o.get("price") or 0),
            rating=cls._parse_rating(rating_raw),
            feedbacks=cls._parse_feedbacks(rating_raw),
            seller=o.get("shop_name") or o.get("business_name") or "",
            marketplace="ym",
            url=o.get("url") or "",
        )
