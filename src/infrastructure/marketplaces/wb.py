import logging
import re
from datetime import date

import httpx
from dateutil import parser as date_parser

from core.search.entities import ProductDTO
from settings import settings


logger = logging.getLogger(__name__)


class WBClient:
    BASE_URL = "http://wb.apisystem.name/search"
    MODELS_URL = "http://wb.apisystem.name/models"

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))
        self._api_key = settings.apisystem_key

    async def close(self) -> None:
        await self._client.aclose()

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
        logger.warning("WB raw response keys: %s, status: %s, offers count: %s",
                    list(data.keys()), data.get("status"), len(data.get("offers") or []))
        if data.get("status") != "OK":
            logger.warning("WB returned non-OK status: %s", data.get("status"))
            return []
        offers = data.get("offers") or []
        return [self._map_offer(o) for o in offers]

    async def get_model_offers(self, model_id: str) -> list[ProductDTO]:
        resp = await self._client.get(
            f"{self.MODELS_URL}/{model_id}/offers",
            params={
                "format": "json",
                "api_key": self._api_key,
                "count": 30,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        logger.debug("WB raw response: %s", data)

        if data.get("status") != "OK":
            return []

        offers = data.get("offers") or []
        return [self._map_offer(o) for o in offers]

    @staticmethod
    def _parse_delivery_days(raw: str | None) -> int | None:
        if not raw:
            return None

        text = raw.strip().lower()

        if text == "сегодня":
            return 0
        if text == "завтра":
            return 1
        if text == "послезавтра":
            return 2

        match = re.search(r"(\d+)\s*[-–—]?\s*(\d+)?\s*дн", text)
        if match:
            return int(match.group(1))

        match = re.search(r"(\d+)\s*дн", text)
        if match:
            return int(match.group(1))

        try:
            delivery_date = date_parser.parse(raw, dayfirst=True).date()
            return max((delivery_date - date.today()).days, 0)
        except (ValueError, TypeError, OverflowError):
            return None

    @classmethod
    def _map_offer(cls, o: dict) -> ProductDTO:
        raw_delivery_price = o.get("delivery_cost")
        delivery_price = int(raw_delivery_price) if raw_delivery_price is not None else None
        delivery_free = delivery_price == 0 if delivery_price is not None else None

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
            delivery_days=cls._parse_delivery_days(o.get("delivery_time")),
            delivery_price=delivery_price,
            delivery_free=delivery_free,
        )
