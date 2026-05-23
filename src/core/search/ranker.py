import math

from core.preferences.entities import UserPreferencesDTO
from core.search.entities import ProductDTO


class ProductRanker:
    _SCALE = 100.0

    def rank(self, products: list[ProductDTO], preferences: UserPreferencesDTO) -> list[ProductDTO]:
        if not products:
            return []

        prefs = preferences.normalized()

        total_costs = [self._total_cost(p) for p in products if p.price > 0]
        ratings = [p.rating for p in products]
        feedbacks_log = [math.log1p(p.feedbacks) for p in products]
        delivery_days = [p.delivery_days for p in products if p.delivery_days is not None]

        min_cost, max_cost = (min(total_costs), max(total_costs)) if total_costs else (0, 1)
        min_rating, max_rating = (min(ratings), max(ratings)) if ratings else (0, 1)
        min_feedbacks, max_feedbacks = (min(feedbacks_log), max(feedbacks_log)) if feedbacks_log else (0, 1)
        min_delivery, max_delivery = (min(delivery_days), max(delivery_days)) if delivery_days else (0, 1)

        for product in products:
            product.score = self._score(
                product,
                prefs,
                min_cost,
                max_cost,
                min_rating,
                max_rating,
                min_feedbacks,
                max_feedbacks,
                min_delivery,
                max_delivery,
            )

        return sorted(products, key=lambda p: p.score or 0, reverse=True)

    def _score(
        self,
        product: ProductDTO,
        prefs: UserPreferencesDTO,
        min_cost: float,
        max_cost: float,
        min_rating: float,
        max_rating: float,
        min_feedbacks: float,
        max_feedbacks: float,
        min_delivery: float,
        max_delivery: float,
    ) -> float:
        if product.price > 0:
            price_score = self._normalize_inverted(self._total_cost(product), min_cost, max_cost)
        else:
            price_score = 0.0

        rating_score = self._normalize(product.rating, min_rating, max_rating)
        feedbacks_score = self._normalize(math.log1p(product.feedbacks), min_feedbacks, max_feedbacks)
        speed_score = self._delivery_score(product, min_delivery, max_delivery)

        raw = (
            prefs.price_weight * price_score
            + prefs.rating_weight * rating_score
            + prefs.feedbacks_weight * feedbacks_score
            + prefs.speed_weight * speed_score
        )

        return round(max(0.0, min(1.0, raw)) * self._SCALE, 1)

    @staticmethod
    def _total_cost(product: ProductDTO) -> float:
        return product.price + (product.delivery_price or 0)

    @staticmethod
    def _delivery_score(product: ProductDTO, min_days: float, max_days: float) -> float:
        if product.delivery_days is None:
            base = 0.5
        elif max_days == min_days:
            base = 1.0
        else:
            base = 1.0 - (product.delivery_days - min_days) / (max_days - min_days)

        if product.delivery_free:
            return min(1.0, base + 0.15)

        return base

    @staticmethod
    def _normalize(value: float, min_val: float, max_val: float) -> float:
        if max_val == min_val:
            return 1.0
        return (value - min_val) / (max_val - min_val)

    @staticmethod
    def _normalize_inverted(value: float, min_val: float, max_val: float) -> float:
        if max_val == min_val:
            return 1.0
        return 1.0 - (value - min_val) / (max_val - min_val)
