"""API settings."""
import os
from enum import Enum
from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, SecretStr


class HttpMethod(Enum):
    """HTTP methods."""

    ALL = "*"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


class ApiSettings(BaseSettings):
    """API settings."""

    def __str__(self):
        setting_list = [f"[Settings parameter] {key}: {value}" for key, value in sorted(self.dict().items())]
        lines = ["---------- SETTINGS ----------"] + setting_list
        return os.linesep.join(lines)

    project_name: str = "My API"
    debug: bool = False

    local_assets_dir: str = "assets"

    api_key_read_access: SecretStr = SecretStr("")
    api_key_write_access: SecretStr = SecretStr("")

    http_allowed_methods: list[str] = []
    http_allowed_headers: list[str] = []
    http_allowed_origins: list[str] = []

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            """Parse environment variables."""
            if field_name in [
                "http_allowed_methods",
                "http_allowed_headers",
                "http_allowed_origins",
            ]:
                raw_val = [(x.strip()) for x in raw_val.split(",")]
                if field_name == "http_allowed_methods":
                    return [HttpMethod(x).value for x in raw_val]
                return raw_val
            # pylint: disable=no-member
            return cls.json_loads(raw_val)


def get_api_settings():
    """Get API settings."""
    if os.getenv("CACHE_SETTINGS"):
        return _get_cached_settings()
    return ApiSettings()


@lru_cache()
def _get_cached_settings():
    return ApiSettings()
