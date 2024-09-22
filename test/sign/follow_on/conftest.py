import pytest


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
    return {
        "QUESTION_FOLLOWING_STATEMENT": lambda _current_sign_type: ".\n\tQ\t"
    }

@pytest.fixture
def follow_on_args_config(no_follow_on_args_config):
    return no_follow_on_args_config | {
        "STATEMENT_ELABORATE": lambda _current_sign_type: ". "
    }
