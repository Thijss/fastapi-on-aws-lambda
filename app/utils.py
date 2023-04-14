"""
Utility functions.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def int_to_ordinal(number: int) -> str:
    """Convert an integer to its ordinal representation."""
    if number % 100 in [11, 12, 13]:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"
