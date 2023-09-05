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
        sign = meta.sign(args, self._config)
        action = ctx.new_action()
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
