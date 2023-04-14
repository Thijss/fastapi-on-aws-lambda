"""Validators for repositories."""
from typing import TYPE_CHECKING

from astroid import NotFoundError
from pydantic import BaseModel

from app.exceptions import AlreadyExistsError

if TYPE_CHECKING:
    from ._base import JsonRepository


def assert_in(repo: "JsonRepository", asset: BaseModel):
    """Assert that an asset is in the repository."""
    if asset not in repo.assets:
        raise NotFoundError(f"{asset} does not exist")


def assert_not_in(repo: "JsonRepository", asset: BaseModel):
    """Assert that an asset is not in the repository."""
    if asset in repo.assets:
        raise AlreadyExistsError(f"{asset} already exists")
