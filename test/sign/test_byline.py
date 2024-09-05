import pytest

from plover_q_and_a import sign


# Command Arguments

@pytest.fixture
def byline_arg():
    return ["BYLINE"]

@pytest.fixture
def too_few_byline_args(byline_arg):
    return byline_arg + ["PLAINTIFF_1"]

@pytest.fixture
def too_many_byline_args(too_few_byline_args):
    return too_few_byline_args + ["Foo", "Bar"]

@pytest.fixture
def blank_speaker_type_byline_args(byline_arg):
    return byline_arg + ["", "INITIAL"]

@pytest.fixture
def blank_sign_type_byline_args(byline_arg):
    return byline_arg + ["PLAINTIFF_1", ""]

@pytest.fixture
def unknown_speaker_type_byline_args(byline_arg):
    return byline_arg + ["WITNESS", "INITIAL"]

@pytest.fixture
def unknown_sign_type_byline_args(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "UNKNOWN"]

@pytest.fixture
def initial_byline_type(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "INITIAL"]

@pytest.fixture
def byline_following_interrupt_type(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "FOLLOWING_INTERRUPT"]

@pytest.fixture
def byline_following_statement_type(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "FOLLOWING_STATEMENT"]

@pytest.fixture
def byline_following_question_type(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "FOLLOWING_INTERROGATIVE"]

# Config

@pytest.fixture
def blank_config():
    return {}

@pytest.fixture
def byline_speaker_config():
    return {
        "speaker_names": {
            "PLAINTIFF_1": "MR. STPHAO"
        }
    }

@pytest.fixture
def no_byline_speaker_name_config_for_speaker_type():
    return {
        "speaker_names": {
            "PLAINTIFF_2": "MR. SKWRAO"
        }
    }

@pytest.fixture
def initial_byline_config(byline_speaker_config):
    return byline_speaker_config | {
        "BYLINE_FOR": lambda speaker_name: f"BY {speaker_name}:\n\tQ\t"
    }

@pytest.fixture
def byline_following_interrupt_config(byline_speaker_config):
    return byline_speaker_config | {
        "BYLINE_FOLLOWING_INTERRUPT_FOR": lambda speaker_name: (
            f"--\nBY {speaker_name}:\n\tQ\t"
        )
    }

@pytest.fixture
def byline_following_statement_config(byline_speaker_config):
    return byline_speaker_config | {
        "BYLINE_FOLLOWING_STATEMENT_FOR": lambda speaker_name: (
            f".\nBY {speaker_name}:\n\tQ\t"
        )
    }

@pytest.fixture
def byline_following_question_config(byline_speaker_config):
    return byline_speaker_config | {
        "BYLINE_FOLLOWING_INTERROGATIVE_FOR": lambda speaker_name: (
            f"?\nBY {speaker_name}:\n\tQ\t"
        )
    }

# Tests

def test_missing_byline_args(byline_arg, blank_config):
    with pytest.raises(
        ValueError,
        match="Two byline arguments must be provided. You gave: "
    ):
        sign.text(byline_arg, blank_config)

def test_too_few_byline_args(too_few_byline_args, blank_config):
    with pytest.raises(
        ValueError,
        match="Two byline arguments must be provided. You gave: PLAINTIFF_1"
    ):
        sign.text(too_few_byline_args, blank_config)

def test_too_many_byline_args(too_many_byline_args, blank_config):
    with pytest.raises(
        ValueError,
        match=(
            "Two byline arguments must be provided. "
            "You gave: PLAINTIFF_1:Foo:Bar"
        )
    ):
        sign.text(too_many_byline_args, blank_config)

def test_blank_speaker_type_args(blank_speaker_type_byline_args, blank_config):
    with pytest.raises(ValueError, match="No speaker type provided"):
        sign.text(blank_speaker_type_byline_args, blank_config)

def test_blank_sign_type_args(blank_sign_type_byline_args, blank_config):
    with pytest.raises(ValueError, match="No sign type provided"):
        sign.text(blank_sign_type_byline_args, blank_config)

def test_unknown_speaker_type_args(
    unknown_speaker_type_byline_args,
    byline_speaker_config
):
    with pytest.raises(
        ValueError,
        match="Unknown byline speaker type provided: WITNESS"
    ):
        sign.text(unknown_speaker_type_byline_args, byline_speaker_config)

def test_unknown_sign_type_args(
    unknown_sign_type_byline_args,
    byline_speaker_config
):
    with pytest.raises(
        ValueError,
        match="Unknown sign type provided for PLAINTIFF_1 byline: UNKNOWN"
    ):
        sign.text(unknown_sign_type_byline_args, byline_speaker_config)

def test_no_speaker_name_config_for_speaker_type(
    initial_byline_type,
    no_byline_speaker_name_config_for_speaker_type
):
    with pytest.raises(
        ValueError,
        match="No speaker name entry for: PLAINTIFF_1"
    ):
        sign.text(
            initial_byline_type,
            no_byline_speaker_name_config_for_speaker_type
        )

def test_initial_byline(initial_byline_type, initial_byline_config):
    assert (
        sign.text(
            initial_byline_type,
            initial_byline_config
        ) == ("QUESTION", "BY MR. STPHAO:\n\tQ\t")
    )

def test_byline_following_interrupt(
    byline_following_interrupt_type,
    byline_following_interrupt_config
):
    assert (
        sign.text(
            byline_following_interrupt_type,
            byline_following_interrupt_config
        ) == ("QUESTION", "--\nBY MR. STPHAO:\n\tQ\t")
    )

def test_byline_following_statement(
    byline_following_statement_type,
    byline_following_statement_config
):
    assert (
        sign.text(
            byline_following_statement_type,
            byline_following_statement_config
        ) == ("QUESTION", ".\nBY MR. STPHAO:\n\tQ\t")
    )

def test_byline_following_question(
    byline_following_question_type,
    byline_following_question_config
):
    assert (
        sign.text(
            byline_following_question_type,
            byline_following_question_config
        ) == ("QUESTION", "?\nBY MR. STPHAO:\n\tQ\t")
    )
