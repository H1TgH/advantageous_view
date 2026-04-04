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
