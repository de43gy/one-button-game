# Project Canvas: Godot-Telegram Mini App Game Prototype

## 1. Project Title & Overview
**Title:** Godot-Telegram Mini App Game Prototype  
**Description:** A client-server game where players click a button to increment a counter, synced with a server for persistence. Includes a leaderboard showing top 5 players by click percentage, with player's position and neighbors. Integrated as Telegram Mini App.  
**Goal:** Test Godot 4.5 integration with Telegram Mini Apps and build a basic multiplayer client-server setup.  
**Status:** Planning Phase - Focus on deployment for early testing.

## 2. Key Features & Scope
**Core Features:**  
- Godot client: Button, click counter, leaderboard display.  
- Server: Click syncing, leaderboard calculation (percentage of total clicks).  
- Onboarding: Prompt for game name on first play (no real usernames).  
- Leaderboard: Top 5; show player's position below with neighbors (skip upper if in top 5).  
- Persistence: Resume clicks from previous sessions.  
**In Scope:**  
- Containerized deployment (Docker Compose: client, backend, DB).  
- GitHub Actions deployment (copy files only, no repo clone; .env from secrets/variables).  
- Godot 4.5 compatibility checks.  
**Out of Scope:**  
- Advanced scaling, mobile optimizations beyond basics.  
- Real-time multiplayer beyond syncing.

## 3. Stakeholders & Target Audience
**Primary Stakeholders:**  
- Developer (you): Testing integration and prototyping.  
**Target Audience:**  
- Experienced developers interested in Godot-Telegram setups.  
**Assumptions:**  
- Users have Telegram; developers know basics (Git, Docker).

## 4. Technical Stack & Architecture
**Client:** Godot 4.5 (GDScript) - UI scenes/scripts for game logic.  
**Backend:** Python 3.10+ with FastAPI - REST API for syncing and leaderboards.
- **Framework:** FastAPI 0.104+ (async web framework)
- **ORM:** SQLAlchemy 2.0+ with asyncpg driver
- **Validation:** Pydantic v2 (built into FastAPI)
- **Telegram:** python-telegram-bot 20.0+ (Bot API integration)
- **Server:** Uvicorn (ASGI server)
- **Additional:** aioredis (optional caching), python-multipart (file uploads)

**Database:** PostgreSQL 16 - Store users, clicks, global stats.  
**Infrastructure:** Docker Compose, GitHub Actions (SSH for file copy).  
**Architecture Overview:**  
- Client in Telegram Mini App communicates with backend REST API (JSON over HTTPS).  
- Backend validates Telegram initData, processes requests asynchronously.
- Data Models:
  - Users (id, telegram_id, game_name, clicks, created_at)
  - GlobalStats (total_clicks, total_users, last_updated)
- API Endpoints:
  - POST /api/clicks - Sync user clicks
  - GET /api/leaderboard?user_id={id} - Fetch leaderboard with user position
  - POST /api/users - Create/update user (onboarding)
  - GET /api/user/{id} - Get user profile
- File Structure: 
  ```
  client/          # Godot project
  backend/         # FastAPI application
    ├── app/
    │   ├── main.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── database.py
    │   ├── api/
    │   └── telegram/
    ├── requirements.txt
    └── Dockerfile
  database/        # PostgreSQL init scripts
  docker-compose.yml
  .env.example
  local_docs/
  ```

## 5. Development Guidelines
**Code Quality:**  
- Self-documenting code; minimal English comments for non-obvious logic.  
- DRY principle; small functions; docstrings (Python: Google-style docstrings).  
- Error handling: Logs, retries, save partial data; FastAPI exception handlers.  
- Security: No commits of .env/sessions; use GitHub Secrets; validate Telegram initData with HMAC-SHA256.  
- Type hints: Use Python type annotations throughout backend code.
**Documentation:**  
- README.md: Concise for pros (features, quick start, deployment, API endpoints).  
- local_docs/: development-plan.md (roadmap), IDEAS.md (features), api-spec.md (endpoint documentation).  
- Update triggers: After phases/features, keep up-to-date.  
**Git Workflow:** Conventional commits (feat:, fix:); test before commit.

## 6. Resources & Environment
**Required Tools:**  
- Godot 4.5, Python 3.10+, PostgreSQL 16, Docker, Docker Compose.
- Development: pip/venv, Postman/curl (API testing).

**Python Dependencies (requirements.txt):**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-telegram-bot==20.7
python-multipart==0.0.6
aioredis==2.0.1
```

**Environment Variables (.env):**  
- TELEGRAM_BOT_TOKEN (secret) - Telegram Bot API token
- DB_PASSWORD (secret) - PostgreSQL password
- SSH_KEY (secret) - Deployment SSH key
- DATABASE_URL - PostgreSQL connection string (auto-generated: `postgresql+asyncpg://user:password@db:5432/gamedb`)
- Non-secrets: DB_USER, DB_NAME, SERVER_HOST, API_PORT (from GitHub Variables).

**Deployment:**  
- Priority: Setup first for server testing.  
- GitHub Actions: Build Docker images, SSH copy files, generate .env, run docker-compose up.
- Backend runs on port 8000 (uvicorn), exposed via reverse proxy (optional: nginx).

## 7. Milestones & Roadmap
**Phase 1: Deployment & Setup** (Priority)  
- Docker Compose setup (backend + PostgreSQL + client serving).  
- FastAPI project structure with database models.
- GitHub Actions deployment workflow.  
- Basic Godot client with HTTPRequest integration.
- Health check endpoint (/health).

**Phase 2: Game Logic**  
- Telegram Mini App integration (initData validation).  
- Click syncing endpoint with conflict resolution.
- Leaderboard calculation (percentage-based ranking).
- User onboarding flow (game name input).

**Phase 3: Enhancements**  
- Leaderboard neighbor display logic.
- Caching layer (Redis) for leaderboard queries.
- Rate limiting (prevent click spam).
- Error recovery and retry logic in client.

**Timeline:** Start with deployment; iterative development.

## 8. Risks & Mitigations
**Risks:**  
- Godot 4.5 incompatibilities: Check against docs, update code.  
- Telegram API limits: Exponential backoff, error handling in python-telegram-bot.  
- Deployment issues: Test SSH/file copy locally.
- Database connection pool exhaustion: Configure SQLAlchemy pool size, use connection timeouts.
- FastAPI async pitfalls: Avoid blocking operations in async routes, use background tasks for heavy processing.

**Mitigations:**  
- Early testing on server.  
- Batch operations for performance (bulk updates).  
- Data integrity: No deletions, duplicate checks, database constraints.
- Use FastAPI dependency injection for database sessions (proper cleanup).
- Implement request timeout limits and payload size restrictions.

## 9. Success Metrics & Notes
**Metrics:**  
- Successful deployment & game run in Telegram.  
- Accurate syncing/leaderboards (< 1s response time).
- API uptime > 99% during testing phase.
- Zero data loss on server restarts (persistence validation).

**Notes:**  
- License: MIT.  
- Data Integrity: Preserve all clicks; use database transactions.
- API Documentation: Auto-generated at /docs (Swagger UI) and /redoc.
- Logging: Structured JSON logs for production debugging.
- Last Updated: October 22, 2025.  