"""
Byline module to handle commands that look like:

    - {:Q_AND_A:BYLINE:PLAINTIFF_1:INITIAL}
    - {:Q_AND_A:BYLINE:PLAINTIFF_2:FOLLOWING_INTERRUPT}
    - {:Q_AND_A:BYLINE:DEFENSE_1:FOLLOWING_QUESTION}
    - {:Q_AND_A:BYLINE:DEFENSE_2:FOLLOWING_STATEMENT}
"""
from typing import Any

from .. import BYLINE_SPEAKER_TYPES
from .arguments import (
    FOLLOWING_INTERROGATIVE,
    FOLLOWING_INTERRUPT,
    FOLLOWING_STATEMENT,
    INITIAL
)
from . import speaker


def sign(args: list[str], config: dict[str, Any]) -> tuple[str, str]:
    """
    Returns the text for a byline type.

    Raises an error if the byline speaker or sign type are blank or not
    recognised.
    """
    if not len(args) == 2:
        given_args: str = ":".join(args)
        raise ValueError(
            f"Two byline arguments must be provided. You gave: {given_args}"
        )

    speaker_type: str
    sign_type: str
    speaker_type, sign_type = speaker.extract_speaker_and_sign(args)

    if not speaker_type in BYLINE_SPEAKER_TYPES:
        raise ValueError(
            f"Unknown byline speaker type provided: {speaker_type}"
        )

    try:
        speaker_name: str = config["speaker_names"][speaker_type]
    except KeyError as exc:
        raise ValueError(
            f"No speaker name entry for: {speaker_type}"
        ) from exc

    byline: str
    if sign_type == INITIAL:
        byline = config["BYLINE_FOR"](speaker_name)
    elif sign_type in (
        FOLLOWING_INTERROGATIVE,
        FOLLOWING_INTERRUPT,
        FOLLOWING_STATEMENT
    ):
        byline = config[f"BYLINE_{sign_type}_FOR"](speaker_name)
    else:
        raise ValueError(
            f"Unknown sign type provided for {speaker_type} byline: {sign_type}"
        )

    return ("QUESTION", byline)
