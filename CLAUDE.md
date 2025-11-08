# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a modern FastAPI RESTful API project template with clean architecture patterns. It features async/await database operations using SQLAlchemy and aiosqlite, with a clear separation of concerns across models, schemas, CRUD operations, and API endpoints.

## Architecture

### Layered Structure

The project follows a classic layered architecture:

1. **Models** (`app/models/`): SQLAlchemy ORM models for database entities
   - `base.py`: Base model class with common fields
   - `user.py` & `item.py`: Specific domain models

2. **Schemas** (`app/schemas/`): Pydantic models for request/response validation
   - `user.py` & `item.py`: Data validation schemas
   - `response.py`: Standardized API response format

3. **CRUD** (`app/crud/`): Database access layer
   - `user.py` & `item.py`: Create, Read, Update, Delete operations
   - Contains business logic for database interactions

4. **API** (`app/api/`): REST endpoint definitions
   - `v1/endpoints/`: Route handlers for each domain
   - `v1/api.py`: Route aggregation and prefix configuration

5. **Core** (`app/core/`): Infrastructure components
   - `config.py`: Application settings using pydantic-settings
   - `exceptions.py`: Custom exception classes (BusinessException, NotFoundException, UnauthorizedException)

### Database

- **Async/SQLite**: Uses SQLAlchemy async engine with aiosqlite
- **Session Management**: `AsyncSessionLocal` factory in `app/database.py`
- **Dependency**: `get_db()` function provides database sessions to route handlers
- **Startup**: Tables are created automatically in `app/main.py` startup event

### Exception Handling

Three-tier exception handling in `app/main.py`:
1. `BusinessException` → Returns 200 with error code (for business logic errors)
2. `HTTPException` → Returns actual HTTP status code
3. Generic `Exception` → Returns 500 with internal error details (more verbose in DEBUG mode)

## Common Development Commands

### Running the Application

```bash
# Development mode with auto-reload
python run.py
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest test_database.py

# Run with verbose output
pytest -v

# Run async database test
pytest test_async_database.py
```

### Database Testing

```bash
# Test database CRUD operations
python test_database.py

# Test async database operations
python test_async_database.py
```

### Docker

```bash
# Build image
docker build -t fastapi-demo .

# Run with Docker Compose (includes database)
docker-compose up -d

# Run container directly
docker run -p 8000:8000 fastapi-demo
```

### Dependencies

```bash
# Install dependencies
pip install -r requirements.txt

# Using UV package manager (recommended for this project)
uv pip install -r requirements.txt
```

## Configuration

Configuration is managed through `app/core/config.py` using pydantic-settings. Key settings:

- **Database**: `DATABASE_URL` (defaults to SQLite at `sqlite:///./app.db`)
- **API**: `API_V1_STR` (prefix for all API routes, default: `/api/v1`)
- **CORS**: `ALLOWED_ORIGINS` (configurable list)
- **JWT**: `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- **Environment**: `DEBUG`, `ENVIRONMENT` (development/production)

Environment variables are loaded from `.env` file. See `.env.example` for all available options.

## API Endpoints

All endpoints are prefixed with `/api/v1`:

- **Users** (`/api/v1/users`):
  - `GET /` - List users (with pagination)
  - `GET /{user_id}` - Get single user
  - `POST /` - Create user
  - `PUT /{user_id}` - Update user
  - `DELETE /{user_id}` - Delete user

- **Items** (`/api/v1/items`):
  - `GET /` - List items (with pagination)
  - `GET /{item_id}` - Get single item
  - `POST /` - Create item
  - `PUT /{item_id}` - Update item
  - `DELETE /{item_id}` - Delete item

- **Utility**:
  - `GET /` - Root endpoint with welcome message
  - `GET /health` - Health check endpoint
  - `GET /docs` - Swagger UI documentation
  - `GET /redoc` - ReDoc documentation

## Development Workflow

### Adding a New API Resource

1. Create model in `app/models/{resource}.py` (inherits from `Base`)
2. Create schema in `app/schemas/{resource}.py` (Pydantic models)
3. Create CRUD operations in `app/crud/{resource}.py`
4. Create endpoints in `app/api/v1/endpoints/{resource}.py`
5. Register router in `app/api/v1/api.py`
6. Add tests in appropriate test file

### Database Migrations

Currently, tables are auto-created at startup. For production use with schema changes, integrate Alembic:

```bash
# Initialize migrations (if not already done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Key Files

- `app/main.py`: Application factory, middleware, exception handlers, route registration
- `app/database.py`: Database engine, sessions, table creation
- `app/core/config.py`: Application configuration
- `run.py`: Production-ready server launcher
- `pyproject.toml`: Python project configuration (uses modern packaging)

## Database Model Relationships

- `User` and `Item` models are independent (no foreign key relationship shown in code)
- `User` model includes password hashing capability in CRUD layer
- Both models have standard audit fields (id, created_at, updated_at via Base)

## Notes

- **Async/Await**: All database operations are async using SQLAlchemy 2.0 style
- **Validation**: Pydantic v2 is used with strict type validation
- **Security**: JWT token support is configured but not fully implemented in routes
- **Documentation**: Auto-generated OpenAPI docs at `/docs` and `/redoc`
- **Python Version**: Requires Python 3.11+ (as specified in pyproject.toml)
