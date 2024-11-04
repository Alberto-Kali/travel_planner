from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import planning, auth
from app.db.init_db import init_db
from app.db.initial_data import init_places
from app.db.base import SessionLocal

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(planning.router)

@app.on_event("startup")
async def startup_event():
    init_db()
    db = SessionLocal()
    init_places(db)
    db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Travel Planner API"}