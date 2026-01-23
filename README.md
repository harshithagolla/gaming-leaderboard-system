# 🎮 Gaming Leaderboard System

A backend system for managing a gaming leaderboard with real-time ranking, pagination, and Redis caching.

Built to demonstrate backend engineering concepts such as database design, caching strategies, cache invalidation, and Docker-based infrastructure.

---

## ✨ Features

- Submit player scores
- Auto-create users on first submission
- Maintain cumulative leaderboard
- Store individual game sessions
- Fetch top players (paginated)
- Fetch individual user rank
- Redis caching for read-heavy APIs
- Cache invalidation on score updates
- Graceful fallback when Redis is unavailable

---

## 🛠 Technologies Used

### Backend
- Python 3.10
- FastAPI
- SQLAlchemy
- PyMySQL
- Uvicorn

### Database
- MySQL

### Caching
- Redis

### Infrastructure
- Docker (Redis container)

### Frontend
- HTML, CSS
- Vanilla JavaScript (Fetch API)

---

## 📌 API Endpoints

- `POST /api/leaderboard/submit`
- `GET /api/leaderboard/top?limit=10&offset=0`
- `GET /api/leaderboard/rank/{user_id}`

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
env
7️⃣ Run Redis using Docker
docker run -d --name redis-local -p 6379:6379 redis:7
8️⃣ Verify Redis
docker exec -it redis-local redis-cli
PING
KEYS *
TTL leaderboard:top:10:0
GET leaderboard:rank:102
9️⃣ Start backend server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
API:
http://127.0.0.1:8000
Swagger Docs:
http://127.0.0.1:8000/docs
🔟 Run frontend
cd frontend
python -m http.server 5500
Open browser:
http://localhost:5500/index.html
