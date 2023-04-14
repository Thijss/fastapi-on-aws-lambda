"""Items router."""
from app.models.items import Item
from app.repositories._base import JsonRepository


class ItemRepository(JsonRepository):
    """Item repository."""

    assets: list[Item] = []

    # pylint: disable=too-few-public-methods
    class Config:
        """Item repository config."""

        json_file_name = "items.json"
