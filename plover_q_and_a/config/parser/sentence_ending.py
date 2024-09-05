"""
Module to handle parsing and formatting of sentence endings from config.
"""
from typing import (
    Any,
    cast
)


# Default values
_INTERROGATIVE_END_MARKER: str = "?"
_STATEMENT_END_MARKER: str = "."
_INTERRUPT_MARKER: str = " --"
_YIELD_MARKER: str = "\n"
_SENTENCE_SPACE: str = " "

def interrupt_yield(data: dict[str, Any]) -> str:
    """
    Format a sentence ending interruption from config.
    """
    return cast(str, data.get("interrupt", _INTERRUPT_MARKER)) + _yield(data)

def interrogative_yield(data: dict[str, Any]) -> str:
    """
    Format a sentence ending interrogative from config.
    """
    return (
        cast(str, data.get("question_end", _INTERROGATIVE_END_MARKER))
        + _yield(data)
    )

def statement_elaborate(data: dict[str, Any]) -> str:
    """
    Format an elaborating sentence ending question from config.
    """
    return (
        _statement_end_marker(data)
        + cast(str, data.get("sentence_space", _SENTENCE_SPACE))
    )

def statement_yield(data: dict[str, Any]) -> str:
    """
    Format an yielding sentence ending question from config.
    """
    return _statement_end_marker(data) + _yield(data)

def _statement_end_marker(data: dict[str, Any]) -> str:
    return cast(str, data.get("statement_end", _STATEMENT_END_MARKER))

def _yield(data: dict[str, Any]) -> str:
    return cast(str, data.get("yield", _YIELD_MARKER))
