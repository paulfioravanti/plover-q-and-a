"""
Question module to handle commands that look like:

    - {:Q_AND_A:QUESTION:INITIAL}
    - {:Q_AND_A:QUESTION:INTERRUPTING}
    - {:Q_AND_A:QUESTION:FOLLOWING_QUESTION}
    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT}
    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:ELABORATE_AFTER:Okay}
    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:YIELD_AFTER:All right}

ELABORATE_AFTER and YIELD_AFTER are considered follow on arguments, and are
handled by the `follow_on` module.
"""
from typing import Any

from .arguments import (
    FOLLOWING_QUESTION,
    FOLLOWING_STATEMENT,
    INITIAL,
    INTERRUPTING,
)
from . import follow_on


def sign(
    sign_type: str,
    args: list[str],
    config: dict[str, Any]
) -> tuple[str, str]:
    """
    Assigns the text for a question type.

    Raises an error if the question type is blank or not recognised.
    """
    if not args:
        raise ValueError("No question args provided")

    question_type: str
    follow_on_args: list[str]
    question_type, *follow_on_args = args
    question_type = question_type.strip().upper()

    if not question_type:
        raise ValueError("No question type provided")

    question: str
    if question_type == INITIAL:
        question = config["QUESTION"]
    elif question_type == INTERRUPTING:
        question = config["QUESTION_FOLLOWING_INTERRUPT"]
    elif question_type in (FOLLOWING_STATEMENT, FOLLOWING_QUESTION):
        question = config[f"QUESTION_{question_type}"]
        (sign_type, question) = follow_on.handle_follow_on(
            sign_type,
            follow_on_args,
            question,
            config,
            "ANSWER_FOLLOWING_QUESTION"
        )
    else:
        raise ValueError(f"Unknown question type provided: {question_type}")

    return (sign_type, question)
