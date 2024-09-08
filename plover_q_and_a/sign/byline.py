"""
Byline module to handle commands that look like:

    - {:Q_AND_A:BYLINE:PLAINTIFF_1:INITIAL}
    - {:Q_AND_A:BYLINE:DEFENSE_1:FOLLOWING_INTERROGATIVE}
    - {:Q_AND_A:BYLINE:DEFENSE_2:FOLLOWING_STATEMENT}
    - {:Q_AND_A:BYLINE:PLAINTIFF_2:FOLLOWING_INTERRUPT}
    - {:Q_AND_A:BYLINE:WITNESS:FOLLOWING_INTERROGATIVE}
"""
from typing import (
    Any,
    Optional
)

from .. import BYLINE_SPEAKER_TYPES
from . import speaker


_ARGUMENT_DIVIDER: str = ":"

def sign(
    current_sign_type: Optional[str],
    args: list[str],
    config: dict[str, Any]
) -> tuple[str, str]:
    """
    Returns the text for a byline type.

    Raises an error if the byline speaker or sign type are blank or not
    recognised.
    """
    if not len(args) == 2:
        raise ValueError(
            "Two byline arguments must be provided. "
            f"You gave: {_ARGUMENT_DIVIDER.join(args)}"
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
        raise ValueError(f"No speaker name entry for: {speaker_type}") from exc

    byline: str
    if sign_type == "INITIAL":
        byline = config["BYLINE_FOR"](speaker_type, speaker_name)
    elif sign_type in (
        "FOLLOWING_INTERROGATIVE",
        "FOLLOWING_INTERRUPT",
        "FOLLOWING_STATEMENT"
    ):
        byline = (
            config[f"BYLINE_{sign_type}_FOR"](
                current_sign_type,
                speaker_type,
                speaker_name
            )
        )
    else:
        raise ValueError(
            f"Unknown sign type provided for {speaker_type} byline: {sign_type}"
        )

    new_current_sign_type: str
    if speaker_type == "WITNESS":
        new_current_sign_type = "ANSWER"
    else:
        new_current_sign_type = "QUESTION"

    return (new_current_sign_type, byline)
