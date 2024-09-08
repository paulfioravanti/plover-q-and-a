"""
Plover entry point extension module.

    - https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
    - https://plover.readthedocs.io/en/latest/plugin-dev/metas.html
"""
from pathlib import Path
from typing import Optional

from plover.engine import StenoEngine
from plover.formatting import (
    _Action,
    Case,
    _Context
)
from plover.machine.base import STATE_RUNNING
from plover.oslayer.config import CONFIG_DIR
from plover.registry import registry

from . import (
    config,
    sign,
    speaker
)


_ARGUMENT_DIVIDER: str = ":"
_CONFIG_FILE: Path = Path(CONFIG_DIR) / config.CONFIG_BASENAME

class QAndA:
    """
    Extension class that also registers a meta plugin.
    The meta deals with creating the Q&A sign outputs, and the extension wrapper
    around it is needed in order to:

        - Read in a config file so that all facets of the Q&A formatting can be
          customised
        - Re-read in the config file whenever the following occur:
            - The Plover UI "Reconnect" button is pressed
            - a SET_CONFIG command is send via a chord
    """
    _engine: StenoEngine
    _config: dict[str, str]
    _current_sign_type: Optional[str]

    def __init__(self, engine: StenoEngine) -> None:
        self._engine = engine

    def start(self) -> None:
        """
        Sets up the meta plugin and steno engine hooks
        """
        self._config = config.load(_CONFIG_FILE)
        self._current_sign_type = None
        registry.register_plugin("meta", "Q_AND_A", self._q_and_a)
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

    def _q_and_a(self, ctx: _Context, argument: str) -> _Action:
        """
        Delegates to meta module to generate the sign to assign to an action.
        """
        if not argument:
            raise ValueError("No command provided")

        args: list[str] = argument.split(_ARGUMENT_DIVIDER)
        command: str
        command_args: list[str]
        command, *command_args = args
        command = command.strip().upper()

        if not command:
            raise ValueError("No command arguments provided")

        action: _Action = ctx.new_action()

        if command == "RESET_CONFIG":
            self._config = config.load(_CONFIG_FILE)
        elif command == "SET_NAME":
            speaker.set_name(command_args, ctx, action, self._config)
        else:
            current_sign_type: str
            text: str
            (current_sign_type, text) = sign.text(
                self._current_sign_type,
                args,
                self._config
            )
            self._current_sign_type = current_sign_type
            action.text = text
            action.prev_attach = True
            action.next_attach = True
            action.next_case = Case.CAP_FIRST_WORD

        return action

    def _machine_state_changed(
        self,
        _machine_type: str,
        machine_state: str
    ) -> None:
        """
        This hook will be called when when the Plover UI "Reconnect" button is
        pressed, so also reload the config when that happens.
        """
        if machine_state == STATE_RUNNING:
            self._config = config.reload(_CONFIG_FILE, self._config)

    def _translated(self, _old: list[_Action], new: list[_Action]) -> None:
        """
        This hook is called whenever a chord produces a translation.
        Here, we are listening out for {:COMMAND:SET_CONFIG} commands. This
        command forces dictionaries to be reloaded, so we want the Q&A config
        to also be reloaded at the same time.
        """
        if len(new) == 0:
            return

        action: _Action = new[0]
        if action.command and action.command.upper() == "SET_CONFIG":
            self._config = config.reload(_CONFIG_FILE, self._config)
