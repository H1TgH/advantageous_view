from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.database import Base


class NotificationModel(Base):
    __tablename__ = "notifications"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    subscription_id: Mapped[UUID | None] = mapped_column(
        PGUUID,
        ForeignKey("price_subscriptions.id", ondelete="SET NULL"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
