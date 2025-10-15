"""Base repository module."""
# pylint: disable=too-few-public-methods

from sqlalchemy.orm import Session


class BaseRepository:
    """Base class to interact with database tables."""

    def __init__(self, db: Session) -> None:
        """Initialise the base repository service."""
        self.db = db
