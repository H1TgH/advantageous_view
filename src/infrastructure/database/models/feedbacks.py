from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.database import Base


class FeedbackModel(Base):
    __tablename__ = "feedbacks"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    product_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    seller: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=""
    )

    marketplace: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="wb"
    )

    product_matched_description: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True
    )

    delivery_on_time: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True
    )

    overall_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
