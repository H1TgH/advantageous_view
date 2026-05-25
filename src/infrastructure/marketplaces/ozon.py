# src/infrastructure/marketplaces/ozon.py

import logging
import re
from datetime import date

import httpx
from dateutil import parser as date_parser

from core.search.entities import ProductDTO
from settings import settings


logger = logging.getLogger(__name__)


class OzonClient:

    SEARCH_URL = "http://ozon.apisystem.name/search"

    def __init__(self) -> None:

        self._api_key = settings.apisystem_key

        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(15.0),
            headers={
                "Accept": "application/json"
            }
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def search(
        self,
        query: str,
        page: int = 1
    ) -> list[ProductDTO]:

        if not self._api_key:
            logger.warning("OZON API KEY NOT FOUND")
            return []

        try:

            response = await self._client.get(
                self.SEARCH_URL,
                params={
                    "text": query,
                    "page": page,
                    "count": 30,
                    "format": "json",
                    "api_key": self._api_key,
                }
            )

            response.raise_for_status()

            data = response.json()

            logger.warning("OZON RESPONSE: %s", data)

        except Exception as e:
            logger.exception("OZON REQUEST ERROR: %s", e)
            return []

        if data.get("status") != "OK":
            logger.warning("OZON STATUS NOT OK")
            return []

        offers = data.get("offers") or []

        logger.warning("OZON OFFERS COUNT: %s", len(offers))

        return [self._map_offer(o) for o in offers]

    @staticmethod
    def _parse_rating(raw) -> float:

        if not raw:
            return 0.0

        match = re.search(r"([\d.]+)", str(raw))

        if match:
            return float(match.group(1))

        return 0.0

    @staticmethod
    def _parse_delivery_days(raw: str | None):

        if not raw:
            return None

        text = raw.lower().strip()

        if text == "сегодня":
            return 0

        if text == "завтра":
            return 1

        if text == "послезавтра":
            return 2

        match = re.search(r"(\d+)", text)

        if match:
            return int(match.group(1))

        try:
            delivery_date = date_parser.parse(
                raw,
                dayfirst=True
            ).date()

            return max(
                (delivery_date - date.today()).days,
                0
            )

        except Exception:
            return None

    @classmethod
    def _map_offer(
        cls,
        o: dict
    ) -> ProductDTO:

        raw_delivery_price = o.get("delivery_cost")

        delivery_price = (
            int(raw_delivery_price)
            if raw_delivery_price is not None
            else 0
        )

        return ProductDTO(
            id=str(
                o.get("sku")
                or o.get("offer_id")
                or ""
            ),

            title=o.get("offer_name") or "",

            brand=o.get("brand") or "",

            price=float(
                o.get("price") or 0
            ),

            rating=cls._parse_rating(
                o.get("product_rating")
            ),

            feedbacks=int(
                o.get("reviews") or 0
            ),

            seller=o.get("shop_name") or "",

            marketplace="ozon",

            url=o.get("url") or "",

            delivery_days=cls._parse_delivery_days(
                o.get("delivery_time")
            ),

            delivery_price=delivery_price,

            delivery_free=delivery_price == 0,
        )