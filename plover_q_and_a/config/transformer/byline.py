"""
Module to handle parsing and formatting of a byline from config.
"""
from typing import (
    Any,
    Callable
)

from . import question


# Default formatting values
_BYLINE_PRE_FORMATTING: str = ""
_BYLINE_MARKER: str = "BY "
_BYLINE_POST_FORMATTING: str = ":\n"

def marker(data: dict[str, Any]) -> Callable[[str], str]:
    """
    Format an answer from config.
    """
    byline_marker: dict[str, str] = (
        # REF: https://stackoverflow.com/a/77230846/567863
        ((data.get("byline") or {}).get("question") or {}).get("marker", {})
    )

    return lambda speaker_name: (
        byline_marker.get("pre", _BYLINE_PRE_FORMATTING)
        + byline_marker.get("marker", _BYLINE_MARKER)
        + speaker_name
        + byline_marker.get("post", _BYLINE_POST_FORMATTING)
        + question.marker(data)
    )
