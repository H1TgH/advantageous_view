from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.search.router import search_router
from api.users.router import users_router
from api.notifications.router import notifications_router
from api.price_tracking.router import price_tracking_router

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

api_router = APIRouter(prefix="/api/v1")

# routers
api_router.include_router(search_router)
api_router.include_router(users_router)
api_router.include_router(price_tracking_router)
api_router.include_router(notifications_router)

# include api
app.include_router(api_router)

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)