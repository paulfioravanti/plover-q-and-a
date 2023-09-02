import pytest

from plover_q_and_a import meta

# Command Arguments

@pytest.fixture
def byline_arg():
    return "BYLINE"

@pytest.fixture
def too_few_byline_args(byline_arg):
    return byline_arg + ":PLAINTIFF_1"

@pytest.fixture
def too_many_byline_args(too_few_byline_args):
    return too_few_byline_args + ":Foo:Bar"

@pytest.fixture
def blank_speaker_type_byline_args(byline_arg):
    return byline_arg + "::INITIAL"

@pytest.fixture
def blank_sign_type_byline_args(byline_arg):
    return byline_arg + ":PLAINTIFF_1:"

@pytest.fixture
def unknown_speaker_type_byline_args(byline_arg):
    return byline_arg + ":WITNESS:INITIAL"

@pytest.fixture
def unknown_sign_type_byline_args(blank_sign_type_byline_args):
    return blank_sign_type_byline_args + "UNKNOWN"

@pytest.fixture
def initial_byline_type(blank_sign_type_byline_args):
    return blank_sign_type_byline_args + "INITIAL"

@pytest.fixture
def interrupting_byline_type(blank_sign_type_byline_args):
    return blank_sign_type_byline_args + "INTERRUPTING"

@pytest.fixture
def byline_following_statement_type(blank_sign_type_byline_args):
    return blank_sign_type_byline_args + "FOLLOWING_STATEMENT"

@pytest.fixture
def byline_following_question_type(blank_sign_type_byline_args):
    return blank_sign_type_byline_args + "FOLLOWING_QUESTION"

# Config

@pytest.fixture
def blank_config():
    return {}

@pytest.fixture
def byline_speaker_config():
    return {
        "BYLINE_SPEAKER_NAMES": {
            "PLAINTIFF_1": "MR. STPHAO"
        }
    }

@pytest.fixture
def initial_byline_config(byline_speaker_config):
    return byline_speaker_config | {
        "BYLINE": lambda speaker_name: f"BY {speaker_name}:\n\tQ\t"
    }

@pytest.fixture
def interrupting_byline_config(byline_speaker_config):
    return byline_speaker_config | {
        "BYLINE_FOLLOWING_INTERRUPT": lambda speaker_name: (
            f"--\nBY {speaker_name}:\n\tQ\t"
        )
    }

@pytest.fixture
def byline_following_statement_config(byline_speaker_config):
    return byline_speaker_config | {
        "BYLINE_FOLLOWING_STATEMENT": lambda speaker_name: (
            f".\nBY {speaker_name}:\n\tQ\t"
        )
    }

@pytest.fixture
def byline_following_question_config(byline_speaker_config):
    return byline_speaker_config | {
        "BYLINE_FOLLOWING_QUESTION": lambda speaker_name: (
            f"?\nBY {speaker_name}:\n\tQ\t"
        )
    }

# Tests

def test_missing_byline_args(byline_arg, blank_config):
    with pytest.raises(
        ValueError,
        match="Two byline arguments must be provided. You gave: "
    ):
        meta.sign(byline_arg, blank_config)

def test_too_few_byline_args(too_few_byline_args, blank_config):
    with pytest.raises(
        ValueError,
        match="Two byline arguments must be provided. You gave: PLAINTIFF_1"
    ):
        meta.sign(too_few_byline_args, blank_config)

def test_too_many_byline_args(too_many_byline_args, blank_config):
    with pytest.raises(
        ValueError,
        match="Two byline arguments must be provided. You gave: PLAINTIFF_1:Foo:Bar"
    ):
        meta.sign(too_many_byline_args, blank_config)

def test_blank_speaker_type_args(blank_speaker_type_byline_args, blank_config):
    with pytest.raises(ValueError, match="No speaker type provided"):
        meta.sign(blank_speaker_type_byline_args, blank_config)

def test_blank_sign_type_args(blank_sign_type_byline_args, blank_config):
    with pytest.raises(ValueError, match="No sign type provided"):
        meta.sign(blank_sign_type_byline_args, blank_config)

def test_unknown_speaker_type_args(
    unknown_speaker_type_byline_args,
    byline_speaker_config
):
    with pytest.raises(
        ValueError,
        match="Unknown speaker type for byline provided: WITNESS"
    ):
        meta.sign(unknown_speaker_type_byline_args, byline_speaker_config)

def test_unknown_sign_type_args(
    unknown_sign_type_byline_args,
    byline_speaker_config
):
    with pytest.raises(
        ValueError,
        match="Unknown sign type provided for PLAINTIFF_1 byline: UNKNOWN"
    ):
        meta.sign(unknown_sign_type_byline_args, byline_speaker_config)

def test_initial_byline(initial_byline_type, initial_byline_config):
    assert (
        meta.sign(
            initial_byline_type,
            initial_byline_config
        ) == "BY MR. STPHAO:\n\tQ\t"
    )

def test_interrupting_byline(
    interrupting_byline_type,
    interrupting_byline_config
):
    assert (
        meta.sign(
            interrupting_byline_type,
            interrupting_byline_config
        ) == "--\nBY MR. STPHAO:\n\tQ\t"
    )

def test_byline_following_statement(
    byline_following_statement_type,
    byline_following_statement_config
):
    assert (
        meta.sign(
            byline_following_statement_type,
            byline_following_statement_config
        ) == ".\nBY MR. STPHAO:\n\tQ\t"
    )

def test_byline_following_question(
    byline_following_question_type,
    byline_following_question_config
):
    assert (
        meta.sign(
            byline_following_question_type,
            byline_following_question_config
        ) == "?\nBY MR. STPHAO:\n\tQ\t"
    )
