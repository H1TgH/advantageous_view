import logging

from core.price_tracking.entities import PriceSubscriptionDTO
from infrastructure.database.repositories.price_tracking import PriceTrackingRepository
from infrastructure.database.uow import UnitOfWork
from infrastructure.marketplaces.wb import WBClient
from infrastructure.marketplaces.ym import YandexMarketClient


logger = logging.getLogger(__name__)

PRICE_DROP_THRESHOLD = 0.05


class PriceCheckerService:
    def __init__(
        self,
        uow: UnitOfWork,
        wb_client: WBClient,
        ym_client: YandexMarketClient,
    ) -> None:
        self._uow = uow
        self._wb = wb_client
        self._ym = ym_client

    async def run(self) -> None:
        logger.info("Запуск проверки цен по подпискам")

        async with self._uow() as session:
            repo = PriceTrackingRepository(session)
            rows = await repo.get_active_subscriptions_with_emails()

        if not rows:
            logger.info("Активных подписок нет, выходим")
            return

        logger.info("Найдено %d активных подписок", len(rows))

        results = []
        for sub, email in rows:
            result = await self._check_one(sub, email)
            if result is not None:
                results.append(result)

        async with self._uow() as session:
            repo = PriceTrackingRepository(session)
            for sub_id, new_price, _email, _old_price, _title, _url, _reason in results:
                await repo.add_price_history(sub_id, new_price)

        logger.info("Проверка завершена. Событий для уведомлений: %d", len(results))
        return results

    async def _check_one(
        self,
        sub: PriceSubscriptionDTO,
        email: str,
    ) -> tuple | None:
        """
        Возвращает (sub_id, new_price, email, old_price, reason)
        если нужно уведомить, иначе None.
        """
        current_price = await self._fetch_min_price(sub)
        if current_price is None:
            logger.warning("Не удалось получить цену для подписки %s (%s)", sub.id, sub.title)
            return None

        async with self._uow() as session:
            repo = PriceTrackingRepository(session)
            last_price = await repo.get_last_price(sub.id)

        if last_price is None:
            async with self._uow() as session:
                repo = PriceTrackingRepository(session)
                await repo.add_price_history(sub.id, current_price)
            logger.info("Первая запись цены для подписки %s: %.0f ₽", sub.id, current_price)
            return None

        reason = self._should_notify(sub, current_price, last_price)
        if reason is None:
            logger.debug(
                "Подписка %s: цена %.0f ₽ → %.0f ₽, уведомление не нужно",
                sub.id, last_price, current_price,
            )
            return None

        logger.info(
            "Подписка %s (%s): цена %.0f ₽ → %.0f ₽, причина: %s",
            sub.id, sub.title, last_price, current_price, reason,
        )
        return (sub.id, current_price, email, last_price, sub.title, sub.url, reason)

    async def _fetch_min_price(self, sub: PriceSubscriptionDTO) -> float | None:
        try:
            if sub.marketplace == "wb":
                offers = await self._wb.get_model_offers(sub.product_id)
            else:
                offers = await self._ym.get_model_offers(sub.product_id)
        except Exception as e:
            logger.error("Ошибка запроса к маркетплейсу для подписки %s: %s", sub.id, e)
            return None

        prices = [o.price for o in offers if o.price > 0]
        if not prices:
            return None

        return min(prices)

    @staticmethod
    def _should_notify(
        sub: PriceSubscriptionDTO,
        current_price: float,
        last_price: float,
    ) -> str | None:
        if sub.target_price is not None and current_price <= sub.target_price:
            return f"достигла целевой цены {sub.target_price:,.0f} ₽"

        if last_price > 0:
            drop = (last_price - current_price) / last_price
            if drop >= PRICE_DROP_THRESHOLD:
                return f"снизилась на {drop * 100:.1f}%"

        return None
