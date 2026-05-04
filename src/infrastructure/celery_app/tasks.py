import asyncio
import logging

from infrastructure.celery_app.app import celery_app
from infrastructure.email.service import EmailService


logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name="send_price_alert",
)
def send_price_alert_task(
    self,
    to_email: str,
    product_title: str,
    old_price: float,
    new_price: float,
    url: str,
    reason: str,
) -> None:
    discount = old_price - new_price
    discount_pct = (discount / old_price * 100) if old_price else 0

    subject = f"Снижение цены: {product_title}"
    body = (
        f"Привет!\n\n"
        f'Цена на товар "{product_title}" {reason}.\n\n'
        f"Было:   {old_price:,.0f} ₽\n"
        f"Стало:  {new_price:,.0f} ₽\n"
        f"Выгода: {discount:,.0f} ₽ ({discount_pct:.1f}%)\n\n"
        f"Ссылка на товар:\n{url}\n\n"
        f"---\n"
        f"Выгодный Взгляд — вы получили это письмо, "
        f"потому что отслеживаете цену этого товара."
    )

    try:
        EmailService().send(to_email, subject, body)
    except Exception as exc:
        logger.error("send_price_alert упала: %s", exc)
        raise self.retry(exc=exc) from exc


@celery_app.task(name="check_prices")
def check_prices_task() -> None:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
    from sqlalchemy.pool import NullPool

    from core.price_tracking.checker import PriceCheckerService
    from infrastructure.database.uow import UnitOfWork
    from infrastructure.marketplaces.wb import WBClient
    from infrastructure.marketplaces.ym import YandexMarketClient
    from settings import settings

    async def _run() -> None:

        engine = create_async_engine(
            settings.db.database_url,
            poolclass=NullPool,
        )
        session_factory = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        uow = UnitOfWork(session_factory=session_factory)

        try:
            service = PriceCheckerService(
                uow=uow,
                wb_client=WBClient(),
                ym_client=YandexMarketClient(),
            )
            results = await service.run()
        finally:
            await engine.dispose()

        if not results:
            return

        for item in results:
            _sub_id, new_price, email, old_price, title, url, reason = item
            send_price_alert_task.delay(
                to_email=email,
                product_title=title,
                old_price=old_price,
                new_price=new_price,
                url=url,
                reason=reason,
            )

    asyncio.run(_run())
