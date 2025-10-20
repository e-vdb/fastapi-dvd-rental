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

## Get started

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

## References
- [fastapi](https://fastapi.tiangolo.com/)
- [Postgres Tutorial](https://neon.com/postgresql/tutorial)
- [SQLalchemy intro](https://www.youtube.com/watch?v=aAy-B6KPld8&list=WL&index=23)
- [Scalable fastapi tuto](https://github.com/ArjanCodes/examples/tree/main/2025/project)
- [Build and Secure a FastAPI Server with Auth0](https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/)
- [auth0-python-fastapi-sample](https://github.com/auth0-blog/auth0-python-fastapi-sample)
- [JSON Web Token (JWT) Debugger](https://www.jwt.io/#libraries)
