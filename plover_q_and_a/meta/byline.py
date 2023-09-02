"""
Byline module to handle commands that look like:

    - {:Q_AND_A:BYLINE:PLAINTIFF_1:INITIAL}
    - {:Q_AND_A:BYLINE:PLAINTIFF_2:INTERRUPTING}
    - {:Q_AND_A:BYLINE:DEFENSE_1:FOLLOWING_QUESTION}
    - {:Q_AND_A:BYLINE:DEFENSE_2:FOLLOWING_STATEMENT}
"""
from typing import List

from .arguments import (
    FOLLOWING_QUESTION,
    FOLLOWING_STATEMENT,
    INITIAL,
    INTERRUPTING
)


def sign(args: List[str], config: dict) -> str:
    """
    Returns the text for a byline type.

    Raises an error if the byline speaker or sign type are blank or not
    recognised.
    """
    if not len(args) == 2:
        given_args = ":".join(args)
        raise ValueError(
            f"Two byline arguments must be provided. You gave: {given_args}"
        )

    speaker_type, sign_type = [arg.strip().upper() for arg in args]

    if not speaker_type:
        raise ValueError("No speaker type provided")

    if not sign_type:
        raise ValueError("No sign type provided")

    try:
        speaker_name = config["BYLINE_SPEAKER_NAMES"][speaker_type]
    except KeyError as exc:
        raise ValueError(
            f"Unknown speaker type for byline provided: {speaker_type}"
        ) from exc

    if sign_type == INITIAL:
        byline = config["BYLINE"](speaker_name)
    elif sign_type == INTERRUPTING:
        byline = config["BYLINE_FOLLOWING_INTERRUPT"](speaker_name)
    elif sign_type in (FOLLOWING_STATEMENT, FOLLOWING_QUESTION):
        byline = config[f"BYLINE_{sign_type}"](speaker_name)
    else:
        raise ValueError(
            f"Unknown sign type provided for {speaker_type} byline: {sign_type}"
        )

    return byline
