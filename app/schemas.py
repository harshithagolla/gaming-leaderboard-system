# app/schemas.py
from pydantic import BaseModel

class SubmitScoreReq(BaseModel):
    user_id: int
    score: int

class LeaderboardEntry(BaseModel):
    user_id: int
    username: str | None = None
    total_score: int

class RankResp(BaseModel):
    user_id: int
    total_score: int
    rank: int
