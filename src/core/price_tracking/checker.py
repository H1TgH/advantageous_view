import logging
from uuid import UUID

from core.notifications.entities import CreateNotificationDTO
from core.price_tracking.entities import PriceCheckAlert, PriceSubscriptionDTO
from infrastructure.database.repositories.notifications import NotificationRepository
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

    async def run(self) -> list[PriceCheckAlert]:
        logger.info("Запуск проверки цен по подпискам")

        async with self._uow() as session:
            repo = PriceTrackingRepository(session)
            rows = await repo.get_active_subscriptions_with_emails()

        if not rows:
            logger.info("Активных подписок нет, выходим")
            return []

        logger.info("Найдено %d активных подписок", len(rows))

        alerts: list[PriceCheckAlert] = []
        for sub, user_id, email in rows:
            alert = await self._check_one(sub, user_id, email)
            if alert is not None:
                alerts.append(alert)

        async with self._uow() as session:
            price_repo = PriceTrackingRepository(session)
            notif_repo = NotificationRepository(session)

            for alert in alerts:
                await price_repo.add_price_history(alert.subscription_id, alert.new_price)

                if alert.notify_in_app:
                    await notif_repo.create(
                        CreateNotificationDTO(
                            user_id=alert.user_id,
                            subscription_id=alert.subscription_id,
                            title=f"Снижение цены: {alert.title}",
                            message=self._build_message(alert),
                        )
                    )

        logger.info("Проверка завершена. Событий для уведомлений: %d", len(alerts))
        return alerts

    async def _check_one(
        self,
        sub: PriceSubscriptionDTO,
        user_id: UUID,
        email: str,
    ) -> PriceCheckAlert | None:
        current_price = await self._fetch_min_price(sub)
        if current_price is None:
            logger.warning("Не удалось получить цену для подписки %s (%s)", sub.id, sub.title)
            return None

        async with self._uow() as session:
            repo = PriceTrackingRepository(session)
            last_price = await repo.get_last_price(sub.id)

            if last_price is None:
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

        if not sub.notify_in_app and not sub.notify_email:
            logger.debug("Подписка %s: уведомления отключены", sub.id)
            return None

        logger.info(
            "Подписка %s (%s): цена %.0f ₽ → %.0f ₽, причина: %s",
            sub.id, sub.title, last_price, current_price, reason,
        )
        return PriceCheckAlert(
            subscription_id=sub.id,
            user_id=user_id,
            email=email,
            new_price=current_price,
            old_price=last_price,
            title=sub.title,
            url=sub.url,
            reason=reason,
            notify_in_app=sub.notify_in_app,
            notify_email=sub.notify_email,
        )

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

    @staticmethod
    def _build_message(alert: PriceCheckAlert) -> str:
        discount = alert.old_price - alert.new_price
        discount_pct = (discount / alert.old_price * 100) if alert.old_price else 0
        return (
            f"Цена на «{alert.title}» {alert.reason}.\n"
            f"Было: {alert.old_price:,.0f} ₽ → Стало: {alert.new_price:,.0f} ₽ "
            f"({discount:,.0f} ₽, {discount_pct:.1f}%)\n"
            f"{alert.url}"
        )