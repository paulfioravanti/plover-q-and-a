"""
Module to handle parsing and formatting of an answer from config.
"""
from typing import Any


# Default formatting values
_ANSWER_BEGIN_MARKER_PRE_FORMATTING: str = "\t"
_ANSWER_BEGIN_MARKER: str = "A"
_ANSWER_BEGIN_MARKER_POST_FORMATTING: str = "\t"

def marker(data: dict[str, Any]) -> str:
    """
    Format an answer from config.
    """
    answer_marker: dict[str, str] = (
        # REF: https://stackoverflow.com/a/77230846/567863
        (data.get("answer") or {}).get("marker", {})
    )

    return (
        answer_marker.get("pre", _ANSWER_BEGIN_MARKER_PRE_FORMATTING)
        + answer_marker.get("text", _ANSWER_BEGIN_MARKER)
        + answer_marker.get("post", _ANSWER_BEGIN_MARKER_POST_FORMATTING)
    )
