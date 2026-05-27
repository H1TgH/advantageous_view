from fastapi import APIRouter, Depends, status

from api.users.schemas import (
    LoginResponseSchema,
    LoginSchema,
    RegistrationSchema,
    TokenSchema,
    UpdateMeSchema,
    UserMeSchema,
)
from core.users.entities import AuthUserDTO, UpdateUserDTO, UserCreationDTO, UserLoginDTO
from core.users.services import UserService, get_user_service
from dependencies import get_current_user


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@users_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserMeSchema,
)
async def get_me(
    current_user: AuthUserDTO = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserMeSchema:
    user = await service.get_me(current_user.id)
    return UserMeSchema(**vars(user))


@users_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: RegistrationSchema,
    service: UserService = Depends(get_user_service),
):
    dto = UserCreationDTO(**user_data.model_dump())

    await service.register(dto)


@users_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponseSchema
)
async def login(
    creds: LoginSchema,
    service: UserService = Depends(get_user_service),
):
    dto = UserLoginDTO(**creds.model_dump())

    tokens = await service.login(dto)

    return LoginResponseSchema(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )


@users_router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=TokenSchema,
)
async def refresh(
    token: TokenSchema,
    service: UserService = Depends(get_user_service),
):
    new_token = service.refresh(token.token)

    return TokenSchema(token=new_token)


@users_router.patch(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserMeSchema,
)
async def update_me(
    data: UpdateMeSchema,
    current_user: AuthUserDTO = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserMeSchema:
    user = await service.update_me(current_user.id, UpdateUserDTO(**data.model_dump()))
    return UserMeSchema(**vars(user))
