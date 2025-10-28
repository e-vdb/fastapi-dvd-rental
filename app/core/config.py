"""Configuration for the application."""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Config class for the api."""

    app_name: str = "FastAPIProjectWithDVDRental"
    debug: bool = False
    db_user: str = "guest"
    db_password: str = ""
    db_name: str = "dvdrental"
    db_host: str = "localhost"
    db_port: str = "5432"

    # auth0 settings
    auth0_domain: str = "mydomain"
    auth0_api_audience: str = "myapi"
    auth0_issuer: str = "https://mydomain.auth0.com"
    auth0_algorithms: str = "RS256"

    # Testing configuration
    testing: bool = False
    test_db_url: str | None = None

    @property
    def db_url(self) -> str:
        """Return the database URL."""
        if self.testing and self.test_db_url:
            return self.test_db_url
        password_part = f":{self.db_password}" if self.db_password else ""
        return (
            f"postgresql://{self.db_user}{password_part}@{self.db_host}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Config:
    """Return the settings."""
    return Config()
