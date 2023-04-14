"""Item model."""
from pydantic import BaseModel


class Item(BaseModel):
    """Item model."""

    name: str
    description: str
