"""Utility functions regarding dates."""

from datetime import UTC, datetime


def get_today_with_custom_format() -> datetime:
    """Get today date formatted for the database.

    The format is:
    datetime.datetime(year, month, day, hour, minute, second)
    No timezone info in the datetime object.
    No milliseconds.

    Returns
    -------
    datetime:
        The current date and time formatted for the database

    """
    return datetime.now(tz=UTC).replace(tzinfo=None).replace(microsecond=0)
