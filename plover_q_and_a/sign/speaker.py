"""
Speaker module to handle commands that look like:

    - {:Q_AND_A:PLAINTIFF_1:INITIAL}
    - {:Q_AND_A:DEFENSE_2:INITIAL}
    - {:Q_AND_A:WITNESS:FOLLOWING_QUESTION}
    - {:Q_AND_A:COURT:FOLLOWING_STATEMENT}
    - {:Q_AND_A:VIDEOGRAPHER:INTERRUPTING}
    - {:Q_AND_A:COURT_REPORTER:INITIAL}
    - {:Q_AND_A:CLERK:FOLLOWING_QUESTION}
    - {:Q_AND_A:BAILIFF:FOLLOWING_STATEMENT}
"""
from typing import (
    Any,
    Tuple
)

from .arguments import (
    FOLLOWING_QUESTION,
    FOLLOWING_STATEMENT,
    INITIAL,
    INTERRUPTING
)


def sign(args: list[str], config: dict[str, Any]) -> str:
    """
    Returns the text for a known speaker.

    Raises an error if the speaker is not recognised, or if the sign type is
    blank or not recognised.
    """
    speaker_type: str
    sign_type: str
    speaker_type, sign_type = extract_speaker_and_sign(args)

    try:
        speaker_name: str = config["speaker_names"][speaker_type]
    except KeyError as exc:
        raise ValueError(
            f"Unknown speaker type provided: {speaker_type}"
        ) from exc

    speaker: str
    if sign_type == INITIAL:
        speaker = config["SPEAKER_FOR"](speaker_name)
    elif sign_type == INTERRUPTING:
        speaker = config["SPEAKER_FOLLOWING_INTERRUPT_FOR"](speaker_name)
    elif sign_type in (FOLLOWING_STATEMENT, FOLLOWING_QUESTION):
        speaker = config[f"SPEAKER_{sign_type}_FOR"](speaker_name)
    else:
        raise ValueError(
            f"Unknown sign type provided for {speaker_type}: {sign_type}"
        )

    return speaker

def extract_speaker_and_sign(args: list[str]) -> Tuple[str, str]:
    """
    Parses and returns speaker and sign types from a set of args.

    Raises an error if no speaker or sign type provided.
    """
    speaker_type: str
    sign_type: str
    speaker_type, sign_type = [arg.strip().upper() for arg in args]

    if not speaker_type:
        raise ValueError("No speaker type provided")

    if not sign_type:
        raise ValueError("No sign type provided")

    return speaker_type, sign_type
