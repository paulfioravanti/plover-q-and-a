"""
Follow on module to handle the final part of commands that look like:

    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:ELABORATE_AFTER:Okay}
    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:YIELD_AFTER:All right}
    - {:Q_AND_A:ANSWER:FOLLOWING_INTERROGATIVE:ELABORATE_AFTER:Uh-huh}
    - {:Q_AND_A:ANSWER:FOLLOWING_INTERROGATIVE:YIELD_AFTER:Correct}
    - {:Q_AND_A:ANSWER:FOLLOWING_INTERROGATIVE:NAMED}
"""
from typing import (
    Any,
    Callable,
    Optional
)


_ARGUMENT_DIVIDER: str = ":"

# pylint: disable-next=too-many-arguments
def handle_follow_on(
    current_sign_type: Optional[str],
    sign_type: str,
    follow_on_args: list[str],
    sign: Callable[[Optional[str]], str],
    config: dict[str, Any],
    yield_key: str
) -> tuple[str, str]:
    """
    Generates the text for when there is an extra action performed after a
    question or answer sign change.

    Raises an error if the follow on arguments are incorrectly formatted, or if
    the follow on commands are not recognised.
    """
    if not follow_on_args:
        return (sign_type, sign(current_sign_type))

    if not len(follow_on_args) == 2:
        raise ValueError(
            "Two follow on arguments must be provided. "
            f"You gave: {_ARGUMENT_DIVIDER.join(follow_on_args)}"
        )

    follow_on_action: str
    user_string: str
    follow_on_action, user_string = follow_on_args
    follow_on_action = follow_on_action.upper()

    sign_value: str
    if follow_on_action == "YIELD_AFTER":
        sign_value = (
            sign(current_sign_type)
            + user_string
            + config[yield_key](current_sign_type)
        )
        if sign_type == "QUESTION":
            sign_type = "ANSWER"
        else:
            sign_type = "QUESTION"
    elif follow_on_action == "ELABORATE_AFTER":
        sign_value = (
            sign(current_sign_type)
            + user_string
            + config["STATEMENT_ELABORATE"](current_sign_type)
        )
    else:
        raise ValueError(
            f"Unknown follow on action provided: {follow_on_action}"
        )

    return (sign_type, sign_value)
