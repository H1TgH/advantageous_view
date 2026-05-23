# src/api/users/schemas.py
from pydantic import BaseModel, EmailStr, Field


class RegistrationSchema(BaseModel):
    """Данные для регистрации"""
    email: EmailStr = Field(..., description="Email пользователя", example="user@example.com")
    name: str = Field(..., min_length=2, max_length=50, description="Имя пользователя", example="Иван")
    password: str = Field(..., min_length=6, max_length=128, description="Пароль", example="secure123")


class LoginSchema(BaseModel):
    """Данные для входа"""
    email: EmailStr = Field(..., description="Email пользователя", example="user@example.com")
    password: str = Field(..., description="Пароль", example="secure123")


class LoginResponseSchema(BaseModel):
    """Ответ после успешного входа"""
    access_token: str = Field(..., description="Access токен для авторизации запросов")
    refresh_token: str = Field(..., description="Refresh токен для обновления access токена")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class TokenSchema(BaseModel):
    """Схема токена (для refresh)"""
    token: str = Field(..., description="Токен (access или refresh)")


class UserResponseSchema(BaseModel):
    """Данные пользователя в ответе"""
    email: EmailStr
    name: str
    is_active: bool = True
    
    class Config:
        from_attributes = True  # для совместимости с ORM