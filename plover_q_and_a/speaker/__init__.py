"""
Handles commands related to setting the name of a recognised speaker.

Examples:

    - {:Q_AND_A:SET_NAME:PLAINTIFF_1}
    - {:Q_AND_A:SET_NAME:DONE}

In the first example above, PLAINTIFF_1 is included in the recognised
list of `SPEAKER_TYPES`.
"""
from plover.formatting import _Action, _Context

from ..arguments import SPEAKER_TYPES
from .arguments import DONE


_SET_NAME_SPEAKER_TYPE_ATTR = "set_name_speaker_type"
_SET_NAME_PROMPT = "[Set %s (%s) =>] "

def set_name(
    command_args: list[str],
    ctx: _Context,
    action: _Action,
    config: dict[str, any]
) -> None:
    """
    Checks the set name command and delegates handling to the appropriate
    function.

    Raises an error if the set name argument is blank or not recognised.
    """
    if not command_args:
        raise ValueError("No SET_NAME command arguments provided")

    set_name_command = command_args[0].strip().upper()

    if set_name_command in SPEAKER_TYPES:
        _begin_set_speaker_name(set_name_command, action, config)
    elif set_name_command == DONE:
        _end_set_speaker_name(ctx, action, config)
    else:
        raise ValueError(
            f"Unknown SET_NAME command provided: {set_name_command}"
        )

def _begin_set_speaker_name(
    speaker_type: str,
    action: _Action,
    config: dict[str, any]
) -> None:
    """
    Opens up a prompt to set the speaker name, and marks an action as the place
    where the prompt started so it can be searched for later.
    """
    setattr(action, _SET_NAME_SPEAKER_TYPE_ATTR, speaker_type.strip())
    current_speaker_name = config["speaker_names"][speaker_type]
    action.text = _SET_NAME_PROMPT % (speaker_type, current_speaker_name)
    action.next_attach = True

def _end_set_speaker_name(
    ctx: _Context,
    action: _Action,
    config: dict[str, any]
) -> None:
    """
    Searches the previous actions in a context for the place where a set speaker
    name prompt began. Once found, take the text entered after the prompt, set
    that name in the config, and delete the prompt text from the current action.
    """
    begin_action = None
    name = ""
    for prev_action, fragment in _iter_last_fragments(ctx):
        if fragment:
            name = fragment + name

        if hasattr(prev_action, _SET_NAME_SPEAKER_TYPE_ATTR):
            begin_action = prev_action
            break

    text_to_delete = f"{begin_action.text} {name}"

    speaker_type = getattr(begin_action, _SET_NAME_SPEAKER_TYPE_ATTR)
    name = name.upper() if config["SPEAKER_UPCASE"] else name
    config["speaker_names"][speaker_type] = name

    action.prev_replace = text_to_delete
    action.prev_attach = True
    action.text = ""

# Modified from Plover's plover.formatting.RetroFormatter.iter_last_fragments().
# The only change made was to to `yield` up the `action`, as well as the
# `fragment`, in order to determine whether a `set_name_speaker_type` property
# had been set.
def _iter_last_fragments(ctx: _Context):
    """
    Iterate over last text fragments (last first).

    A text fragment is a series of non-whitespace characters
    followed by zero or more trailing whitespace characters.
    """
    replace = 0
    next_action = None
    current_fragment = ""
    for action in ctx.iter_last_actions():
        part = "" if action.text is None else action.text
        if (
            next_action is not None
            and next_action.text is not None
            and not next_action.prev_attach
        ):
            part += next_action.space_char
        if replace:
            # Ignore replaced content.
            if len(part) > replace:
                part = part[:-replace]
                replace = 0
            else:
                replace -= len(part)
                part = ''
        if part:
            # Find out new complete fragments.
            fragments = ctx.FRAGMENT_RX.findall(part + current_fragment)
            for fragment in reversed(fragments[1:]):
                yield action, fragment
            current_fragment = fragments[0]
        replace += len(action.prev_replace)
        next_action = action

    # Don't forget to process the current (first) fragment.
    if not current_fragment.isspace():
        yield next_action, current_fragment.lstrip()
