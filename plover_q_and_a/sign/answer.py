"""
Answer module to handle commands that look like:

    - {:Q_AND_A:ANSWER:FOLLOWING_INTERROGATIVE}
    - {:Q_AND_A:ANSWER:FOLLOWING_STATEMENT}
    - {:Q_AND_A:ANSWER:FOLLOWING_INTERRUPT}
    - {:Q_AND_A:ANSWER:FOLLOWING_INTERROGATIVE:ELABORATE_AFTER:Uh-huh}
    - {:Q_AND_A:ANSWER:FOLLOWING_INTERROGATIVE:YIELD_AFTER:Correct}

ELABORATE_AFTER and YIELD_AFTER are considered follow on arguments, and are
handled by the `follow_on` module.
"""
from typing import (
    Any,
    Callable,
    Optional
)

from . import follow_on


def sign(
    current_sign_type: Optional[str],
    sign_type: str,
    args: list[str],
    config: dict[str, Any]
) -> tuple[str, str]:
    """
    Returns the text for an answer type.

    Raises an error if the answer type is blank or not recognised.
    """
    if not args:
        raise ValueError("No answer args provided")

    answer_type: str
    follow_on_args: list[str]
    answer_type, *follow_on_args = args
    answer_type = answer_type.strip().upper()

    if not answer_type:
        raise ValueError("No answer type provided")

    answer: Callable[[Optional[str]], str]
    answer_value: str
    if answer_type in (
        "FOLLOWING_INTERROGATIVE",
        "FOLLOWING_STATEMENT",
        "FOLLOWING_INTERRUPT"
    ):
        answer = config[f"ANSWER_{answer_type}"]
        (sign_type, answer_value) = follow_on.handle_follow_on(
            current_sign_type,
            sign_type,
            follow_on_args,
            answer,
            config,
            yield_key="QUESTION_FOLLOWING_STATEMENT"
        )
    else:
        raise ValueError(f"Unknown answer type provided: {answer_type}")

    return (sign_type, answer_value)
