from uuid import UUID

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.database import Base


class UserNotificationSettingsModel(Base):
    __tablename__ = "user_notification_settings"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    notifications_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    subscription_price_changes: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    subscription_new_features: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notify_in_app: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notify_email: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
