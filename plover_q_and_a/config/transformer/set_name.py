"""
Module to handle parsing and formatting of a set speaker name prompt
from config.
"""
import re
from typing import (
    Any,
    Pattern,
    cast
)


# Default value
_SET_NAME_PROMPT: str = "[Set {speaker_type} ({current_speaker_name}) =>] "
# Prompt must contain both literal {speaker_type} and {current_speaker_name}
# strings in the prompt, otherwise it is invalid.
_SET_NAME_PROMPT_MATCH_CONDITION: Pattern[str] = re.compile(
    r"(?=.*{speaker_type})(?=.*{current_speaker_name})"
)

def prompt(data: dict[str, Any]) -> str:
    """
    Format a set name prompt from config.
    """
    set_name_prompt: str = cast(
        str,
        data.get("set_name_prompt", _SET_NAME_PROMPT)
    )

    if not re.match(_SET_NAME_PROMPT_MATCH_CONDITION, set_name_prompt):
        raise ValueError(
            "Both {speaker_type} and {current_speaker_name} must be "
            "present in the set_name_prompt."
        )

    return set_name_prompt
