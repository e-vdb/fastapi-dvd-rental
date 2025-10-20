"""Configuration for the application."""
from __future__ import annotations

from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    """Config class for the api."""

    app_name: str = "FastAPIProjectWithDVDRental"
    debug: bool = False
    db_user: str = getenv("USERNAME", "guest")
    db_name: str = "dvdrental"
    db_host: str = "localhost"

    # auth0 settings
    auth0_domain: str = getenv("AUTH0_DOMAIN", "mydomain")
    auth0_api_audience: str = getenv("AUTH0_API_AUDIENCE", "myapi")
    auth0_issuer: str = getenv("AUTH0_ISSUER", "https://mydomain.auth0.com")
    auth0_algorithms: str = getenv("AUTH0_ALGORITHMS", "RS256")

    # Testing configuration
    testing: bool = False
    test_db_url: str | None = None

    @property
    def db_url(self) -> str:
        """Return the database URL."""
        if self.testing and self.test_db_url:
            return self.test_db_url
        return f"postgresql://{self.db_user}@{self.db_host}/{self.db_name}"


@lru_cache
def get_settings() -> Config:
    """Return the settings."""
    return Config()
