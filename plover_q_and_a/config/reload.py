"""
Module that deals with config reloading.
"""
from pathlib import Path
from typing import Any

from .load import load


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
