"""Base class for repositories"""
import json
from abc import ABC
from pathlib import Path, PosixPath
from typing import Optional

from pydantic import BaseModel

from app.repositories._validators import assert_in
from app.s3 import S3AssetBucket
from app.settings.repository import RepositorySettings, S3Access, get_repo_settings
from app.utils import BASE_DIR


class JsonRepository(BaseModel, ABC):
    """Base class for repositories that store data in json files"""

    assets: list[BaseModel] = []

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic config"""

        json_file_name: PosixPath

    def add(self, asset: BaseModel, validators: Optional[list[callable]] = None):
        """Add asset to repository"""
        validators = validators or []

        for validator in validators:
            validator(self, asset)
        self.assets.append(asset)
        self.save()

    def remove(self, asset: BaseModel, validators: Optional[list[callable]] = None):
        """Remove asset from repository"""
        validators = validators or []
        validators.append(assert_in)
        for validator in validators:
            validator(self, asset)

        self.assets.remove(asset)
        self.save()

    @classmethod
    def load(cls, refresh: bool = False):
        """Load model from json"""
        repo = cls()
        if (refresh or not repo.json_exists()) and get_repo_settings().s3_access in [
            S3Access.WRITE,
            S3Access.READ,
        ]:
            repo._download(settings=get_repo_settings())

        if repo.json_exists():
            json_data = repo._read_json_data()
            return cls(**json_data)
        return cls()

    def save(self):
        """Save model to json"""
        self._write_json_data()
        settings = get_repo_settings()
        if settings.s3_access is S3Access.WRITE:
            self._upload(settings)

    def _read_json_data(self):
        with open(self.local_json_file, "r", encoding="utf-8") as infile:
            return json.load(infile)

    def _write_json_data(self):
        self.local_json_file.touch(exist_ok=True)
        with open(self.local_json_file, "w", encoding="utf-8") as outfile:
            outfile.write(self.json(indent=4))

    def _upload(self, settings: RepositorySettings):
        s3_bucket = S3AssetBucket(bucket_name=settings.s3_bucket_name)
        s3_bucket.upload_asset(self.Config.json_file_name)

    def _download(self, settings: RepositorySettings):
        s3_bucket = S3AssetBucket(bucket_name=settings.s3_bucket_name)
        s3_bucket.download_asset(self.Config.json_file_name)

    def json_exists(self):
        """Check if json file exists"""
        return Path(self.local_json_file).exists()

    @property
    def local_json_file(self) -> Path:
        """Get local json file path"""
        settings = get_repo_settings()
        return BASE_DIR / settings.local_assets_dir / self.Config.json_file_name
