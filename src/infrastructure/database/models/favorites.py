from uuid import UUID

from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.database import Base


class FavoriteModel(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_favorites_user_product"),)

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

    brand: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=""
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )

    rating: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )

    feedbacks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
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

    url: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=""
    )
