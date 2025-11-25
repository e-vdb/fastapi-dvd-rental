"""Customer models."""

from pydantic import BaseModel, ConfigDict


class CustomerOutput(BaseModel):
    """Model for customer."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    customer_id: int
    first_name: str
    last_name: str
    store_id: int
