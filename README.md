# 🔐 Authentication & Authorization Service

A production-ready Authentication and Authorization microservice built
with **FastAPI**, designed with security, scalability, and clean
architecture principles.

------------------------------------------------------------------------

##  Project Vision

This service provides:

-   JWT Access Tokens
-   Refresh Token Rotation
-   Role-Based Access Control (RBAC)
-   Account Lock Protection (Brute Force Mitigation)
-   Email Verification Flow (Mocked)
-   Password Reset Flow
-   Token Blacklisting
-   Structured Logging
-   Database Migrations (Alembic)
-   Docker-Ready Architecture

The goal is to simulate how a real authentication microservice would be
built in a professional backend environment.

------------------------------------------------------------------------

##  Architecture Overview

    authentication_authorization_service/
    │
    ├── app/
    │   ├── api/                 # Route definitions
    │   ├── core/                # Configuration & security utilities
    │   ├── models/              # SQLAlchemy ORM models
    │   ├── schemas/             # Pydantic schemas
    │   ├── services/            # Business logic layer
    │   ├── repositories/        # Database abstraction layer
    │   ├── db/                  # Database engine & session management
    │   └── main.py              # FastAPI entrypoint
    │
    ├── migrations/              # Alembic migration history
    ├── tests/                   # Unit & integration tests
    ├── .env.example             # Environment template
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md

### Architectural Principles

-   Separation of concerns
-   Service layer pattern
-   Repository abstraction
-   Stateless access tokens
-   Refresh token persistence
-   Explicit environment validation
-   Migration-driven database evolution

------------------------------------------------------------------------

##  Technology Stack

-   Python 3.11
-   FastAPI
-   SQLAlchemy 2.x
-   Pydantic v2 + pydantic-settings
-   Alembic
-   SQLite (development)
-   Docker (planned production setup)

------------------------------------------------------------------------

##  Security Design Decisions

This project follows secure authentication practices:

-   Passwords hashed using bcrypt
-   Refresh tokens hashed before storage
-   Access tokens are short-lived and stateless
-   Refresh tokens are stored and revocable
-   Brute-force protection with configurable lock duration
-   Generic login error responses to prevent user enumeration
-   Environment variables validated at startup
-   Token blacklisting for emergency invalidation

------------------------------------------------------------------------

##  Environment Configuration

All configuration is managed using **pydantic-settings**.

Required environment variables:

    APP_NAME=
    ENV=
    DEBUG=
    DATABASE_URL=
    JWT_SECRET=
    JWT_ALGORITHM=
    ACCESS_TOKEN_EXPIRE_MINUTES=
    REFRESH_TOKEN_EXPIRE_DAYS=
    MAX_LOGIN_ATTEMPTS=
    ACCOUNT_LOCK_MINUTES=

------------------------------------------------------------------------

##  Running the Project (Development)

### 1️⃣ Create Virtual Environment

``` bash
py -3.11 -m venv venv
venv\Scripts\activate
```

### 2️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment

Create a `.env` file based on `.env.example`.

### 4️⃣ Run the Server

``` bash
uvicorn app.main:app --reload
```

Server will start at:

http://127.0.0.1:8000

------------------------------------------------------------------------

## 🗃 Database & Migrations

This project uses **Alembic** for schema management.

Initialize migrations:

``` bash
alembic init migrations
```

Generate migration:

``` bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

``` bash
alembic upgrade head
```

Database changes are never applied manually.

------------------------------------------------------------------------

##  Development Roadmap

### Phase 0 --- Foundation

-   Project structure
-   Environment validation
-   Database engine
-   FastAPI bootstrap

### Phase 1 --- Database & Core Models

-   User model
-   Role model
-   Token models
-   Login attempt tracking
-   Alembic integration

### Phase 2 --- Security Utilities

-   Password hashing
-   JWT infrastructure
-   Token generation & validation

### Phase 3 --- Authentication Flows

-   Register
-   Login
-   Refresh
-   Logout
-   Account lock logic

### Phase 4 --- Authorization (RBAC)

-   Role-based guards
-   Admin-only routes

### Phase 5 --- Account Protection Features

-   Password reset
-   Email verification
-   Token rotation

### Phase 6 --- Production Hardening

-   Dockerization
-   Structured logging
-   Rate limiting
-   CI/CD readiness

------------------------------------------------------------------------

##  Purpose of This Project

-   Portfolio-grade backend microservice
-   Demonstration of security-aware backend engineering
-   Foundation for future distributed systems integration

------------------------------------------------------------------------

##  Future Enhancements

-   PostgreSQL support
-   Redis for token blacklisting
-   OAuth2 provider integration
-   Multi-factor authentication
-   Observability with structured JSON logs
-   Cloud deployment

------------------------------------------------------------------------

##  Author

Marcos Farid Salomón\
Backend Engineer (In Progress)

------------------------------------------------------------------------

⚠️ This project is designed for educational and portfolio purposes and
follows production patterns, but requires further hardening for
real-world deployment.
