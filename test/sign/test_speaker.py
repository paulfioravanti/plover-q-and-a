import pytest

from plover_q_and_a import sign


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
def speaker_following_interrupt_type(speaker_arg):
    return speaker_arg + ["FOLLOWING_INTERRUPT"]

@pytest.fixture
def speaker_following_statement_type(speaker_arg):
    return speaker_arg + ["FOLLOWING_STATEMENT"]

@pytest.fixture
def speaker_following_question_type(speaker_arg):
    return speaker_arg + ["FOLLOWING_INTERROGATIVE"]

# Config

@pytest.fixture
def blank_config():
    return {}

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
def speaker_following_interrupt_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOLLOWING_INTERRUPT_FOR": lambda speaker_name: (
            f"--\n\t{speaker_name}:  "
        )
    }

@pytest.fixture
def speaker_following_statement_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOLLOWING_STATEMENT_FOR": lambda speaker_name: (
            f".\n\t{speaker_name}:  "
        )
    }

@pytest.fixture
def speaker_following_question_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOLLOWING_INTERROGATIVE_FOR": lambda speaker_name: (
            f"?\n\t{speaker_name}:  "
        )
    }

# Tests

def test_blank_sign_type_args(blank_sign_type_speaker_args, blank_config):
    with pytest.raises(ValueError, match="No sign type provided"):
        sign.text(blank_sign_type_speaker_args, blank_config)

def test_unknown_speaker_type(initial_speaker_type, unknown_speaker_config):
    with pytest.raises(
        ValueError,
        match="Unknown speaker type provided: WITNESS"
    ):
        sign.text(initial_speaker_type, unknown_speaker_config)

def test_unknown_sign_type_args(
    unknown_sign_type_speaker_args,
    speaker_config
):
    with pytest.raises(
        ValueError,
        match="Unknown sign type provided for WITNESS: UNKNOWN"
    ):
        sign.text(unknown_sign_type_speaker_args, speaker_config)

def test_initial_speaker(initial_speaker_type, initial_speaker_config):
    assert (
        sign.text(
            initial_speaker_type,
            initial_speaker_config
        ) == ("SPEAKER", "\tTHE WITNESS:  ")
    )

def test_interrupting_speaker(
    speaker_following_interrupt_type,
    speaker_following_interrupt_config
):
    assert (
        sign.text(
            speaker_following_interrupt_type,
            speaker_following_interrupt_config
        ) == ("SPEAKER", "--\n\tTHE WITNESS:  ")
    )

def test_speaker_following_statement(
    speaker_following_statement_type,
    speaker_following_statement_config
):
    assert (
        sign.text(
            speaker_following_statement_type,
            speaker_following_statement_config
        ) == ("SPEAKER", ".\n\tTHE WITNESS:  ")
    )

def test_speaker_following_question(
    speaker_following_question_type,
    speaker_following_question_config
):
    assert (
        sign.text(
            speaker_following_question_type,
            speaker_following_question_config
        ) == ("SPEAKER", "?\n\tTHE WITNESS:  ")
    )
