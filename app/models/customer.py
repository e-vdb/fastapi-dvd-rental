"""Customer models."""

from pydantic import BaseModel


class CustomerOutput(BaseModel):
    """Model for customer."""

    customer_id: int
    first_name: str
    last_name: str
    store_id: int
