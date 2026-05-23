from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.users.router import users_router
from api.search.router import search_router  # ✅ раскомментируй!

app = FastAPI(title="Advantageous View API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:5500", "http://localhost:5500", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(users_router)
api_v1_router.include_router(search_router)  # ✅ раскомментируй!

app.include_router(api_v1_router)

# Закрытие ресурсов при выключении
@app.on_event("shutdown")
async def shutdown_event():
    from core.search.services import get_search_service
    service = get_search_service()
    await service.close()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Advantageous View API is running"}