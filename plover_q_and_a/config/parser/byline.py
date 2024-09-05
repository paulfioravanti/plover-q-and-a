"""
Module to handle parsing and formatting of a byline from config.
"""
from typing import (
    Any,
    Callable,
    Union,
    cast
)

from . import question


# Default formatting values
_BYLINE_MARKER: str = "BY "
_BYLINE_PRE_FORMATTING: str = ""
_BYLINE_POST_FORMATTING: str = ":\n"

def formatted_byline(data: dict[str, Any]) -> Callable[[str], str]:
    """
    Format an answer from config.
    """
    byline: dict[str, Union[str, dict[str, str]]] = cast(
        dict[str, Union[str, dict[str, str]]],
        data.get("byline", {})
    )
    byline_formatting: dict[str, str] = cast(
        dict[str, str],
        byline.get("formatting", {})
    )

    return lambda speaker_name: (
        byline_formatting.get("pre", _BYLINE_PRE_FORMATTING)
        + cast(str, byline.get("marker", _BYLINE_MARKER))
        + speaker_name
        + byline_formatting.get("post", _BYLINE_POST_FORMATTING)
        + question.marker(data)
    )
