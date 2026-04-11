from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.users.entities import UserCreationDTO, UserModelDTO
from infrastructure.database.models.users import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user_data: UserCreationDTO) -> None:
        new_user = UserModel(**asdict(user_data))
        self.session.add(new_user)

    async def get_by_email(self, email: str) -> UserModelDTO | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        return UserModelDTO.from_model(
            result.scalar_one_or_none()
        )

    async def get_by_id(self, id: UUID) -> UserModelDTO | None:
        stmt = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(stmt)
        return UserModelDTO.from_model(
            result.scalar_one_or_none()
        )
