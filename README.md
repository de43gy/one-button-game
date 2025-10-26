# Godot-Telegram Mini App Game Prototype

A click-counter game built with Godot 4.5.1 and integrated as a Telegram Mini App. Features server-side persistence, percentage-based leaderboards, and containerized deployment.

## Features

- **One-Button Gameplay** - Click to increment counter with server sync
- **Telegram Integration** - Native Mini App with initData authentication
- **Percentage Leaderboards** - Top 5 players + user position with neighbors
- **Session Persistence** - Resume clicks across sessions
- **Docker Deployment** - Single-command containerized setup
- **FastAPI Backend** - Async Python REST API with PostgreSQL
- **Real-time Updates** - Efficient click syncing and leaderboard refresh

## Tech Stack

- **Client:** Godot 4.5.1 (GDScript)
- **Backend:** Python 3.10+ with FastAPI, SQLAlchemy, asyncpg
- **Database:** PostgreSQL 16
- **Infrastructure:** Docker Compose, GitHub Actions
- **Authentication:** Telegram Bot API (HMAC-SHA256 validation)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Telegram Bot Token (via [@BotFather](https://t.me/botfather))
- Python 3.10+ (for local development)
- Godot 4.5.1 (for client development)

### Local Development

1. **Clone and setup environment:**
```bash
git clone <repository-url>
cd one-button-game
cp .env.example .env
# Edit .env with your Telegram bot token and database credentials
```

2. **Start services:**
```bash
docker-compose up -d
```

3. **Verify health:**
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","timestamp":"...","version":"1.0.0"}
```

4. **Access API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Environment Variables

Create `.env` from `.env.example`:

```env
# Secrets (GitHub Secrets in production)
TELEGRAM_BOT_TOKEN=your_bot_token_here
DB_PASSWORD=secure_password_here

# Configuration (GitHub Variables)
DB_USER=gameuser
DB_NAME=gamedb
SERVER_HOST=0.0.0.0
API_PORT=8000
```

## Project Structure

```
.
├── client/               # Godot 4.5.1 project
│   ├── scenes/          # UI scenes
│   └── scripts/         # GDScript logic
├── backend/             # FastAPI application
│   ├── app/
│   │   ├── main.py      # Entry point
│   │   ├── models.py    # SQLAlchemy models
│   │   ├── schemas.py   # Pydantic schemas
│   │   ├── database.py  # DB connection
│   │   ├── api/         # API routes
│   │   └── telegram/    # Telegram integration
│   ├── requirements.txt
│   └── Dockerfile
├── database/            # PostgreSQL init scripts
├── local_docs/          # Development documentation
│   ├── development-plan.md
│   ├── IDEAS.md
│   └── api-spec.md
├── docker-compose.yml
├── .env.example
├── CLAUDE.md           # Project canvas
└── README.md
```

## API Endpoints

### Health Check
```http
GET /health
```

### User Management
```http
POST /api/users          # Create/update user (onboarding)
GET /api/user/{id}       # Get user profile
```

### Click Syncing
```http
POST /api/clicks         # Sync user clicks (max 10/min)
```

### Leaderboard
```http
GET /api/leaderboard?user_id={id}  # Top 5 + user position + neighbors
```

**Full API documentation:** See [local_docs/api-spec.md](local_docs/api-spec.md)

## Deployment

### GitHub Actions (Production)

1. **Configure secrets** in repository settings:
   - `TELEGRAM_BOT_TOKEN`
   - `DB_PASSWORD`
   - `SSH_KEY` (for server deployment)

2. **Set variables:**
   - `DB_USER`, `DB_NAME`, `SERVER_HOST`, `API_PORT`

3. **Push to main branch** - auto-deploys via GitHub Actions

### Manual Deployment

```bash
# On server
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f backend

# Database migrations (if needed)
docker-compose exec backend alembic upgrade head
```

## Development

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Client Setup
1. Open `client/` in Godot 4.5.1
2. Configure API base URL in project settings
3. Run scene: `scenes/main.tscn`

### Testing
```bash
# Backend tests
cd backend
pytest

# API manual testing
curl -X POST http://localhost:8000/api/clicks \
  -H "Authorization: tma <initDataString>" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"uuid","clicks":100,"timestamp":"2025-10-22T12:00:00Z"}'
```

## Roadmap

**Phase 1 (Current):** Deployment & Infrastructure
- [x] Docker Compose setup
- [ ] GitHub Actions deployment
- [ ] Basic Godot client
- [ ] Health check endpoint

**Phase 2:** Core Game Logic
- [ ] Telegram Mini App integration
- [ ] Click syncing with conflict resolution
- [ ] Leaderboard calculation
- [ ] User onboarding flow

**Phase 3:** Enhancements
- [ ] Neighbor display logic
- [ ] Redis caching layer
- [ ] Rate limiting
- [ ] Error recovery

See [local_docs/development-plan.md](local_docs/development-plan.md) for details.

## Contributing

1. Follow [Conventional Commits](https://www.conventionalcommits.org/)
2. Test locally before push
3. Update documentation for new features
4. No commits of `.env` or session files

## Security

- **Authentication:** All API requests validate Telegram initData
- **Rate Limiting:** 10 clicks/min, 30 leaderboard req/min
- **Data Integrity:** Server-authoritative click counts
- **Secrets Management:** GitHub Secrets for production

## License

MIT License - See LICENSE file for details

## Support

- **Documentation:** See `local_docs/` for detailed specs
- **Issues:** Open GitHub issue for bugs/features
- **API Docs:** `/docs` endpoint (Swagger UI)

## Acknowledgments

Built with Godot 4.5.1, FastAPI, and Telegram Bot API.

---

**Status:** Planning Phase
**Last Updated:** 2025-10-22
**Version:** 1.0.0
