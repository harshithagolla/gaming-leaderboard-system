# app/cache.py
import os
import redis
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

redis_client: Optional[redis.Redis] = None

def init_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True,
            socket_keepalive=True
        )
        # quick ping to ensure connection (raises if cannot connect)
        try:
            redis_client.ping()
        except Exception as e:
            # if redis is not available, keep None => routes will handle it gracefully
            redis_client = None
            raise

def get_redis():
    return redis_client

def top_key(n: int = 10):
    return f"leaderboard:top:{n}"

def rank_key(user_id: int):
    return f"leaderboard:rank:{user_id}"
