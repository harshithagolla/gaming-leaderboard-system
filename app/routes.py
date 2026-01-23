from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .db import get_db
from . import crud, schemas
from .cache import get_redis, rank_key, top_key
import json

router = APIRouter()


@router.post("/submit", response_model=schemas.RankResp)
def submit_score(payload: schemas.SubmitScoreReq, db: Session = Depends(get_db)):
    if payload.score < 0:
        raise HTTPException(
            status_code=400, detail="score must be non-negative")
    try:
        crud.ensure_user_exists(db, payload.user_id, payload.username)
        crud.insert_game_session(db, payload.user_id, payload.score)
        crud.upsert_leaderboard_increment(db, payload.user_id, payload.score)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    redis = get_redis()
    if redis:
        for key in redis.scan_iter("leaderboard:top:*"):
            redis.delete(key)
        redis.delete(rank_key(payload.user_id))


    total = crud.get_user_total_score(db, payload.user_id)
    rank = crud.get_user_rank(db, payload.user_id)
    return {"user_id": payload.user_id, "total_score": total, "rank": rank}


@router.get("/top")
def get_top(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    redis = get_redis()
    cache_key = top_key(limit, offset)

    if redis:
        cached = redis.get(cache_key)
        if cached:
            return {"top": json.loads(cached)}

    rows = crud.get_top_n(db, limit=limit, offset=offset)

    if redis:
        redis.setex(cache_key, 10, json.dumps(rows))  # cache for 10 sec

    return {"top": rows}



@router.get("/rank/{user_id}")
def get_rank(user_id: int, db: Session = Depends(get_db)):
    redis = get_redis()
    cache_key = rank_key(user_id)

    if redis:
        cached = redis.get(cache_key)
        if cached:
            return json.loads(cached)

    total = crud.get_user_total_score(db, user_id)

    if total == 0:
        cnt = db.execute("SELECT COUNT(*) FROM leaderboard").scalar()
        result = {"user_id": user_id, "total_score": 0, "rank": int(cnt) + 1}
    else:
        rank = crud.get_user_rank(db, user_id)
        result = {"user_id": user_id, "total_score": total, "rank": rank}

    if redis:
        redis.setex(cache_key, 10, json.dumps(result))  # TTL = 10 sec

    return result

