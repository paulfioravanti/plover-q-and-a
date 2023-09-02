"""
Meta that reads in Q&A commands contained in an action and then delegates off to
other modules depending on the *first* command argument, in order to create the
appropriate text output.

Examples:

    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT}
    - {:Q_AND_A:ANSWER:FOLLOWING_QUESTION}
    - {:Q_AND_A:BYLINE:PLAINTIFF_1:INITIAL}
    - {:Q_AND_A:COURT_REPORTER:INITIAL}

In the final example above, COURT_REPORTER is included in the recognised
list of `SPEAKER_TYPES`.

Raises an error in the sign type is not recognised.
"""
from . import (
    answer,
    byline,
    question,
    speaker
)
from .arguments import (
    ANSWER,
    BYLINE,
    QUESTION,
    SPEAKER_TYPES
)


def sign(args: str, config: dict) -> str:
    """
    Checks the sign type and delegates handling to the appropriate module to
    generate the correct sign.

    Raises an error if the sign type is blank or not recognised.
    """
    args = args.split(":")

    sign_type, *sign_type_args = args
    sign_type = sign_type.strip().upper()

    if not sign_type:
        raise ValueError("No sign type provided")

    if sign_type == QUESTION:
        meta = question.sign(sign_type_args, config)
    elif sign_type == ANSWER:
        meta = answer.sign(sign_type_args, config)
    elif sign_type == BYLINE:
        meta = byline.sign(sign_type_args, config)
    elif sign_type in SPEAKER_TYPES:
        meta = speaker.sign(args, config)
    else:
        raise ValueError(f"Unknown sign type provided: {sign_type}")

    return meta
