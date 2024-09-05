"""
Module to handle parsing and formatting of a question from config.
"""
from typing import Any


# Default formatting values
_QUESTION_BEGIN_MARKER_PRE_FORMATTING: str = "\t"
_QUESTION_BEGIN_MARKER: str = "Q"
_QUESTION_BEGIN_MARKER_POST_FORMATTING: str = "\t"

def marker(data: dict[str, Any]) -> str:
    """
    Format a question from config.
    """
    question_marker: dict[str, str] = (
        # REF: https://stackoverflow.com/a/77230846/567863
        (data.get("question") or {}).get("marker", {})
    )

    return (
        question_marker.get("pre", _QUESTION_BEGIN_MARKER_PRE_FORMATTING)
        + question_marker.get("text", _QUESTION_BEGIN_MARKER)
        + question_marker.get("post", _QUESTION_BEGIN_MARKER_POST_FORMATTING)
    )
