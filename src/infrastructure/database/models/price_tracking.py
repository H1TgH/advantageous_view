from uuid import UUID

from sqlalchemy import Boolean, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.database import Base


class PriceSubscriptionModel(Base):
    __tablename__ = "price_subscriptions"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_subscriptions_user_product"),)

    user_id: Mapped[UUID] = mapped_column(
        PGUUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    product_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=""
    )

    marketplace: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="wb"
    )

    target_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )


class PriceHistoryModel(Base):
    __tablename__ = "price_history"

    subscription_id: Mapped[UUID] = mapped_column(
        PGUUID,
        ForeignKey("price_subscriptions.id", ondelete="CASCADE"),
        nullable=False,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
