"""
Follow on module to handle the final part of commands that look like:

    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:ELABORATE_AFTER:Okay}
    - {:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:YIELD_AFTER:All right}
    - {:Q_AND_A:ANSWER:FOLLOWING_QUESTION:ELABORATE_AFTER:Uh-huh}
    - {:Q_AND_A:ANSWER:FOLLOWING_QUESTION:YIELD_AFTER:Correct}
"""
from typing import Any


_ARGUMENT_DIVIDER: str = ":"
_ELABORATE_AFTER: str = "ELABORATE_AFTER"
_ELABORATE_AFTER_CONFIG_KEY: str = "STATEMENT_ELABORATE"
_YIELD_AFTER: str = "YIELD_AFTER"
_QUESTION_SIGN_TYPE: str = "QUESTION"
_ANSWER_SIGN_TYPE: str = "ANSWER"

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
        given_args: str = _ARGUMENT_DIVIDER.join(follow_on_args)
        raise ValueError(
            f"Two follow on arguments must be provided. You gave: {given_args}"
        )

    follow_on_action: str
    user_string: str
    follow_on_action, user_string = follow_on_args
    follow_on_action = follow_on_action.upper()

    if follow_on_action == _YIELD_AFTER:
        sign += user_string + config[yield_key]
        if sign_type == _QUESTION_SIGN_TYPE:
            sign_type = _ANSWER_SIGN_TYPE
        else:
            sign_type = _QUESTION_SIGN_TYPE
    elif follow_on_action == _ELABORATE_AFTER:
        sign += user_string + config[_ELABORATE_AFTER_CONFIG_KEY]
    else:
        raise ValueError(
            f"Unknown follow on action provided: {follow_on_action}"
        )

    return (sign_type, sign)
