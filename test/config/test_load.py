import json
from pathlib import Path
import pytest

from plover_q_and_a import config

_NON_LAMBDA_CONFIG_KEYS = [
    "ANSWER_FOLLOWING_INTERRUPT",
    "ANSWER_FOLLOWING_QUESTION",
    "ANSWER_FOLLOWING_STATEMENT",
    "PREV_ATTACH_MARKERS",
    "QUESTION",
    "QUESTION_FOLLOWING_INTERRUPT",
    "QUESTION_FOLLOWING_QUESTION",
    "QUESTION_FOLLOWING_STATEMENT",
    "speaker_names",
    "STATEMENT_ELABORATE"
]
_LAMBDA_CONFIG_KEYS = [
    "BYLINE_FOR",
    "BYLINE_FOLLOWING_INTERRUPT_FOR",
    "BYLINE_FOLLOWING_QUESTION_FOR",
    "BYLINE_FOLLOWING_STATEMENT_FOR",
    "SPEAKER_FOR",
    "SPEAKER_FOLLOWING_INTERRUPT_FOR",
    "SPEAKER_FOLLOWING_QUESTION_FOR",
    "SPEAKER_FOLLOWING_STATEMENT_FOR"
]

@pytest.fixture
def bad_config_path():
    return (Path(__file__).parent / "bad_json_data.json").resolve()

@pytest.fixture
def non_existent_config_path():
    return (Path(__file__).parent / "non_existent.json").resolve()

@pytest.fixture
def overrides_config_path():
    return (Path(__file__).parent / "overrides.json").resolve()

@pytest.fixture
def default_config_path():
    return (Path(__file__).parent / "../../examples/q_and_a.json").resolve()

@pytest.fixture
def speaker_name():
    return "SPEAKER_NAME"

def test_bad_config(bad_config_path):
    with pytest.raises(
        ValueError,
        match="Config file must contain a JSON object"
    ):
        config.load(bad_config_path)

def test_non_existent_config_loads_defaults(
    non_existent_config_path,
    default_config_path,
    speaker_name
):
    loaded_config = config.load(non_existent_config_path)
    default_config = config.load(default_config_path)
    for key in _NON_LAMBDA_CONFIG_KEYS:
        assert loaded_config[key] == default_config[key]
    for key in _LAMBDA_CONFIG_KEYS:
        assert (
            loaded_config[key](speaker_name)
            == default_config[key](speaker_name)
        )

def test_specified_config_overwrites_defaults(
    overrides_config_path,
    default_config_path
):
    loaded_config = config.load(overrides_config_path)
    loaded_config_speaker_name = loaded_config["speaker_names"]["PLAINTIFF_1"]
    loaded_config_speaker = (
        loaded_config["SPEAKER_FOR"](loaded_config_speaker_name)
    )
    default_config = config.load(default_config_path)
    default_config_speaker_name = default_config["speaker_names"]["PLAINTIFF_1"]
    default_config_speaker = (
        default_config["SPEAKER_FOR"](default_config_speaker_name)
    )

    assert loaded_config_speaker == "> PLAINTIFF 1 ->"
    assert not loaded_config_speaker == default_config_speaker
