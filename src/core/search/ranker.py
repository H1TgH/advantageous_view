from core.preferences.entities import UserPreferencesDTO
from core.search.entities import ProductDTO


class ProductRanker:
    def rank(self, products: list[ProductDTO], preferences: UserPreferencesDTO) -> list[ProductDTO]:
        if not products:
            return []

        prefs = preferences.normalized()

        prices = [p.price for p in products if p.price > 0]
        ratings = [p.rating for p in products]
        feedbacks = [p.feedbacks for p in products]
        delivery_days = [p.delivery_days for p in products if p.delivery_days is not None]

        min_price, max_price = (min(prices), max(prices)) if prices else (0, 1)
        min_rating, max_rating = (min(ratings), max(ratings)) if ratings else (0, 1)
        min_feedbacks, max_feedbacks = (min(feedbacks), max(feedbacks)) if feedbacks else (0, 1)
        min_delivery, max_delivery = (min(delivery_days), max(delivery_days)) if delivery_days else (0, 1)

        for product in products:
            product.score = self._score(
                product,
                prefs,
                min_price,
                max_price,
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
        min_price: float,
        max_price: float,
        min_rating: float,
        max_rating: float,
        min_feedbacks: float,
        max_feedbacks: float,
        min_delivery: float,
        max_delivery: float,
    ) -> float:
        price_score = self._normalize_inverted(product.price, min_price, max_price)
        rating_score = self._normalize(product.rating, min_rating, max_rating)
        feedbacks_score = self._normalize(product.feedbacks, min_feedbacks, max_feedbacks)
        speed_score = self._delivery_score(product.delivery_days, min_delivery, max_delivery)

        return (
            prefs.price_weight * price_score
            + prefs.rating_weight * rating_score
            + prefs.feedbacks_weight * feedbacks_score
            + prefs.speed_weight * speed_score
        )

    @staticmethod
    def _delivery_score(days: int | None, min_days: float, max_days: float) -> float:
        if days is None:
            return 0.5
        if max_days == min_days:
            return 1.0
        return 1.0 - (days - min_days) / (max_days - min_days)

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
