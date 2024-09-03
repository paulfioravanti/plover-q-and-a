"""
Module to handle parsing and formatting of an answer from config.
"""
from typing import (
    Any,
    Union,
    cast
)


# Default formatting values
_ANSWER_BEGIN_MARKER: str = "A"
_ANSWER_BEGIN_MARKER_PRE_FORMATTING: str = "\t"
_ANSWER_BEGIN_MARKER_POST_FORMATTING: str = "\t"

def formatted_answer(data: dict[str, Any]) -> str:
    """
    Format an answer from config.
    """
    answer: dict[str, Union[str, dict[str, str]]] = data.get("answer", {})
    answer_formatting: dict[str, str] = cast(
        dict[str, str],
        answer.get("formatting", {})
    )

    return (
        answer_formatting.get("pre", _ANSWER_BEGIN_MARKER_PRE_FORMATTING)
        + cast(str, answer.get("marker", _ANSWER_BEGIN_MARKER))
        + answer_formatting.get("post", _ANSWER_BEGIN_MARKER_POST_FORMATTING)
    )
