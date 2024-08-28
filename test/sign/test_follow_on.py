import pytest

from plover_q_and_a import sign


# Command Arguments

@pytest.fixture
def no_follow_on_args_type():
    return ["QUESTION", "FOLLOWING_STATEMENT"]

@pytest.fixture
def too_few_follow_on_args_type(no_follow_on_args_type):
    return no_follow_on_args_type + ["ELABORATE_AFTER"]

@pytest.fixture
def too_many_follow_on_args_type(too_few_follow_on_args_type):
    return too_few_follow_on_args_type + ["Foo", "Bar"]

@pytest.fixture
def unknown_follow_on_action_type(no_follow_on_args_type):
    return no_follow_on_args_type + ["SHOUT", "Objection"]

# Config

@pytest.fixture
def no_follow_on_args_config():
    return { "QUESTION_FOLLOWING_STATEMENT": ".\n\tQ\t" }

@pytest.fixture
def follow_on_args_config(no_follow_on_args_config):
    return no_follow_on_args_config | {
        "STATEMENT_ELABORATE": ". "
    }

# Tests

def test_no_follow_on_args(no_follow_on_args_type, no_follow_on_args_config):
    assert (
        sign.text(no_follow_on_args_type, no_follow_on_args_config)
        == ".\n\tQ\t"
    )

def test_too_few_follow_on_args(
    too_few_follow_on_args_type,
    follow_on_args_config
):
    with pytest.raises(
        ValueError,
        match=(
            "Two follow on arguments must be provided. "
            "You gave: ELABORATE_AFTER"
        )
    ):
        sign.text(too_few_follow_on_args_type, follow_on_args_config)

def test_too_many_follow_on_args(
    too_many_follow_on_args_type,
    follow_on_args_config
):
    with pytest.raises(
        ValueError,
        match=(
            "Two follow on arguments must be provided. "
            "You gave: ELABORATE_AFTER:Foo:Bar"
        )
    ):
        sign.text(too_many_follow_on_args_type, follow_on_args_config)

def test_unknown_follow_on_action(
    unknown_follow_on_action_type,
    follow_on_args_config
):
    with pytest.raises(
        ValueError,
        match="Unknown follow on action provided: SHOUT"
    ):
        sign.text(unknown_follow_on_action_type, follow_on_args_config)
