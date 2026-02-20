# 🎮 Gaming Leaderboard System

A fully containerized, scalable backend system for managing a real-time gaming leaderboard with JWT authentication, pagination, Redis caching.

This project demonstrates backend engineering concepts including database design, authentication flows, caching strategies, cache invalidation, service orchestration, and Docker-based multi-container infrastructure.
---

## ✨ Features

- User registration and login (JWT authentication)
- Secure protected endpoints using Bearer tokens
- Submit player scores (authenticated)
- Automatic leaderboard updates
- Cumulative score tracking per user
- Store individual game sessions
- Fetch top players (paginated)
- Fetch rank by user ID
- Fetch current logged-in user rank
- Redis caching for read-heavy APIs
- Cache invalidation on score updates
- Graceful fallback when Redis is unavailable

---

## 🏗 Architecture Overview

The system runs as multiple isolated containers using Docker Compose:
- Backend API (FastAPI)
- MySQL Database
- Redis Cache
- Frontend (Static HTML + JS)

---

## 🛠 Technologies Used

**Backend**
- Python 3.10
- FastAPI
- SQLAlchemy (ORM)
- PyMySQL
- Uvicorn
- Passlib (bcrypt hashing)
- Python-JOSE (JWT)

**Database**
- MySQL

**Caching**
- Redis

**Infrastructure**
- Docker
- Docker compose

**Frontend**
- HTML, CSS
- Vanilla JavaScript (Fetch API)

---

## 📌 API Endpoints

**Authentication**
- POST /auth/register
- POST /auth/login

**Leaderboard**
- POST /api/leaderboard/submit (Protected)
- GET /api/leaderboard/top?limit=10&offset=0
- GET /api/leaderboard/rank/{user_id}
- GET /api/leaderboard/rank/me (Protected)

---

## ⚡ Caching Strategy

- Read-through Redis caching
- Cached endpoints:
  - Leaderboard pages (`/top`)
  - User rank (`/rank/{user_id}`)
- Cache keys include pagination parameters
- Cache invalidated on score submission
- Short TTL for freshness

---

## 🔐 Authentication

- JWT-based authentication
- Password hashing using bcrypt
- Token-based access control for protected APIs
- Secure dependency injection using FastAPI Depends

---

## 🐳 Docker-Based Setup

1️⃣ Clone repository
git clone <repo-url>
cd gaming-leaderboard
2️⃣ Start all services
docker-compose up --build

This will:
- Build backend image
- Start MySQL container
- Start Redis container
- Initialize database schema
- Create persistent volume
- Start backend API
- Start frontend

**🌍Access the Application**
Backend API:
http://localhost:8001

Swagger Docs:
http://localhost:8001/docs

Frontend:
http://localhost:5500

🛑 Stop Containers
docker-compose down

🔄 Reset Database (Remove Volume)
docker-compose down -v


## ▶️ Project Setup (Commands)

```bash
1️⃣ Clone repository
git clone <repo-url>
cd gaming-leaderboard
2️⃣ Create virtual environment
python -m venv venv
3️⃣ Activate virtual environment (Windows)
venv\Scripts\activate
4️⃣ Install dependencies
pip install -r requirements.txt
5️⃣ Setup MySQL database
mysql -u root -p < schema.sql
6️⃣ Create environment file .env
env (# Database Configuration -DB_USER DB_PASS DB_HOST DB_PORT DB_NAME
# Redis Configuration REDIS_HOST REDIS_PORT REDIS_DB REDIS_PASSWORD)
7️⃣ Run Redis using Docker
docker run -d --name redis-local -p 6379:6379 redis:7
8️⃣ Verify Redis
docker exec -it redis-local redis-cli
PING, KEYS *
TTL leaderboard:top:10:0, GET leaderboard:rank:102
9️⃣ Start backend server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
API:
http://127.0.0.1:8001
Swagger Docs:
http://127.0.0.1:8001/docs
🔟 Run frontend
cd frontend
python -m http.server 5500
Open browser - http://localhost:5500/index.html
