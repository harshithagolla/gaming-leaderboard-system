# app/main.py
from fastapi import FastAPI
from .routes import router
from .db import engine, Base
import os

app = FastAPI(title="Leaderboard API")

app.include_router(router)

# Create tables if not exist (optional; recommended while developing)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
