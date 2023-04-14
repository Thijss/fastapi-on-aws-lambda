"""Test the items router."""
# pylint: disable=missing-function-docstring
import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


_ITEMS_URL = "items/"


def test_get_items_no_api_key():
    response = client.get(_ITEMS_URL)
    assert response.status_code == 403


def test_get_items_unauthorized():
    headers = {"ApiKey": "NOT READ"}

    response = client.get(_ITEMS_URL, headers=headers)
    assert response.status_code == 401


def test_get_items_authorized():
    headers = {"ApiKey": "READ"}

    with patch.dict(os.environ, {"api_key_read_access": "READ"}):
        response = client.get(_ITEMS_URL, headers=headers)
    assert response.status_code == 200
