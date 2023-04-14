"""Authentication and authorization for the API."""
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.settings.api import get_api_settings

api_key_header = APIKeyHeader(name="ApiKey", auto_error=False)


async def api_key_read_access_auth(api_key: str = Security(api_key_header)):
    """Check if the API key is valid for read-only access."""
    api_settings = get_api_settings()

    if not api_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    required_api_keys = [
        api_settings.api_key_read_access.get_secret_value(),
        api_settings.api_key_write_access.get_secret_value(),
    ]
    if api_key not in required_api_keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Allowed")


async def api_key_write_access_auth(api_key: str = Security(api_key_header)):
    """Check if the API key is valid for full access."""
    settings = get_api_settings()
    if api_key == "" or api_key != settings.api_key_write_access.get_secret_value():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")
