from pathlib import Path
import pytest


@pytest.fixture
def bad_config_path():
    return _path("files/bad_json_data.json")

@pytest.fixture
def non_existent_config_path():
    return _path("files/non_existent.json")

@pytest.fixture
def overrides_config_path():
    return _path("files/overrides.json")

@pytest.fixture
def lower_case_with_no_upcase_config_path():
    return _path("files/lower_case_with_no_upcase_formatting.json")

@pytest.fixture
def lower_case_with_upcase_config_path():
    return _path("files/lower_case_with_upcase_formatting.json")

@pytest.fixture
def lower_case_without_upcase_config_path():
    return _path("files/lower_case_without_upcase_formatting.json")

@pytest.fixture
def set_name_prompt_no_speaker_type_config_path():
    return _path("files/set_name_prompt_no_speaker_type.json")

@pytest.fixture
def set_name_prompt_no_current_speaker_name_config_path():
    return _path("files/set_name_prompt_no_current_speaker_name.json")

@pytest.fixture
def default_config_path():
    return _path("../../examples/config/platinum_steno.json")

def _path(path):
    return (Path(__file__).parent / path).resolve()

# Arguments

@pytest.fixture
def speaker_type_questioner():
    return "PLAINTIFF_1"

@pytest.fixture
def speaker_name_questioner():
    return "MR. STPHAO"

@pytest.fixture
def speaker_type_answerer():
    return "WITNESS"

@pytest.fixture
def speaker_name_answerer():
    return "THE WITNESS"

@pytest.fixture
def config_with_local_speaker_name_changes():
    return {
        "speaker_names": {
            "PLAINTIFF_1": "MR. CUSTOM NAME"
        }
    }
