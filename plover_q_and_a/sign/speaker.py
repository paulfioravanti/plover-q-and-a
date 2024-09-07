"""
Speaker module to handle commands that look like:

    - {:Q_AND_A:PLAINTIFF_1:INITIAL}
    - {:Q_AND_A:DEFENSE_2:INITIAL}
    - {:Q_AND_A:WITNESS:FOLLOWING_INTERROGATIVE}
    - {:Q_AND_A:COURT:FOLLOWING_STATEMENT}
    - {:Q_AND_A:VIDEOGRAPHER:FOLLOWING_INTERRUPT}
    - {:Q_AND_A:COURT_REPORTER:INITIAL}
    - {:Q_AND_A:CLERK:FOLLOWING_INTERROGATIVE}
    - {:Q_AND_A:BAILIFF:FOLLOWING_STATEMENT}
"""
from typing import (
    Any,
    Optional
)


def sign(
    current_sign_type: Optional[str],
    args: list[str],
    config: dict[str, Any]
) -> tuple[str, str]:
    """
    Returns the text for a known speaker.

    Raises an error if the speaker is not recognised, or if the sign type is
    blank or not recognised.
    """
    sign_type: str
    speaker_type, sign_type = extract_speaker_and_sign(args)

    try:
        speaker_name: str = config["speaker_names"][speaker_type]
    except KeyError as exc:
        raise ValueError(
            f"Unknown speaker type provided: {speaker_type}"
        ) from exc

    speaker: str
    if sign_type == "INITIAL":
        speaker = config["SPEAKER_FOR"](speaker_name)
    elif sign_type in (
        "FOLLOWING_INTERROGATIVE",
        "FOLLOWING_STATEMENT",
        "FOLLOWING_INTERRUPT"
    ):
        speaker = config[f"SPEAKER_{sign_type}_FOR"](
            current_sign_type,
            speaker_name
        )
    else:
        raise ValueError(
            f"Unknown sign type provided for {speaker_type}: {sign_type}"
        )

    return ("SPEAKER", speaker)

def extract_speaker_and_sign(args: list[str]) -> tuple[str, str]:
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
