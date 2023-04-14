"""Repository settings."""
import os
from enum import Enum
from functools import lru_cache

from pydantic import BaseSettings


class S3Access(Enum):
    """S3 access."""

    NO_ACCESS = "no_access"
    READ = "read"
    WRITE = "write"


class RepositorySettings(BaseSettings):
    """Repository settings."""

    def __str__(self):
        setting_list = [f"[Settings parameter] {key}: {value}" for key, value in sorted(self.dict().items())]
        lines = ["---------- SETTINGS ----------"] + setting_list
        return os.linesep.join(lines)

    local_assets_dir: str = "assets"
    s3_assets_dir: str = "assets"
    s3_access: S3Access = S3Access.NO_ACCESS
    s3_bucket_name: str = ""

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_prefix = ""
        env_file_encoding = "utf-8"


def get_repo_settings() -> RepositorySettings:
    """Get repository settings."""
    if os.getenv("CACHE_SETTINGS"):
        return _get_cached_settings()
    return RepositorySettings()


@lru_cache()
def _get_cached_settings():
    return RepositorySettings()
