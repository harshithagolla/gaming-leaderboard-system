from sqlalchemy.orm import Session
from sqlalchemy import text
from . import models

def insert_game_session(db: Session, user_id: int, score: int, game_mode: str = "solo"):
    gs = models.GameSession(user_id=user_id, score=score, game_mode=game_mode)
    db.add(gs)
    db.flush()

def ensure_user_exists(db: Session, user_id: int, username: str | None = None):
    user = db.get(models.User, user_id)
    if not user:
        user = models.User(
            id=user_id,
            username=username or f"user_{user_id}"
        )
        db.add(user)
        db.flush()
    else:
        if username and user.username != username:
            user.username = username

def upsert_leaderboard_increment(db: Session, user_id: int, score: int):
    # Use raw SQL ON DUPLICATE KEY UPDATE for performance & atomic increment
    sql = text("""
    INSERT INTO leaderboard (user_id, total_score)
    VALUES (:user_id, :score)
    ON DUPLICATE KEY UPDATE total_score = leaderboard.total_score + :score
    """)
    db.execute(sql, {"user_id": user_id, "score": score})

def get_top_n(db: Session, limit: int = 10, offset: int = 0):
    q = text("""
    SELECT l.user_id, u.username, l.total_score
    FROM leaderboard l
    JOIN users u ON u.id = l.user_id
    ORDER BY l.total_score DESC
    LIMIT :limit OFFSET :offset
    """)
    res = db.execute(q, {"limit": limit, "offset": offset}).fetchall()
    return [
        {"user_id": r[0], "username": r[1], "total_score": int(r[2])}
        for r in res
    ]

def get_user_total_score(db: Session, user_id: int):
    q = text("SELECT total_score FROM leaderboard WHERE user_id = :user_id")
    r = db.execute(q, {"user_id": user_id}).fetchone()
    return int(r[0]) if r else 0

def get_user_rank(db: Session, user_id: int):
    total = get_user_total_score(db, user_id)
    # Count how many users have a strictly greater score
    q = text("SELECT COUNT(*) FROM leaderboard WHERE total_score > :total")
    cnt = db.execute(q, {"total": total}).scalar()
    return int(cnt) + 1
