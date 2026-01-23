# app/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from . import crud, schemas

router = APIRouter(prefix="/api/leaderboard")

@router.post("/submit")
def submit_score(payload: schemas.SubmitScoreReq, db: Session = Depends(get_db)):
    if payload.score < 0:
        raise HTTPException(status_code=400, detail="score must be non-negative")
    # Wrap in transaction
    try:
        insert_session_and_update = False
        # insert session and update leaderboard as a single transaction
        crud.insert_game_session(db, payload.user_id, payload.score)
        crud.upsert_leaderboard_increment(db, payload.user_id, payload.score)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    total = crud.get_user_total_score(db, payload.user_id)
    rank = crud.get_user_rank(db, payload.user_id)
    return {"user_id": payload.user_id, "total_score": total, "rank": rank}

@router.get("/top")
def get_top(db: Session = Depends(get_db)):
    rows = crud.get_top_n(db, 10)
    return {"top": rows}

@router.get("/rank/{user_id}")
def get_rank(user_id: int, db: Session = Depends(get_db)):
    total = crud.get_user_total_score(db, user_id)
    if total == 0:
        # user might not exist in leaderboard yet; still return rank as last
        # We'll return rank = count_total + 1
        q = "SELECT COUNT(*) FROM leaderboard"
        cnt = db.execute(q).scalar()
        return {"user_id": user_id, "total_score": 0, "rank": int(cnt) + 1}
    rank = crud.get_user_rank(db, user_id)
    return {"user_id": user_id, "total_score": total, "rank": rank}
