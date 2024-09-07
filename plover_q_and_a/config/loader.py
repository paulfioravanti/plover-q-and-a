"""
Module to handle reading in the application JSON config file.
"""
from pathlib import Path
from typing import (
    Any,
    Callable,
    Optional,
    cast
)

from . import (
    extractor,
    transformer
)


def load(config_path: Path) -> dict[str, Any]:
    """
    Reads in the config JSON file, munges the data into application-wide config,
    and provides defaults in case values aren't specified.

    Raises an error if the specified config file is not JSON format.
    """
    config_data: dict[str, Any] = extractor.load(config_path)
    data: transformer.TransformedData = transformer.transform(config_data)

    return {
        "QUESTION": data["question_marker"],
        "QUESTION_FOLLOWING_INTERROGATIVE": lambda current_sign_type: (
            cast(
                Callable[[Optional[str]], str],
                data["interrogative_yield"]
            )(current_sign_type)
            + cast(str, data["question_marker"])
        ),
        "QUESTION_FOLLOWING_STATEMENT": lambda current_sign_type: (
            cast(
                Callable[[Optional[str]], str],
                data["statement_yield"]
            )(current_sign_type)
            + cast(str, data["question_marker"])
        ),
        "QUESTION_FOLLOWING_INTERRUPT": lambda current_sign_type: (
            cast(
                Callable[[Optional[str]], str],
                data["interrupt_yield"]
            )(current_sign_type)
            + cast(str, data["question_marker"])
        ),
        "ANSWER_FOLLOWING_INTERROGATIVE": lambda current_sign_type: (
            cast(
                Callable[[Optional[str]], str],
                data["interrogative_yield"]
            )(current_sign_type)
            + cast(str, data["answer_marker"])
        ),
        "ANSWER_FOLLOWING_STATEMENT": lambda current_sign_type: (
            cast(
                Callable[[Optional[str]], str],
                data["statement_yield"]
            )(current_sign_type)
            + cast(str, data["answer_marker"])
        ),
        "ANSWER_FOLLOWING_INTERRUPT": lambda current_sign_type: (
            cast(
                Callable[[Optional[str]], str],
                data["interrupt_yield"]
            )(current_sign_type)
            + cast(str, data["answer_marker"])
        ),
        "BYLINE_FOR": data["byline_marker"],
        "BYLINE_FOLLOWING_INTERROGATIVE_FOR": (
            lambda current_sign_type, speaker_name: (
                cast(
                    Callable[[Optional[str]], str],
                    data["interrogative_yield"]
                )(current_sign_type)
                + cast(
                    Callable[[str], str],
                    data["byline_marker"]
                )(speaker_name)
            )
        ),
        "BYLINE_FOLLOWING_STATEMENT_FOR": (
            lambda current_sign_type, speaker_name: (
                cast(
                    Callable[[Optional[str]], str],
                    data["statement_yield"]
                )(current_sign_type)
                + cast(
                    Callable[[str], str],
                    data["byline_marker"]
                )(speaker_name)
            )
        ),
        "BYLINE_FOLLOWING_INTERRUPT_FOR": (
            lambda current_sign_type, speaker_name: (
                cast(
                    Callable[[Optional[str]], str],
                    data["interrupt_yield"]
                )(current_sign_type)
                + cast(
                    Callable[[str], str],
                    data["byline_marker"]
                )(speaker_name)
            )
        ),
        "SPEAKER_FOR": data["speaker_marker"],
        "SPEAKER_FOLLOWING_INTERROGATIVE_FOR": (
            lambda current_sign_type, speaker_name: (
                cast(
                    Callable[[Optional[str]], str],
                    data["interrogative_yield"]
                )(current_sign_type)
                + cast(
                    Callable[[str], str],
                    data["speaker_marker"]
                )(speaker_name)
            )
        ),
        "SPEAKER_FOLLOWING_STATEMENT_FOR": (
            lambda current_sign_type, speaker_name: (
                cast(
                    Callable[[Optional[str]], str],
                    data["statement_yield"]
                )(current_sign_type)
                + cast(
                    Callable[[str], str],
                    data["speaker_marker"]
                )(speaker_name)
            )
        ),
        "SPEAKER_FOLLOWING_INTERRUPT_FOR": (
            lambda current_sign_type, speaker_name: (
                cast(
                    Callable[[Optional[str]], str],
                    data["interrupt_yield"]
                )(current_sign_type)
                + cast(
                    Callable[[str], str],
                    data["speaker_marker"]
                )(speaker_name)
            )
        ),
        "speaker_names": data["speaker_names"],
        "SPEAKER_UPCASE": data["speaker_upcase"],
        # NOTE: Not sure what's going on with pylint with the warning below...
        # pylint: disable-next=unnecessary-lambda
        "STATEMENT_ELABORATE": lambda current_sign_type: (
            cast(
                Callable[[Optional[str]], str],
                data["statement_elaborate"]
            )(current_sign_type)
        ),
        "SET_NAME_PROMPT": data["set_name_prompt"]
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
