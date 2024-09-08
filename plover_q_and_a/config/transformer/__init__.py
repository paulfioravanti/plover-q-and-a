"""
Module to handle transforming information from the application JSON config file
into a form the application can work with.
"""
from typing import (
    Any,
    Callable,
    Mapping,
    Optional,
    Union
)

from . import (
    answer,
    byline,
    question,
    sentence_ending,
    set_name,
    speaker
)


__all__ = [
    "transform"
]

TransformedData = dict[
    str,
    Union[
        str,
        bool,
        list[str],
        dict[str, str],
        Callable[[str], str],
        Callable[[str, str], str],
        Callable[[Optional[str]], str]
    ]
]

def transform(data: dict[str, Any]) -> TransformedData:
    """
    Parse config data, providing defaults values where not provided.
    """
    return {
        "question_marker": question.marker(data),
        "answer_marker": answer.marker(data),
        "byline_marker": byline.marker(data),
        "speaker_marker": speaker.marker(data),
        "speaker_names": speaker.names(data),
        "speaker_upcase": speaker.should_upcase(data),
        "interrogative_yield": sentence_ending.interrogative_yield(data),
        "statement_yield": sentence_ending.statement_yield(data),
        "statement_elaborate": sentence_ending.statement_elaborate(data),
        "interrupt_yield": sentence_ending.interrupt_yield(data),
        "set_name_prompt": set_name.prompt(data)
    }
