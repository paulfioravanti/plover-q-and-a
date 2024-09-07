"""
Meta that reads in Q&A commands contained in an action and then delegates off to
other modules depending on the *first* command argument, in order to create the
appropriate text output.

Examples:

    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT}
    - {:Q_AND_A:ANSWER:FOLLOWING_INTERROGATIVE}
    - {:Q_AND_A:BYLINE:PLAINTIFF_1:INITIAL}
    - {:Q_AND_A:COURT_REPORTER:INITIAL}

In the final example above, COURT_REPORTER is included in the recognised
list of `SPEAKER_TYPES`.
"""
from typing import (
    Any,
    Optional
)

from .. import SPEAKER_TYPES
from . import (
    answer,
    byline,
    question,
    speaker
)


def text(
    current_sign_type: Optional[str],
    args: list[str],
    config: dict[str, Any]
) -> tuple[str, str]:
    """
    Checks the sign type and delegates handling to the appropriate module to
    generate the correct sign text.

    Raises an error if the sign type is blank or not recognised.
    """
    sign_type: str
    sign_type_args: list[str]
    sign_type, *sign_type_args = args
    sign_type = sign_type.strip().upper()

    if not sign_type:
        raise ValueError("No sign type provided")

    sign_text: str
    if sign_type == "QUESTION":
        (current_sign_type, sign_text) = question.sign(
            current_sign_type,
            sign_type,
            sign_type_args,
            config
        )
    elif sign_type == "ANSWER":
        (current_sign_type, sign_text) = answer.sign(
            current_sign_type,
            sign_type,
            sign_type_args,
            config
        )
    elif sign_type == "BYLINE":
        (current_sign_type, sign_text) = byline.sign(
            current_sign_type,
            sign_type_args,
            config
        )
    elif sign_type in SPEAKER_TYPES:
        (current_sign_type, sign_text) = speaker.sign(
            current_sign_type,
            args,
            config
        )
    else:
        raise ValueError(f"Unknown sign type provided: {sign_type}")

    return (current_sign_type, sign_text)
