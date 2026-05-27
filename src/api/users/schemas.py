from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegistrationSchema(BaseModel):
    email: EmailStr
    name: str
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenSchema(BaseModel):
    token: str


class UserMeSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr


class UpdateMeSchema(BaseModel):
    name: str
    email: EmailStr


class UserNotificationSettingsSchema(BaseModel):
    notifications_enabled: bool
    subscription_price_changes: bool
    subscription_new_features: bool
    notify_in_app: bool
    notify_email: bool


class UpdateUserNotificationSettingsSchema(UserNotificationSettingsSchema):
    pass
