from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.search.router import search_router
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

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(search_router)
api_router.include_router(users_router)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)