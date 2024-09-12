"""
Modified from Plover's plover.formatting.RetroFormatter.iter_last_fragments().
The only change made was to to `yield` up the `action`, as well as the
`fragment`, in order to determine whether a `set_name_speaker_type` property
had been set.
"""
from typing import Generator

from plover.formatting import _Context


# NOTE: Function mostly lifted directly from Plover's codebase.
def iter_last_fragments(ctx: _Context) -> Generator[_Context, None, None]:
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
