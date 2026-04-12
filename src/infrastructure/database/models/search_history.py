from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.database import Base


class SearchHistoryModel(Base):
    __tablename__ = "search_history"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    query: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
