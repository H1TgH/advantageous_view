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

        min_price, max_price = (min(prices), max(prices)) if prices else (0, 1)
        min_rating, max_rating = (min(ratings), max(ratings)) if ratings else (0, 1)
        min_feedbacks, max_feedbacks = (min(feedbacks), max(feedbacks)) if feedbacks else (0, 1)

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
            )

        # 👇 сортируем уже по полю
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
    ) -> float:
        price_score = self._normalize_inverted(product.price, min_price, max_price)
        rating_score = self._normalize(product.rating, min_rating, max_rating)
        feedbacks_score = self._normalize(product.feedbacks, min_feedbacks, max_feedbacks)

        return (
            prefs.price_weight * price_score
            + prefs.rating_weight * rating_score
            + prefs.feedbacks_weight * feedbacks_score
        )

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
