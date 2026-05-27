
from core.preferences.entities import UserPreferencesDTO
from core.search.entities import ProductDTO


_BAYESIAN_C = 50.0


class ProductRanker:
    _SCALE = 100.0

    def rank(self, products: list[ProductDTO], preferences: UserPreferencesDTO) -> list[ProductDTO]:
        if not products:
            return []

        prefs = preferences.normalized()

        total_costs = [self._total_cost(p) for p in products if p.price > 0]
        delivery_days = [p.delivery_days for p in products if p.delivery_days is not None]
        ratings = [p.rating for p in products if p.rating > 0]

        min_cost, max_cost = (min(total_costs), max(total_costs)) if total_costs else (0, 1)
        min_delivery, max_delivery = (min(delivery_days), max(delivery_days)) if delivery_days else (0, 1)
        global_mean_rating = sum(ratings) / len(ratings) if ratings else 4.0

        for product in products:
            product.score = self._score(
                product,
                prefs,
                min_cost,
                max_cost,
                min_delivery,
                max_delivery,
                global_mean_rating,
            )

        return sorted(products, key=lambda p: p.score or 0, reverse=True)

    def _score(
        self,
        product: ProductDTO,
        prefs: UserPreferencesDTO,
        min_cost: float,
        max_cost: float,
        min_delivery: float,
        max_delivery: float,
        global_mean_rating: float,
    ) -> float:
        price_score = (
            self._normalize_inverted(self._total_cost(product), min_cost, max_cost)
            if product.price > 0
            else 0.0
        )

        trust_score = self._bayesian_trust(product.rating, product.feedbacks, global_mean_rating)
        speed_score = self._delivery_score(product, min_delivery, max_delivery)

        trust_weight = prefs.rating_weight + prefs.feedbacks_weight

        raw = (
            prefs.price_weight * price_score
            + trust_weight * trust_score
            + prefs.speed_weight * speed_score
        )

        return round(max(0.0, min(1.0, raw)) * self._SCALE, 1)

    @staticmethod
    def _bayesian_trust(rating: float, feedbacks: int, global_mean: float) -> float:
        if rating <= 0:
            return 0.0
        bayesian = (_BAYESIAN_C * global_mean + feedbacks * rating) / (_BAYESIAN_C + feedbacks)
        return (bayesian - 1.0) / 4.0

    @staticmethod
    def _total_cost(product: ProductDTO) -> float:
        return product.price + (product.delivery_price or 0)

    @staticmethod
    def _delivery_score(product: ProductDTO, min_days: float, max_days: float) -> float:
        if product.delivery_days is None:
            return 0.2
        if max_days == min_days:
            return 1.0
        return 1.0 - (product.delivery_days - min_days) / (max_days - min_days)

    @staticmethod
    def _normalize_inverted(value: float, min_val: float, max_val: float) -> float:
        if max_val == min_val:
            return 1.0
        return 1.0 - (value - min_val) / (max_val - min_val)
