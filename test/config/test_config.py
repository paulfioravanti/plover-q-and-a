import json
from pathlib import Path
import pytest

from plover_q_and_a import config

_NON_LAMBDA_CONFIG_KEYS = [
    "ANSWER_FOLLOWING_INTERRUPT",
    "ANSWER_FOLLOWING_QUESTION",
    "ANSWER_FOLLOWING_STATEMENT",
    "QUESTION",
    "QUESTION_FOLLOWING_INTERRUPT",
    "QUESTION_FOLLOWING_QUESTION",
    "QUESTION_FOLLOWING_STATEMENT",
    "SET_NAME_PROMPT",
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

# Files

@pytest.fixture
def bad_config_path():
    return (Path(__file__).parent / "files/bad_json_data.json").resolve()

@pytest.fixture
def non_existent_config_path():
    return (Path(__file__).parent / "files/non_existent.json").resolve()

@pytest.fixture
def overrides_config_path():
    return (Path(__file__).parent / "files/overrides.json").resolve()

@pytest.fixture
def lower_case_with_no_upcase_config_path():
    return (
      Path(__file__).parent / "files/lower_case_with_no_upcase_formatting.json"
    ).resolve()

@pytest.fixture
def lower_case_with_upcase_config_path():
    return (
      Path(__file__).parent / "files/lower_case_with_upcase_formatting.json"
    ).resolve()

@pytest.fixture
def lower_case_without_upcase_config_path():
    return (
      Path(__file__).parent / "files/lower_case_without_upcase_formatting.json"
    ).resolve()

@pytest.fixture
def set_name_prompt_no_speaker_type_config_path():
    return (
      Path(__file__).parent / "files/set_name_prompt_no_speaker_type.json"
    ).resolve()

@pytest.fixture
def set_name_prompt_no_current_speaker_name_config_path():
    return (
      Path(__file__).parent
      / "files/set_name_prompt_no_current_speaker_name.json"
    ).resolve()

@pytest.fixture
def default_config_path():
    return (Path(__file__).parent / "../../examples/q_and_a.json").resolve()

# Arguments

@pytest.fixture
def speaker_name():
    return "SPEAKER_NAME"

@pytest.fixture
def config_with_local_speaker_name_changes():
    return {
        "speaker_names": {
            "PLAINTIFF_1": "MR. CUSTOM NAME"
        }
    }

# Tests

def test_bad_config(bad_config_path):
    with pytest.raises(
        ValueError,
        match="Unable to decode file contents as JSON"
    ):
        config.load(bad_config_path)

def test_no_speaker_type_in_set_name_prompt(
    set_name_prompt_no_speaker_type_config_path
):
    with pytest.raises(
        ValueError,
        match=(
            "Both {speaker_type} and {current_speaker_name} must be "
            "present in the set_name_prompt."
        )
    ):
        config.load(set_name_prompt_no_speaker_type_config_path)

def test_no_current_speaker_name_in_set_name_prompt(
    set_name_prompt_no_current_speaker_name_config_path
):
    with pytest.raises(
        ValueError,
        match=(
            "Both {speaker_type} and {current_speaker_name} must be "
            "present in the set_name_prompt."
        )
    ):
        config.load(set_name_prompt_no_current_speaker_name_config_path)

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

def test_lower_case_speaker_names_get_upcased_when_no_formatting_upcase_given(
    lower_case_with_no_upcase_config_path
):
    loaded_config = config.load(lower_case_with_no_upcase_config_path)
    assert loaded_config["speaker_names"]["PLAINTIFF_1"] == "MR. JOHNSON"

def test_lower_case_speaker_names_get_upcased_when_formatting_upcase_true(
    lower_case_with_upcase_config_path
):
    loaded_config = config.load(lower_case_with_upcase_config_path)
    assert loaded_config["speaker_names"]["PLAINTIFF_1"] == "MR. JOHNSON"

def test_lower_case_speaker_names_stay_lowercased_when_formatting_upcase_false(
    lower_case_without_upcase_config_path
):
    loaded_config = config.load(lower_case_without_upcase_config_path)
    assert loaded_config["speaker_names"]["PLAINTIFF_1"] == "mr. johnson"

def test_reloading_does_not_overwrite_local_changes_to_speaker_names(
    default_config_path,
    config_with_local_speaker_name_changes,
):
    reloaded_config = config.reload(
        default_config_path,
        config_with_local_speaker_name_changes
    )
    # Custom value stays
    assert reloaded_config["speaker_names"]["PLAINTIFF_1"] == "MR. CUSTOM NAME"
    # Default values inserted
    assert reloaded_config["speaker_names"]["PLAINTIFF_2"] == "MR. SKWRAO"
