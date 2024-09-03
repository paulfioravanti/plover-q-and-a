"""
Module to handle parsing and formatting of a question from config.
"""
from typing import (
    Any,
    Union,
    cast
)


# Default formatting values
_QUESTION_BEGIN_MARKER: str = "Q"
_QUESTION_BEGIN_MARKER_PRE_FORMATTING: str = "\t"
_QUESTION_BEGIN_MARKER_POST_FORMATTING: str = "\t"

def formatted_question(data: dict[str, Any]) -> str:
    """
    Format a question from config.
    """
    question: dict[str, Union[str, dict[str, str]]] = data.get("question", {})
    question_formatting: dict[str, str] = cast(
        dict[str, str],
        question.get("formatting", {})
    )

    return (
        question_formatting.get("pre", _QUESTION_BEGIN_MARKER_PRE_FORMATTING)
        + cast(str, question.get("marker", _QUESTION_BEGIN_MARKER))
        + question_formatting.get(
            "post", _QUESTION_BEGIN_MARKER_POST_FORMATTING
        )
    )
