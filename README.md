# Fastapi with dvd-rental database

[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/release/python-3120/)


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

## Authentication

The application uses Auth0 for authentication. The token is verified using the PyJWT library. The token is passed in the Authorization header as a Bearer token.

## References
- [Postgres Tutorial](https://neon.com/postgresql/tutorial)
- [SQLalchemy intro](https://www.youtube.com/watch?v=aAy-B6KPld8&list=WL&index=23)
- [Scalable fastapi tuto](https://github.com/ArjanCodes/examples/tree/main/2025/project)
- [Build and Secure a FastAPI Server with Auth0](https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/)
