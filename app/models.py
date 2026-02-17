from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    join_date = Column(TIMESTAMP, server_default=func.now())
    password_hash = Column(String(255), nullable=False)

class GameSession(Base):
    __tablename__ = "game_sessions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    game_mode = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    total_score = Column(BigInteger, nullable=False, default=0)
