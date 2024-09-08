"""
Module to handle parsing and formatting of a byline from config.
"""
from typing import (
    Any,
    Callable,
    cast
)

from . import (
    answer,
    question
)


# Default formatting values
_BYLINE_QUESTION_PRE_FORMATTING: str = ""
_BYLINE_QUESTION_MARKER_TEXT: str = "BY "
_BYLINE_QUESTION_POST_FORMATTING: str = ":\n"
_BYLINE_ANSWER_PRE_FORMATTING: str = ""
_BYLINE_ANSWER_MARKER_TEXT: str = ""
_BYLINE_ANSWER_POST_FORMATTING: str = ""

def marker(data: dict[str, Any]) -> Callable[[str, str], str]:
    """
    Format an answer from config.
    """
    question_byline: Callable[[str], str] = _question_byline(data)
    answer_byline: Callable[[str], str] = _answer_byline(data)

    def _function(speaker_type: str, speaker_name: str) -> str:
        if speaker_type == "WITNESS":
            return answer_byline(speaker_name)

        return question_byline(speaker_name)

    return _function

def _question_byline(data: dict[str, Any]) -> Callable[[str], str]:
    byline_marker: dict[str, str] = _byline_marker_for(data, "question")
    pre_formatting: str = (
        byline_marker.get("pre", _BYLINE_QUESTION_PRE_FORMATTING)
    )
    marker_text: str = byline_marker.get("text", _BYLINE_QUESTION_MARKER_TEXT)
    post_formatting: str = (
        byline_marker.get("post", _BYLINE_QUESTION_POST_FORMATTING)
    )
    byline_follow_on: str = question.marker(data)

    return lambda speaker_name: (
        pre_formatting
        + marker_text
        + speaker_name
        + post_formatting
        + byline_follow_on
    )

def _answer_byline(data: dict[str, Any]) -> Callable[[str], str]:
    byline_marker: dict[str, str] = _byline_marker_for(data, "answer")
    pre_formatting: str = (
        byline_marker.get("pre", _BYLINE_ANSWER_PRE_FORMATTING)
    )
    marker_text: str = byline_marker.get("text", _BYLINE_ANSWER_MARKER_TEXT)
    post_formatting: str = (
        byline_marker.get("post", _BYLINE_ANSWER_POST_FORMATTING)
    )
    byline_follow_on: str = answer.marker(data)

    return lambda speaker_name: (
        pre_formatting
        + marker_text
        + speaker_name
        + post_formatting
        + byline_follow_on
    )

def _byline_marker_for(
    data: dict[str, Any],
    byline_type: str
) -> dict[str, str]:
    return cast(
        dict[str, str],
        ((data.get("byline") or {}).get(byline_type) or {}).get("marker", {})
    )
