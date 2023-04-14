"""Test items repository."""
# pylint: disable=missing-function-docstring
from unittest.mock import patch

import pytest

from app.models.items import Item
from app.repositories.items import ItemRepository
from app.settings.repository import RepositorySettings
from app.utils import BASE_DIR


@pytest.fixture(name="repo")
def fixture_repo():
    return ItemRepository()


@pytest.fixture(name="asset")
def fixtrue_asset():
    return Item(name="test", description="test")


def test_add(repo, asset):
    with patch.object(ItemRepository, "save"):
        repo.add(asset)
    assert len(repo.assets) == 1
    assert repo.assets[0].dict() == asset


def test_remove(repo, asset):
    with patch.object(ItemRepository, "save"):
        repo.add(asset)
        repo.remove(asset)
    assert len(repo.assets) == 0


def test_load(repo):
    with patch.object(ItemRepository, "_download") as mock_download:
        loaded_repo = repo.load()
    assert len(loaded_repo.assets) == 0
    assert not mock_download.called


def test_save(repo):
    with patch.object(ItemRepository, "_upload") as mock_upload:
        with patch.object(ItemRepository, "_write_json_data") as mock_write_json_data:
            repo.save()
    assert mock_write_json_data.called
    assert not mock_upload.called


def test_local_json_file(repo):
    settings = RepositorySettings(local_assets_dir="test_dir")
    with patch("app.repositories._base.get_repo_settings", return_value=settings):
        assert str(repo.local_json_file) == f"{BASE_DIR}/test_dir/{repo.Config.json_file_name}"
