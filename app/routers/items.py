"""Items router."""
from fastapi import APIRouter, Depends
from starlette import status

from app.auth import api_key_read_access_auth, api_key_write_access_auth
from app.models.items import Item

router = APIRouter()


@router.get("", dependencies=[Depends(api_key_read_access_auth)])
async def get_items() -> list[Item]:
    """Get all items."""
    return [
        Item(name="Item no. 1", description="First item"),
        Item(name="Item no. 2", description="Second item"),
    ]


@router.post(
    "",
    dependencies=[Depends(api_key_write_access_auth)],
    status_code=status.HTTP_201_CREATED,
)
async def add_item(name: str, description: str) -> Item:
    """Add an item."""
    return Item(name=name, description=description)
