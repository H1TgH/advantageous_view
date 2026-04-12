from fastapi import APIRouter, FastAPI

from api.preferences.router import preferences_router
from api.search.router import search_router
from api.users.router import users_router


app = FastAPI()

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(users_router)
api_v1_router.include_router(search_router)
api_v1_router.include_router(preferences_router)

app.include_router(api_v1_router)
