"""Unit tests for the API settings."""
# pylint: disable=missing-function-docstring
import os
from unittest.mock import patch

import pytest

from app.settings.api import ApiSettings


def test_allowed_http_methods():
    with patch.dict(os.environ, {"HTTP_ALLOWED_METHODS": "GET, POST"}):
        settings = ApiSettings()

    assert settings.http_allowed_methods == ["GET", "POST"]


def test_allowed_http_methods_with_spaces():
    with patch.dict(os.environ, {"HTTP_ALLOWED_METHODS": "GET    ,     POST   "}):
        settings = ApiSettings()

    assert settings.http_allowed_methods == ["GET", "POST"]


def test_invalid_allowed_http_methods():
    with patch.dict(os.environ, {"HTTP_ALLOWED_METHODS": "GET, POST, INVALID"}):
        with pytest.raises(ValueError):
            ApiSettings()
