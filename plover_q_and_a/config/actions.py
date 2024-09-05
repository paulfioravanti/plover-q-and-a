"""
Module to handle reading in the application JSON config file.
"""
from pathlib import Path
from typing import (
    Any,
    Callable
)

from . import (
    file,
    parser
)


def load(config_path: Path) -> dict[str, Any]:
    """
    Reads in the config JSON file, munges the data into application-wide config,
    and provides defaults in case values aren't specified.

    Raises an error if the specified config file is not JSON format.
    """
    data: dict[str, Any] = file.load(config_path)

    question_marker: str
    answer_marker: str
    byline_marker: Callable[[str], str]
    speaker_marker: Callable[[str], str]
    speaker_names: list[str]
    speaker_upcase: bool
    interrogative_yield: str
    statement_yield: str
    statement_elaborate: str
    interrupt_yield: str
    set_name_prompt: str
    (
        question_marker,
        answer_marker,
        byline_marker,
        speaker_marker,
        speaker_names,
        speaker_upcase,
        interrogative_yield,
        statement_yield,
        statement_elaborate,
        interrupt_yield,
        set_name_prompt
    ) = parser.parse(data)

    return {
        "QUESTION": question_marker,
        "QUESTION_FOLLOWING_INTERRUPT": interrupt_yield + question_marker,
        "QUESTION_FOLLOWING_INTERROGATIVE": interrogative_yield + question_marker,
        "QUESTION_FOLLOWING_STATEMENT": statement_yield + question_marker,
        "ANSWER_FOLLOWING_INTERRUPT": interrupt_yield + answer_marker,
        "ANSWER_FOLLOWING_INTERROGATIVE": interrogative_yield + answer_marker,
        "ANSWER_FOLLOWING_STATEMENT": statement_yield + answer_marker,
        "BYLINE_FOR": byline_marker,
        "BYLINE_FOLLOWING_INTERRUPT_FOR": lambda speaker_name: (
            interrupt_yield + byline_marker(speaker_name)
        ),
        "BYLINE_FOLLOWING_INTERROGATIVE_FOR": lambda speaker_name: (
            interrogative_yield + byline_marker(speaker_name)
        ),
        "BYLINE_FOLLOWING_STATEMENT_FOR": lambda speaker_name: (
            statement_yield + byline_marker(speaker_name)
        ),
        "SET_NAME_PROMPT": set_name_prompt,
        "SPEAKER_FOR": speaker_marker,
        "SPEAKER_FOLLOWING_INTERRUPT_FOR": lambda speaker_name: (
            interrupt_yield + speaker_marker(speaker_name)
        ),
        "SPEAKER_FOLLOWING_INTERROGATIVE_FOR": lambda speaker_name: (
            interrogative_yield + speaker_marker(speaker_name)
        ),
        "SPEAKER_FOLLOWING_STATEMENT_FOR": lambda speaker_name: (
            statement_yield + speaker_marker(speaker_name)
        ),
        "speaker_names": speaker_names,
        "SPEAKER_UPCASE": speaker_upcase,
        "STATEMENT_ELABORATE": statement_elaborate,
    }

def reload(
    config_filepath: Path,
    current_config: dict[str, Any]
) -> dict[str, Any]:
    """
    Reloads config from defaults, but making sure to keep any speaker name
    changes that have been made.
    """
    new_config: dict[str, Any] = load(config_filepath)
    new_config["speaker_names"] = (
        new_config["speaker_names"] | current_config["speaker_names"]
    )

    return new_config
