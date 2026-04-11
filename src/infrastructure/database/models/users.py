from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.database import Base


class UserModel(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
    )

    password: Mapped[str] = mapped_column(
        String,
    )

    name: Mapped[str] = mapped_column(
        String,
    )
