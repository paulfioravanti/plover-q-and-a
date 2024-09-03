"""
Module to collate parsed application JSON config file.
"""
from typing import (
    Any,
    Tuple
)
from . import (
    answer,
    byline,
    question,
    sentence_ending,
    set_name,
    speaker
)

def parse(data: dict[str, Any]) -> Tuple[Any, ...]:
    """
    Parse config data, providing defaults values where not provided.
    """
    return (
        question.formatted_question(data),
        sentence_ending.question_yield(data),
        answer.formatted_answer(data),
        sentence_ending.statement_yield(data),
        sentence_ending.statement_elaborate(data),
        sentence_ending.interrupt_yield(data),
        byline.formatted_byline(data),
        set_name.prompt(data),
        speaker.should_upcase(data),
        speaker.names(data),
        speaker.formatted_speaker(data)
    )
