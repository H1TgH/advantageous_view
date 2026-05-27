from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from infrastructure.database.models.users import UserModel


@dataclass
class UserCreationDTO:
    name: str
    email: str
    password: str


@dataclass
class UserModelDTO:
    id: UUID
    email: str
    password: str
    name: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, user: UserModel | None) -> "UserModelDTO | None":
        return cls(
            id=user.id,
            email=user.email,
            password=user.password,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
        ) if user else None


@dataclass
class UserReadDTO:
    id: UUID
    name: str
    email: str

    @classmethod
    def from_model(cls, user: UserModel) -> "UserReadDTO":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
        )


@dataclass
class UserLoginDTO:
    email: str
    password: str


@dataclass
class UpdateUserDTO:
    name: str
    email: str


@dataclass
class LoginTokensDTO:
    access_token: str
    refresh_token: str


@dataclass
class AuthUserDTO:
    id: UUID


@dataclass
class UserNotificationSettingsDTO:
    user_id: UUID
    notifications_enabled: bool
    subscription_price_changes: bool
    subscription_new_features: bool
    notify_in_app: bool
    notify_email: bool
