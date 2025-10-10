"""Configuration for the application."""

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

    @property
    def db_url(self) -> str:
        """Return the database URL."""
        return f"postgresql://{self.db_user}@{self.db_host}/{self.db_name}"


config = Config()
