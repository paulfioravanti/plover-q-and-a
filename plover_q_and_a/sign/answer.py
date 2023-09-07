"""
Answer module to handle commands that look like:

    - {:Q_AND_A:ANSWER:INTERRUPTING}
    - {:Q_AND_A:ANSWER:FOLLOWING_QUESTION}
    - {:Q_AND_A:ANSWER:FOLLOWING_STATEMENT}
    - {:Q_AND_A:ANSWER:FOLLOWING_QUESTION:ELABORATE_AFTER:Uh-huh}
    - {:Q_AND_A:ANSWER:FOLLOWING_QUESTION:YIELD_AFTER:Correct}

ELABORATE_AFTER and YIELD_AFTER are considered follow on arguments, and are
handled by the `follow_on` module.
"""
from .arguments import (
    FOLLOWING_QUESTION,
    FOLLOWING_STATEMENT,
    INTERRUPTING,
)
from .follow_on import handle_follow_on


def sign(args: list[str], config: dict[str, any]) -> str:
    """
    Returns the text for an answer type.

    Raises an error if the answer type is blank or not recognised.
    """
    if not args:
        raise ValueError("No answer args provided")

    answer_type, *follow_on_args = args
    answer_type = answer_type.strip().upper()

    if not answer_type:
        raise ValueError("No answer type provided")

    if answer_type == INTERRUPTING:
        answer = config["ANSWER_FOLLOWING_INTERRUPT"]
    elif answer_type in (FOLLOWING_STATEMENT, FOLLOWING_QUESTION):
        answer = config[f"ANSWER_{answer_type}"]
        answer = handle_follow_on(
            follow_on_args, answer, config, "QUESTION_FOLLOWING_STATEMENT"
        )
    else:
        raise ValueError(f"Unknown answer type provided: {answer_type}")

    return answer
