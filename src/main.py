from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.favorites.router import favorites_router
from api.feedbacks.router import feedback_router
from api.notifications.router import notifications_router
from api.preferences.router import preferences_router
from api.price_tracking.router import price_tracking_router
from api.search.router import search_router
from api.search_history.router import search_history_router
from api.users.router import users_router
from infrastructure.marketplaces.wb import WBClient
from infrastructure.marketplaces.ym import YandexMarketClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.wb_client = WBClient()
    app.state.ym_client = YandexMarketClient()
    yield
    await app.state.wb_client.close()
    await app.state.ym_client.close()


app = FastAPI(lifespan=lifespan)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(users_router)
api_v1_router.include_router(search_router)
api_v1_router.include_router(preferences_router)
api_v1_router.include_router(search_history_router)
api_v1_router.include_router(favorites_router)
api_v1_router.include_router(price_tracking_router)
api_v1_router.include_router(notifications_router)
api_v1_router.include_router(feedback_router)

app.include_router(api_v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
