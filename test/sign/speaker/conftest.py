import pytest


# Command Arguments

@pytest.fixture
def speaker_arg():
    return ["WITNESS"]

@pytest.fixture
def blank_sign_type_speaker_args(speaker_arg):
    return speaker_arg + [""]

@pytest.fixture
def unknown_sign_type_speaker_args(speaker_arg):
    return speaker_arg + ["UNKNOWN"]

@pytest.fixture
def initial_speaker_type(speaker_arg):
    return speaker_arg + ["INITIAL"]

@pytest.fixture
def speaker_following_interrogative_type(speaker_arg):
    return speaker_arg + ["FOLLOWING_INTERROGATIVE"]

@pytest.fixture
def speaker_following_statement_type(speaker_arg):
    return speaker_arg + ["FOLLOWING_STATEMENT"]

@pytest.fixture
def speaker_following_interrupt_type(speaker_arg):
    return speaker_arg + ["FOLLOWING_INTERRUPT"]

# Config

@pytest.fixture
def unknown_speaker_config():
    return {
        "speaker_names": {
            "COURT": "THE COURT"
        }
    }

@pytest.fixture
def speaker_config():
    return {
        "speaker_names": {
            "WITNESS": "THE WITNESS"
        }
    }

@pytest.fixture
def initial_speaker_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOR": lambda speaker_name: f"\t{speaker_name}:  "
    }

@pytest.fixture
def speaker_following_interrogative_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOLLOWING_INTERROGATIVE_FOR": (
            lambda _current_sign_type, speaker_name: (
                f"?\n\t{speaker_name}:  "
            )
        )
    }

@pytest.fixture
def speaker_following_statement_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOLLOWING_STATEMENT_FOR": (
            lambda _current_sign_type, speaker_name: (
                f".\n\t{speaker_name}:  "
            )
        )
    }

@pytest.fixture
def speaker_following_interrupt_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOLLOWING_INTERRUPT_FOR": (
            lambda _current_sign_type, speaker_name: (
                f"--\n\t{speaker_name}:  "
            )
        )
    }
