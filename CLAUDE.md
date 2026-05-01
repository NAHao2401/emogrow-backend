# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development commands

This repository is a small FastAPI backend without a build system, test suite, formatter config, or migration tool checked in.

### Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### Run the app

```powershell
uvicorn app.main:app --reload
```

App URLs when running locally:
- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Environment variables

Expected in `.env` via `app/core/config.py`:
- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM` (defaults to `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (defaults to `60`)

The example project setup expects PostgreSQL.

### Tests

No test files or test runner configuration are present in the repository right now. If tests are added later, document the exact commands here.

## High-level architecture

This is a layered FastAPI application for authentication and child profile management.

### Request flow

Typical request flow is:
1. Route handlers in `app/api/*.py` define endpoints and inject dependencies.
2. Dependencies in `app/api/deps.py` provide a SQLAlchemy session and authenticated user.
3. Business logic lives in `app/services/*.py`.
4. SQLAlchemy models in `app/models/*.py` persist data.
5. Pydantic schemas in `app/schemas/*.py` define request and response shapes.
6. Shared exception handling in `app/core/error_handler.py` converts domain, validation, and database errors into a consistent JSON error format.

### Application bootstrap

`app/main.py` wires the application together:
- creates tables at startup with `Base.metadata.create_all(bind=engine)`
- registers global exception handlers
- mounts the auth and children routers

Because schema creation is done directly at startup, there is currently no migration system like Alembic in the repo. Model changes will be applied only for tables that can be created by SQLAlchemy, not managed through versioned migrations.

### API surface

Current routers:
- `app/api/auth.py` — register, login, and `/auth/me`
- `app/api/children.py` — CRUD-style endpoints for the authenticated user's child profiles
- `app/api/review.py` — emotion statistics endpoint (`GET /review/children/{child_id}/emotion-statistics`)

### Auth model

Authentication is JWT-based:
- password hashing and token encoding/decoding live in `app/core/security.py`
- `OAuth2PasswordBearer` is configured in `app/api/deps.py`
- authenticated routes depend on `get_current_user()`, which decodes the bearer token, extracts `sub`, and loads the user from the database

`login_user()` in `app/services/auth_service.py` puts `sub`, `email`, and `role` into the access token.

### Data model

The repo currently has four SQLAlchemy models:
- `User` in `app/models/user.py`
- `Child` in `app/models/child.py`
- `EmotionLog` in `app/models/review.py`
- `StickerCollection` in `app/models/review.py`

Relationship shape:
- one `User` owns many `Child` rows through `children.user_id -> users.user_id`
- one `Child` owns many `EmotionLog` rows through `emotion_logs.child_id -> children.child_id`
- one `Child` owns many `StickerCollection` rows through `sticker_collections.child_id -> children.child_id`
- ownership checks are enforced in service-layer queries, especially in `app/services/child_service.py` and `app/services/review_service.py`.

### Validation and error conventions

Validation is split across two layers:
- Pydantic field validation in `app/schemas/*.py`
- service-level business validation in `app/services/*` using custom exceptions from `app/core/exceptions.py`

Error responses are intentionally normalized to a JSON shape with fields like:
- `success`
- `message`
- `error_code`
- `details`

When changing API behavior, preserve that error response contract unless the user asks to redesign it.

## Important implementation notes

- Database sessions are synchronous SQLAlchemy sessions from `app/db/session.py`; the codebase is not using SQLAlchemy async APIs.
- The README shows a `postgresql+psycopg://...` URL, but `requirements.txt` currently includes `psycopg2-binary`, so verify driver compatibility before changing connection settings.
- `app/models` is imported in `app/main.py` only for model registration before `create_all()`. If new models are added, they must be imported there or through another import path that guarantees metadata registration before startup.
- The children endpoints are user-scoped by querying with both `child_id` and `current_user.user_id`; preserve that ownership filter when modifying retrieval or update logic.
