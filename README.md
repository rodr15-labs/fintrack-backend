# 📘 FinTrack Backend Documentation

## 1. Overview

**FinTrack** is a RESTful API for personal finance management built with modern Python technologies.  
The platform allows users to:

- Register and manage financial transactions
- Track income and expenses
- Organize movements by categories
- Monitor personal financial activity securely and efficiently

The project is designed with scalability, maintainability, and clean architecture principles in mind.

---

## 2. Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.13+ | Main programming language |
| FastAPI | High-performance API framework |
| SQLAlchemy 2.0 | ORM using Declarative Mapping |
| PostgreSQL | Relational database |
| Alembic | Database migrations |
| Docker & Docker Compose | Containerized development environment |
| Ruff | Linting and code formatting |

---

## 3. Architecture Overview

The backend follows a layered and modular structure:

- **FastAPI** handles routing and request lifecycle
- **SQLAlchemy** manages database models and relationships
- **Pydantic Schemas** validate and serialize API data
- **Alembic** controls schema evolution and migrations
- **Docker** ensures consistent local development environments

### Database Relationship

The current database design includes a:

- **1:N relationship** between `User` and `Transaction`

Meaning:

- One user can have multiple transactions
- Each transaction belongs to exactly one user

---

## 4. Database Migrations (Alembic)

Alembic is configured to safely manage database schema changes across environments.

### Features

- Dynamic database configuration using `.env`
- Automatic model change detection via `Base.metadata`
- Version-controlled schema evolution

### Migration Configuration

Alembic reads the database URL dynamically from:

```bash
migrations/env.py
```

Model discovery is enabled through:

```python
target_metadata = Base.metadata
```

---

## 5. Common Alembic Commands

### Generate a Migration

After modifying SQLAlchemy models:

```bash
PYTHONPATH=. python -m alembic revision --autogenerate -m "description of change"
```

### Apply Latest Migrations

```bash
PYTHONPATH=. python -m alembic upgrade head
```

### Roll Back the Last Migration

```bash
PYTHONPATH=. python -m alembic downgrade -1
```

> ⚠️ Important: Ensure the PostgreSQL Docker container is running before executing migrations.

---

## 6. Project Structure

```plaintext
fintrack-backend/
│
├── app/
│   ├── db/
│   │   ├── base_class.py      # SQLAlchemy Base class
│   │   └── session.py         # Engine and SessionLocal configuration
│   │
│   ├── models/
│   │   ├── user.py            # User model
│   │   └── transaction.py     # Transaction model
│   │
│   ├── schemas/
│   │   └── transaction.py     # Pydantic schemas
│   │
│   └── api/                   # API routes (future)
│
├── migrations/                # Alembic migration versions
│
├── .env                       # Environment variables (ignored by Git)
├── alembic.ini                # Alembic configuration
├── docker-compose.yml         # Docker services
└── README.md
```

---

## 7. Current Data Model

### Transaction Model

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `amount` | Float | Transaction amount (required) |
| `description` | String | Optional description (max 255 chars) |
| `category` | String | Transaction category (indexed) |
| `user_id` | Integer | Foreign key referencing `users.id` |
| `date` | DateTime | Transaction date |

---

## 8. Development Workflow

### Start the Environment

```bash
docker compose up -d
```

### Run the API

```bash
uvicorn app.main:app --reload
```

### Code Quality

Run Ruff for linting and formatting:

```bash
ruff check .
ruff format .
```

---

## 9. Roadmap

### Planned Features

#### ✅ Transaction CRUD
- Create transactions
- Retrieve transaction history
- Update existing transactions
- Delete transactions

#### 🔐 Authentication & Authorization
- JWT-based authentication
- Protected endpoints
- User-specific data isolation

#### 🧠 Business Logic
- Financial validation rules
- Balance constraints
- Advanced reporting and analytics

#### 📊 Future Improvements
- Monthly summaries
- Budget tracking
- Category analytics
- Recurring transactions
- API rate limiting

---

## 10. Environment Variables

Example `.env` configuration:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fintrack
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/fintrack
```

---

## 11. Developer Notes

- Always keep migrations synchronized with SQLAlchemy models.
- Avoid editing migration files manually unless necessary.
- Use Docker to ensure environment consistency across machines.
- Follow clean architecture and separation of concerns principles.

---

## 12. Future API Example

Example transaction payload:

```json
{
  "amount": 120.50,
  "description": "Groceries",
  "category": "Food",
  "date": "2026-05-13T10:30:00"
}
```

---

# 🚀 FinTrack Goals

The long-term goal of FinTrack is to provide a secure, scalable, and developer-friendly financial management API that can evolve into a complete personal finance platform.