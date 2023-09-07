from pathlib import Path
import pytest

from plover_q_and_a import config

# Files

@pytest.fixture
def default_config_path():
    return (Path(__file__).parent / "../../examples/q_and_a.json").resolve()

# Config

@pytest.fixture
def config_with_local_speaker_name_changes():
    return {
        "speaker_names": {
            "PLAINTIFF_1": "MR. CUSTOM NAME"
        }
    }

# Tests

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
