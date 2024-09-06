"""
Module to collate parsed application JSON config file.
"""
from typing import Any

from . import (
    answer,
    byline,
    question,
    sentence_ending,
    set_name,
    speaker
)

def parse(data: dict[str, Any]) -> tuple[Any, ...]:
    """
    Parse config data, providing defaults values where not provided.
    """
    return (
        question.marker(data),
        answer.marker(data),
        byline.marker(data),
        speaker.marker(data),
        speaker.names(data),
        speaker.should_upcase(data),
        sentence_ending.interrogative_yield(data),
        sentence_ending.statement_yield(data),
        sentence_ending.statement_elaborate(data),
        sentence_ending.interrupt_yield(data),
        set_name.prompt(data)
    )
