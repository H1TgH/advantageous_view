from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.database import Base


class UserPreferencesModel(Base):
    __tablename__ = "user_preferences"

    user_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    price_weight: Mapped[float] = mapped_column(server_default="0.5")
    rating_weight: Mapped[float] = mapped_column(server_default="0.25")
    feedbacks_weight: Mapped[float] = mapped_column(server_default="0.25")
