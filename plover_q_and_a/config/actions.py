"""
Module to handle reading in the application JSON config file.
"""
from pathlib import Path
from typing import Any

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
    data = file.load(config_path)
    (
        formatted_question,
        question_end,
        formatted_answer,
        statement_end,
        statement_elaborate,
        interrupt,
        formatted_byline,
        set_name_prompt,
        speaker_upcase,
        speaker_names,
        formatted_speaker
    ) = parser.parse(data)

    return {
        "ANSWER_FOLLOWING_INTERRUPT": interrupt + formatted_answer,
        "ANSWER_FOLLOWING_QUESTION": question_end + formatted_answer,
        "ANSWER_FOLLOWING_STATEMENT": statement_end + formatted_answer,
        "BYLINE_FOR": formatted_byline,
        "BYLINE_FOLLOWING_INTERRUPT_FOR": lambda speaker_name: (
            interrupt + formatted_byline(speaker_name)
        ),
        "BYLINE_FOLLOWING_QUESTION_FOR": lambda speaker_name: (
            question_end + formatted_byline(speaker_name)
        ),
        "BYLINE_FOLLOWING_STATEMENT_FOR": lambda speaker_name: (
            statement_end + formatted_byline(speaker_name)
        ),
        "QUESTION": formatted_question,
        "QUESTION_FOLLOWING_INTERRUPT": interrupt + formatted_question,
        "QUESTION_FOLLOWING_QUESTION": question_end + formatted_question,
        "QUESTION_FOLLOWING_STATEMENT": statement_end + formatted_question,
        "SET_NAME_PROMPT": set_name_prompt,
        "SPEAKER_FOR": formatted_speaker,
        "SPEAKER_FOLLOWING_INTERRUPT_FOR": lambda speaker_name: (
            interrupt + formatted_speaker(speaker_name)
        ),
        "SPEAKER_FOLLOWING_QUESTION_FOR": lambda speaker_name: (
            question_end + formatted_speaker(speaker_name)
        ),
        "SPEAKER_FOLLOWING_STATEMENT_FOR": lambda speaker_name: (
            statement_end + formatted_speaker(speaker_name)
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
    new_config = load(config_filepath)
    new_config["speaker_names"] = (
        new_config["speaker_names"] | current_config["speaker_names"]
    )

    return new_config
