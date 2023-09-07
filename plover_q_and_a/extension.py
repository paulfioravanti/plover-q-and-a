"""
Plover Q&A - A Plover extension to assist with writing Question and Answer
(Q&A): the process of switching between different people or lines of questioning
in a conversation.
"""
from pathlib import Path
from typing import List

from plover.engine import StenoEngine
from plover.formatting import _Action, Case, _Context
from plover.machine.base import STATE_RUNNING
from plover.oslayer.config import CONFIG_DIR
from plover.registry import registry

from . import meta
from . import config


_CONFIG_FILEPATH = Path(CONFIG_DIR) / "q_and_a.json"

class QAndA:
    """
    Plover entry point extension class that also registers a meta plugin.
    - https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
    - https://plover.readthedocs.io/en/latest/plugin-dev/metas.html

    The meta deals with creating the Q&A sign outputs, and the extension wrapper
    around it is needed in order to:

        - Read in a config file so that all facets of the Q&A formatting can be
          customised
        - Re-read in the config file whenever the following occur:
            - The Plover UI "Reconnect" button is pressed
            - a SET_CONFIG command is send via a chord
    """

    def __init__(self, engine: StenoEngine) -> None:
        self._engine = engine
        self._config = config.load(_CONFIG_FILEPATH)

    def start(self) -> None:
        """
        Sets up the meta plugin and steno engine hooks
        """
        registry.register_plugin("meta", "q_and_a", self._q_and_a)
        self._engine.hook_connect("translated", self._translated)
        self._engine.hook_connect(
            "machine_state_changed",
            self._machine_state_changed
        )

    def stop(self) -> None:
        """
        Tears down the steno engine hooks
        """
        self._engine.hook_disconnect("translated", self._translated)
        self._engine.hook_disconnect(
            "machine_state_changed",
            self._machine_state_changed
        )

    def _q_and_a(self, ctx: _Context, args: str) -> _Action:
        """
        Delegates to meta module to generate the sign to assign to an action.
        """
        if not args:
            raise ValueError("No command provided")

        args = args.split(":")
        command, *command_args = args
        command = command.strip().upper()

        if not command:
            raise ValueError("No command arguments provided")

        action = ctx.new_action()

        if command == "SET_NAME":
            if not command_args:
                raise ValueError("No SET_NAME command arguments provided")

            set_name_command = command_args[0].strip().upper()

            if set_name_command in meta.arguments.SPEAKER_TYPES:
                current_speaker_name = (
                    self._config["speaker_names"][set_name_command]
                )
                action.text = (
                    f"[Set {set_name_command} ({current_speaker_name}) =>] "
                )
                action.set_name_speaker_type = set_name_command.strip()
                action.next_attach = True
            elif set_name_command == "DONE":
                begin_action = None
                name = ""
                for action, fragment in self._iter_last_fragments(ctx):
                    if fragment:
                        name = fragment + name

                    if hasattr(action, "set_name_speaker_type"):
                        begin_action = action
                        break

                text_to_delete = f"{begin_action.text} {name}"

                speaker_type = action.set_name_speaker_type
                self._config["speaker_names"][speaker_type] = name

                action.prev_replace = text_to_delete
                action.prev_attach = True
                action.text = ""
            else:
                raise ValueError(
                    f"Unknown SET_NAME command provided: {set_name_command}"
                )
        else:
            sign = meta.sign(args, self._config)
            action.text = sign
            if sign[0] in self._config["PREV_ATTACH_MARKERS"]:
                action.prev_attach = True
            action.next_attach = True
            action.next_case = Case.CAP_FIRST_WORD

        return action

    def _machine_state_changed(self, _machine_type: str, machine_state: str) -> None:
        """
        This hook will be called when when the Plover UI "Reconnect" button is
        pressed, so re-read in the config when that happens.
        """
        if machine_state == STATE_RUNNING:
            self._config = config.load(_CONFIG_FILEPATH)

    def _translated(self, _old: List[_Action], new: List[_Action]) -> None:
        """
        This hook is called whenever a chord produces a translation.
        Here, we are listening out for {:COMMAND:SET_CONFIG} commands. This
        command forces dictionaries to be reloaded, so we want the Q&A config
        to also be re-read in at the same time.
        """
        if len(new) == 0:
            return

        action = new[0]
        if action.command and action.command.upper() == "SET_CONFIG":
            self._config = config.load(_CONFIG_FILEPATH)

    # Modified from Plover's
    # plover.formatting.RetroFormatter.iter_last_fragments() function
    # to yield up the action as well as the fragment.
    # REF: https://github.com/openstenoproject/plover/blob/e6516275ca67105639537b7089913a893a2a495b/plover/formatting.py#L174
    def _iter_last_fragments(self, ctx):
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
            yield action, current_fragment.lstrip()
