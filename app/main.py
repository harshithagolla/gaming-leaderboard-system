from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as leaderboard_router
from .db import engine, Base
from .auth import router as auth_router
from .cache import init_redis

app = FastAPI(title="Leaderboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leaderboard_router, prefix="/api/leaderboard")
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Leaderboard API is running "}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    try:
        init_redis()
    except Exception:
        print("Redis not available, running without cache")
