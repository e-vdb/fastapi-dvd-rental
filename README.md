# Fastapi with dvd-rental database

[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/release/python-3120/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/ruff-0A8BFF.svg?logo=ruff)](https://github.com/astral-sh/ruff)
[![FastAPI](https://img.shields.io/badge/fastapi-0A8BFF.svg?logo=fastapi)](https://github.com/tiangolo/fastapi)
[![Auth0](https://img.shields.io/badge/auth0-0A8BFF.svg?logo=auth0)](https://auth0.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-0A8BFF.svg?logo=postgresql)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-0A8BFF.svg?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![PyJWT](https://img.shields.io/badge/pyjwt-0A8BFF.svg?logo=pyjwt)](https://github.com/jpadilla/pyjwt)
[![Pydantic](https://img.shields.io/badge/pydantic-0A8BFF.svg?logo=pydantic)](https://github.com/pydantic/pydantic)
![ci workflow](https://github.com/e-vdb/fastapi-dvd-rental/actions/workflows/ci.yml/badge.svg)

## Features

- 🔐 OAuth2 authentication with Auth0
- 🎭 Role-based access control (RBAC)
- 🧪 Comprehensive test coverage (70%+)
- 🚀 CI with GitHub Actions

## Get started

### Prerequisites

- Python 3.12
- PostgreSQL
- Auth0 account

### Set-up the database

- Download the dvdrental database zip folder (see tutorial [here](https://neon.com/postgresql/postgresql-getting-started/load-postgresql-sample-database))
- Unzip the folder to extract dvdrental.tar
- Import the dvdrental.tar file into your postgres database

```
psql -d postgres -c "CREATE DATABASE dvdrental;"

pg_restore --no-owner --no-privileges -d dvdrental dvdrental.tar
```

### Clone the repository

```
git clone https://github.com/e-vdb/fastapi-dvd-rental.git
cd fastapi-dvd-rental
```

### Install dependencies

```
uv sync --locked --all-extras --dev
```

### Commands

Run the application (development mode)

```
uv run fastapi dev app/app.py
```

Run unit tests

```
uv run pytest
```

Run unit tests with coverage

```
uv run pytest --cov=app
```

Run the application in container with docker compose
```
docker compose up --build
```
and stop with
```
docker compose down
```
## 📡 API Endpoints

### Health Check Endpoints

| Endpoint | Purpose | Use Case |
| -------- |---------|----------|
|GET /health |	Comprehensive health check |	Monitoring dashboards|
|GET /health/live |	Liveness probe |	|

Health Check Response Example

```json
{
   "status":"healthy",
   "timestamp":"2025-11-14T12:55:44.430744+00:00",
   "uptime_seconds":17.613036,
   "version":"1.0.0",
   "environment":"development",
   "checks": {
      "database": {
         "status":"healthy",
         "duration_ms":44.121742248535156,
         "error":null
      }
   }
}
```

## 🔍 Monitoring & Observability

### Structured Logging and request tracing middleware

We use `structlog` python library to log events using structured data and we log for each request the following:

- processing time
- status code

### Health Check Patterns

Two types of health checks have been implemented:

1. Comprehensive Check (/health)
   - Answers: "Is everything working optimally?"
   - Use for: Monitoring dashboards
2. Liveness Check (/health/live)
   - Answers: "Is the process running?"

### Metrics

Prometheus metrics endpoint can be accessed using

```bash
curl http://localhost:8000/metrics
```

## GitHub Actions

### Lint and test

The workflow is set up in `.github/workflows/ci.yml`.

## Experiment with postgres

Connect to postgres and select the dvdrental database
```
psql postgres

\c dvdrental
```

## Authentication

The application uses Auth0 for authentication. The token is verified using the PyJWT library. The token is passed in the Authorization header as a Bearer token.


## Layer flow

```
[Router] → [Service] → [Repository] → [DB]
                         ↑
                 [Pydantic Models]

```

| Layer                 | Purpose                                             | Example                                |
| --------------------- | --------------------------------------------------- |----------------------------------------|
| **Router**            | HTTP entrypoint, validation, response serialization | `/rentals/`, `/rentals/filter`         |
| **Service**           | Business logic, transactions, orchestration         | `RentalService.create_rental()`        |
| **Repository**        | Data access (SQLAlchemy queries)                    | `RentalRepository.create_rental_raw()` |
| **Models (Pydantic)** | Input/output schema                                 | `RentalFilters`, `RentalItem`          |
| **DB Layer**          | ORM mapping                                         | `Rental` SQLAlchemy model              |


## 🔒 Local HTTPS

### mkcert Configuration

To avoid certificate warnings in development:

1. **Install mkcert**
```bash
   # macOS
   brew install mkcert nss
   
   # Linux
   sudo apt install libnss3-tools
   wget -O mkcert https://github.com/FiloSottile/mkcert/releases/latest/download/mkcert-linux-amd64
   chmod +x mkcert
   sudo mv mkcert /usr/local/bin/
```

2. **Create local Certificate Authority**
```bash
   mkcert -install
```

3. **Generate certificates**
```bash
   ./scripts/setup-local-certs.sh
```

4. **Install CA on your devices**
   
   The CA file is located at: `$(mkcert -CAROOT)/rootCA.pem`
   
   **iPhone:**
   - Transfer `rootCA.pem` via AirDrop
   - Settings > General > VPN & Device Management > Install
   - Settings > General > About > Certificate Trust Settings > Enable
   
   **Android:**
   - Rename to `rootCA.crt`
   - Settings > Security > Install from storage

## 🏗️ Architecture
```
┌─────────────────────────────────────┐
│  Clients (Browser, Mobile)         │
└──────────────┬──────────────────────┘
               │ HTTPS
               ▼
┌─────────────────────────────────────┐
│  Nginx (Reverse Proxy)              │
│  - SSL termination                  │
│  - Port 443                         │
└──────────────┬──────────────────────┘
               │ HTTP
               ▼
┌─────────────────────────────────────┐
│  FastAPI                            │
│  - REST API                         │
│  - Port 8000                        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  PostgreSQL                         │
│  - Database                         │
│  - Port 5432 (internal)             │
└─────────────────────────────────────┘
```

## 📝 API Documentation

Once the application is running:
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

## References
- [fastapi](https://fastapi.tiangolo.com/)
- [Postgres Tutorial](https://neon.com/postgresql/tutorial)
- [SQLalchemy intro](https://www.youtube.com/watch?v=aAy-B6KPld8&list=WL&index=23)
- [Scalable fastapi tuto](https://github.com/ArjanCodes/examples/tree/main/2025/project)
- [Build and Secure a FastAPI Server with Auth0](https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/)
- [auth0-python-fastapi-sample](https://github.com/auth0-blog/auth0-python-fastapi-sample)
- [JSON Web Token (JWT) Debugger](https://www.jwt.io/#libraries)
- [Building a Health-Check Microservice with FastAPI ](https://dev.to/lisan_al_gaib/building-a-health-check-microservice-with-fastapi-26jo)
- [fastapi-microservice-health-check](https://github.com/DanielPopoola/fastapi-microservice-health-check)
- [homelab-certificats-https-ssl-mkcert](https://blog.stephane-robert.info/post/homelab-certificats-https-ssl-mkcert/)
- [Publishing Docker images](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images)
