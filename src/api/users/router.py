from fastapi import APIRouter, Depends, status

from api.users.schemas import LoginResponseSchema, LoginSchema, RegistrationSchema, TokenSchema
from core.users.entities import UserCreationDTO, UserLoginDTO
from core.users.services import UserService, get_user_service


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


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
