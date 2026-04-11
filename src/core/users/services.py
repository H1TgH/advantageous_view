import asyncio
from datetime import UTC, datetime, timedelta

import bcrypt
from jose import ExpiredSignatureError, JWTError, jwt

from core.users.entities import AuthUserDTO, LoginTokensDTO, UserCreationDTO, UserLoginDTO, UserModelDTO
from core.users.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserDoesNotExistException,
)
from infrastructure.database.repositories.users import UserRepository
from infrastructure.database.uow import UnitOfWork
from settings import settings


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def register(self, user_data: UserCreationDTO) -> None:
        async with self.uow() as session:
            repo = UserRepository(session)
            await self._validate_uniqueness(repo, user_data.email)
            user_data.password = await self._hash_password(user_data.password)
            await repo.add(user_data)

    async def _validate_uniqueness(self, repo: UserRepository, email: str):
        user = await repo.get_by_email(email)
        if user:
            raise UserAlreadyExistsException("Email already exists")

    @staticmethod
    async def _hash_password(password: str) -> str:
        hashed = await asyncio.to_thread(
            bcrypt.hashpw,
            password.encode(),
            bcrypt.gensalt(),
        )
        return hashed.decode()

    async def login(self, creds: UserLoginDTO) -> LoginTokensDTO:
        user = await self._authenticate(creds)

        access_token = self._create_token(
            {"sub": str(user.id), "type": "access"},
            expires_delta=timedelta(minutes=settings.security.access_ttl)
        )

        refresh_token = self._create_token(
            {"sub": str(user.id), "type": "refresh"},
            expires_delta=timedelta(days=settings.security.refresh_ttl)
        )

        return LoginTokensDTO(access_token, refresh_token)

    async def _authenticate(self, creds: UserLoginDTO) -> AuthUserDTO:
        async with self.uow() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email(creds.email)
            await self._validate_credentials(user, creds.password)

            dto = AuthUserDTO(id=user.id)

        return dto

    @staticmethod
    async def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return await asyncio.to_thread(
            bcrypt.checkpw,
            plain_password.encode(),
            hashed_password.encode(),
        )

    async def _validate_credentials(self, user: UserModelDTO, password: str) -> None:
        if not user or not await self._verify_password(password, user.password):
            raise InvalidCredentialsException("Incorrect email or password")

    @staticmethod
    def _create_token(data: dict, expires_delta: timedelta) -> str:
        payload = data.copy()
        exp = datetime.now(UTC) + expires_delta
        payload.update({"exp": exp})

        return jwt.encode(
            payload,
            settings.security.secret_key.get_secret_value(),
            settings.security.algorithm,
        )

    @staticmethod
    def _verify_token(token: str, token_type: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.security.secret_key.get_secret_value(),
                settings.security.algorithm,
            )
        except ExpiredSignatureError as e:
            raise InvalidTokenException("Token expired") from e
        except JWTError as e:
            raise InvalidTokenException(str(e)) from e

        if payload.get("type") != token_type:
            raise InvalidTokenException("Invalid token type")

        return payload

    def refresh(self, refresh_token: str) -> str:
        user_id = self.get_user_id_from_token_or_raise(refresh_token, "refresh")
        return self._create_token(
            {"sub": user_id, "type": "access"},
            timedelta(minutes=settings.security.access_ttl)
        )

    def get_user_id_from_token_or_raise(self, token: str, token_type: str) -> str:
        payload = self._verify_token(token, token_type)
        return payload.get("sub")

    async def get_current_user(self, token: str) -> AuthUserDTO:
        async with self.uow() as session:
            repo = UserRepository(session)
            user_id = self.get_user_id_from_token_or_raise(token, "access")
            await self._get_by_id_or_raise(repo, user_id)

            dto = AuthUserDTO(
                id=user_id
            )

        return dto

    @staticmethod
    async def _get_by_id_or_raise(repo: UserRepository, user_id) -> UserModelDTO:
        user = await repo.get_by_id(user_id)
        if not user:
            raise UserDoesNotExistException("User does not exists")
        return user


def get_user_service() -> UserService:
    return UserService(UnitOfWork())
