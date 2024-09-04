"""
Follow on module to handle the final part of commands that look like:

    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:ELABORATE_AFTER:Okay}
    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:YIELD_AFTER:All right}
    - {:Q_AND_A:ANSWER:FOLLOWING_QUESTION:ELABORATE_AFTER:Uh-huh}
    - {:Q_AND_A:ANSWER:FOLLOWING_QUESTION:YIELD_AFTER:Correct}
"""
from typing import Any


_ELABORATE_AFTER = "ELABORATE_AFTER"
_YIELD_AFTER = "YIELD_AFTER"

def handle_follow_on(
    sign_type: str,
    follow_on_args: list[str],
    sign: str,
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
        return (sign_type, sign)

    if not len(follow_on_args) == 2:
        given_args: str = ":".join(follow_on_args)
        raise ValueError(
            f"Two follow on arguments must be provided. You gave: {given_args}"
        )

    follow_on_action: str
    user_string: str
    follow_on_action, user_string = follow_on_args
    follow_on_action = follow_on_action.upper()

    if follow_on_action == _YIELD_AFTER:
        sign += user_string + config[yield_key]
        if sign_type == "QUESTION":
            sign_type = "ANSWER"
        else:
            sign_type = "QUESTION"
    elif follow_on_action == _ELABORATE_AFTER:
        sign += user_string + config["STATEMENT_ELABORATE"]
    else:
        raise ValueError(
            f"Unknown follow on action provided: {follow_on_action}"
        )

    return (sign_type, sign)
