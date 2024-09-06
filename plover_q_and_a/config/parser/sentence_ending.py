"""
Module to handle parsing and formatting of sentence endings from config.
"""
from typing import (
    Any,
    Callable,
    Optional,
    cast
)


# Default values
_INTERROGATIVE_END_MARKER: str = "?"
_STATEMENT_END_MARKER: str = "."
_INTERRUPT_MARKER: str = " --"
_YIELD_MARKER: str = "\n"
_SENTENCE_SPACE: str = " "

def interrogative_yield(data: dict[str, Any]) -> Callable[[str], str]:
    """
    Format a sentence ending interrogative from config.
    """
    def _function(current_sign_type: Optional[str]) -> str:
        sign_type_ending: dict[str, str] = _sign_type_ending(
            current_sign_type,
            data
        )

        return (
            sign_type_ending.get("interrogative", _INTERROGATIVE_END_MARKER)
            + _yield(sign_type_ending)
        )

    return _function

def statement_elaborate(data: dict[str, Any]) -> Callable[[str], str]:
    """
    Format an elaborating sentence ending question from config.
    """
    def _function(current_sign_type: Optional[str]) -> str:
        sign_type_ending: dict[str, str] = _sign_type_ending(
            current_sign_type,
            data
        )

        return (
            _statement_end_marker(sign_type_ending)
            + cast(str, data.get("sentence_space", _SENTENCE_SPACE))
        )

    return _function

def statement_yield(data: dict[str, Any]) -> Callable[[str], str]:
    """
    Format an yielding sentence ending question from config.
    """
    def _function(current_sign_type: Optional[str]) -> str:
        sign_type_ending: dict[str, str] = _sign_type_ending(
            current_sign_type,
            data
        )

        return (
            _statement_end_marker(sign_type_ending)
            + _yield(sign_type_ending)
        )

    return _function

def interrupt_yield(data: dict[str, Any]) -> Callable[[str], str]:
    """
    Format a sentence ending interruption from config.
    """
    def _function(current_sign_type: Optional[str]) -> str:
        sign_type_ending: dict[str, str] = _sign_type_ending(
            current_sign_type,
            data
        )

        return (
            sign_type_ending.get("interrupt", _INTERRUPT_MARKER)
            + _yield(sign_type_ending)
        )

    return _function

def _sign_type_ending(
    current_sign_type: Optional[str],
    data: dict[str, Any]
) -> dict[str, str]:
    sign_type_key: str
    if current_sign_type:
        sign_type_key = current_sign_type.lower()
    else:
        sign_type_key = ""

    # REF: https://stackoverflow.com/a/77230846/567863
    return (data.get(sign_type_key) or {}).get("ending") or {}

def _statement_end_marker(sign_type_ending: dict[str, str]) -> str:
    return sign_type_ending.get("statement", _STATEMENT_END_MARKER)

def _yield(sign_type_ending: dict[str, str]) -> str:
    return sign_type_ending.get("yield", _YIELD_MARKER)
