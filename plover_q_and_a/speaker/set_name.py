"""
Handles commands related to setting the name of a recognised speaker.

Examples:

    - {:Q_AND_A:SET_NAME:PLAINTIFF_1}
    - {:Q_AND_A:SET_NAME:DONE}

In the first example above, PLAINTIFF_1 is included in the recognised
list of `SPEAKER_TYPES`.
"""
from typing import (
    Any,
    Union
)

from plover.formatting import (
    _Action,
    _Context
)

from .. import SPEAKER_TYPES
from .formatting import iter_last_fragments


def set_name(
    command_args: list[str],
    ctx: _Context,
    action: _Action,
    config: dict[str, Any]
) -> None:
    """
    Checks the set name command and delegates handling to the appropriate
    function.

    Raises an error if the set name argument is blank or not recognised.
    """
    if not command_args:
        raise ValueError("No SET_NAME command arguments provided")

    set_name_command: str = command_args[0].strip().upper()

    if set_name_command in SPEAKER_TYPES:
        _begin_set_speaker_name(set_name_command, action, config)
    elif set_name_command == "DONE":
        _end_set_speaker_name(ctx, action, config)
    else:
        raise ValueError(
            f"Unknown SET_NAME command provided: {set_name_command}"
        )

def _begin_set_speaker_name(
    speaker_type: str,
    action: _Action,
    config: dict[str, Any]
) -> None:
    """
    Opens up a prompt to set the speaker name, and marks an action as the place
    where the prompt started so it can be searched for later.
    """
    # NOTE: This is an arbitrary attr that is being set on an `_Action` object,
    # and is *not* part of the `_Action` API (but doing this kind of dynamic
    # attribute assignment seems to be allowed).
    setattr(action, "set_name_speaker_type", speaker_type.strip())
    current_speaker_name: str = config["speaker_names"][speaker_type]
    action.text = config["SET_NAME_PROMPT"].format(
        speaker_type=speaker_type,
        current_speaker_name=current_speaker_name
    )
    action.next_attach = True

def _end_set_speaker_name(
    ctx: _Context,
    action: _Action,
    config: dict[str, Any]
) -> None:
    """
    Searches the previous actions in a context for the place where a set speaker
    name prompt began. Once found, take the text entered after the prompt, set
    that name in the config, and delete the prompt text from the current action.
    """
    begin_action: Union[_Action, None] = None
    name: str = ""
    for prev_action, fragment in iter_last_fragments(ctx):
        if fragment:
            name = fragment + name

        if hasattr(prev_action, "set_name_speaker_type"):
            begin_action = prev_action
            break

    # Ignore SET_NAME:DONE command if called before SET_NAME:<SPEAKER>
    if not begin_action:
        return

    speaker_type: str = getattr(begin_action, "set_name_speaker_type")

    if config["SPEAKER_UPCASE"]:
        name = name.upper()

    config["speaker_names"][speaker_type] = name

    # NOTE: prev_replace text gets deleted.
    action.prev_replace = f"{begin_action.text} {name}"
    action.prev_attach = True
    action.text = ""
