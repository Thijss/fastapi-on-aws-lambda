"""
Exceptions for the app.
"""


class ValidationError(Exception):
    """Raised when an asset fails validation."""


class NotFoundError(ValidationError):
    """Raised when an asset is not found."""


class AlreadyExistsError(ValidationError):
    """Raised when an asset already exists."""
