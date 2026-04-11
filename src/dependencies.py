

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.users.entities import AuthUserDTO
from core.users.exceptions import InvalidTokenException, UserDoesNotExistException
from core.users.services import UserService, get_user_service


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    auth_service: UserService = Depends(get_user_service)
) -> AuthUserDTO:
    try:
        token = credentials.credentials
        return await auth_service.get_current_user(token)
    except InvalidTokenException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        ) from e
    except UserDoesNotExistException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
