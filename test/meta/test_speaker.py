import pytest

from plover_q_and_a import meta

# Command Arguments

@pytest.fixture
def speaker_arg():
    return "WITNESS"

@pytest.fixture
def blank_sign_type_speaker_args(speaker_arg):
    return speaker_arg + ":"

@pytest.fixture
def unknown_sign_type_speaker_args(blank_sign_type_speaker_args):
    return blank_sign_type_speaker_args + "UNKNOWN"

@pytest.fixture
def initial_speaker_type(blank_sign_type_speaker_args):
    return blank_sign_type_speaker_args + "INITIAL"

@pytest.fixture
def interrupting_speaker_type(blank_sign_type_speaker_args):
    return blank_sign_type_speaker_args + "INTERRUPTING"

@pytest.fixture
def speaker_following_statement_type(blank_sign_type_speaker_args):
    return blank_sign_type_speaker_args + "FOLLOWING_STATEMENT"

@pytest.fixture
def speaker_following_question_type(blank_sign_type_speaker_args):
    return blank_sign_type_speaker_args + "FOLLOWING_QUESTION"

# Config

@pytest.fixture
def blank_config():
    return {}

@pytest.fixture
def unknown_speaker_config():
    return {
        "SPEAKER_NAMES": {
            "COURT": "THE COURT"
        }
    }

@pytest.fixture
def speaker_config():
    return {
        "SPEAKER_NAMES": {
            "WITNESS": "THE WITNESS"
        }
    }

@pytest.fixture
def initial_speaker_config(speaker_config):
    return speaker_config | {
        "SPEAKER": lambda speaker_name: f"\t{speaker_name}:  "
    }

@pytest.fixture
def interrupting_speaker_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOLLOWING_INTERRUPT": lambda speaker_name: (
            f"--\n\t{speaker_name}:  "
        )
    }

@pytest.fixture
def speaker_following_statement_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOLLOWING_STATEMENT": lambda speaker_name: (
            f".\n\t{speaker_name}:  "
        )
    }

@pytest.fixture
def speaker_following_question_config(speaker_config):
    return speaker_config | {
        "SPEAKER_FOLLOWING_QUESTION": lambda speaker_name: (
            f"?\n\t{speaker_name}:  "
        )
    }

# Tests

def test_blank_sign_type_args(blank_sign_type_speaker_args, blank_config):
    with pytest.raises(ValueError, match="No sign type provided"):
        meta.sign(blank_sign_type_speaker_args, blank_config)

def test_unknown_speaker_type(initial_speaker_type, unknown_speaker_config):
    with pytest.raises(
        ValueError,
        match="Unknown speaker type provided: WITNESS"
    ):
        meta.sign(initial_speaker_type, unknown_speaker_config)

def test_unknown_sign_type_args(
    unknown_sign_type_speaker_args,
    speaker_config
):
    with pytest.raises(
        ValueError,
        match="Unknown sign type provided for WITNESS: UNKNOWN"
    ):
        meta.sign(unknown_sign_type_speaker_args, speaker_config)

def test_initial_speaker(initial_speaker_type, initial_speaker_config):
    assert (
        meta.sign(
            initial_speaker_type,
            initial_speaker_config
        ) == "\tTHE WITNESS:  "
    )

def test_interrupting_speaker(
    interrupting_speaker_type,
    interrupting_speaker_config
):
    assert (
        meta.sign(
            interrupting_speaker_type,
            interrupting_speaker_config
        ) == "--\n\tTHE WITNESS:  "
    )

def test_speaker_following_statement(
    speaker_following_statement_type,
    speaker_following_statement_config
):
    assert (
        meta.sign(
            speaker_following_statement_type,
            speaker_following_statement_config
        ) == ".\n\tTHE WITNESS:  "
    )

def test_speaker_following_question(
    speaker_following_question_type,
    speaker_following_question_config
):
    assert (
        meta.sign(
            speaker_following_question_type,
            speaker_following_question_config
        ) == "?\n\tTHE WITNESS:  "
    )
