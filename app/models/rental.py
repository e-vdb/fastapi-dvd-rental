"""
Models for the endpoints input and responses.
"""

from pydantic import BaseModel
from datetime import datetime

class RentalOutput(BaseModel):

    rental_date: datetime
    title: str


class RentalFilmCountOutput(BaseModel):
    title: str
    count: int
