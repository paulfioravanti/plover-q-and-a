import pytest

from plover_q_and_a import meta

# Command Arguments

@pytest.fixture
def question_arg():
    return ["QUESTION"]

@pytest.fixture
def blank_question_type(question_arg):
    return question_arg + [""]

@pytest.fixture
def unknown_question_type(question_arg):
    return question_arg + ["UNKNOWN"]

@pytest.fixture
def initial_question_type(question_arg):
    return question_arg + ["INITIAL"]

@pytest.fixture
def interrupting_question_type(question_arg):
    return question_arg + ["INTERRUPTING"]

@pytest.fixture
def question_following_statement_type(question_arg):
    return question_arg + ["FOLLOWING_STATEMENT"]

@pytest.fixture
def question_following_statement_then_yield_to_answer_type(
    question_following_statement_type
):
    return question_following_statement_type + ["YIELD_AFTER", "Okay"]

@pytest.fixture
def question_following_statement_then_elaborate_type(
    question_following_statement_type
):
    return question_following_statement_type + ["ELABORATE_AFTER", "All right"]

@pytest.fixture
def question_following_question_type(question_arg):
    return question_arg + ["FOLLOWING_QUESTION"]

@pytest.fixture
def question_following_question_then_yield_to_answer_type(
    question_following_question_type
):
    return question_following_question_type + ["YIELD_AFTER", "Okay"]

@pytest.fixture
def question_following_question_then_elaborate_type(
    question_following_question_type
):
    return question_following_question_type + ["ELABORATE_AFTER", "All right"]

# Config

@pytest.fixture
def blank_config():
    return {}

@pytest.fixture
def initial_question_config():
    return { "QUESTION": "\tQ\t" }

@pytest.fixture
def interrupting_question_config():
    return { "QUESTION_FOLLOWING_INTERRUPT": "--\n\tQ\t" }

@pytest.fixture
def question_following_statement_config():
    return { "QUESTION_FOLLOWING_STATEMENT": ".\n\tQ\t" }

@pytest.fixture
def answer_following_question_config():
    return { "ANSWER_FOLLOWING_QUESTION": "?\n\tA\t" }

@pytest.fixture
def question_following_statement_then_yield_to_answer_config(
    question_following_statement_config,
    answer_following_question_config
):
    return (
        question_following_statement_config
        | answer_following_question_config
    )

@pytest.fixture
def statement_elaborate_config():
    return { "STATEMENT_ELABORATE": ". " }

@pytest.fixture
def question_following_statement_then_elaborate_config(
    question_following_statement_config,
    statement_elaborate_config
):
    return question_following_statement_config | statement_elaborate_config

@pytest.fixture
def question_following_question_config():
    return { "QUESTION_FOLLOWING_QUESTION": "?\n\tQ\t" }

@pytest.fixture
def question_following_question_then_yield_to_answer_config(
    question_following_question_config,
    answer_following_question_config
):
    return (
        question_following_question_config
        | answer_following_question_config
    )

@pytest.fixture
def question_following_question_then_elaborate_config(
    question_following_question_config,
    statement_elaborate_config
):
    return question_following_question_config | statement_elaborate_config

# Tests

def test_missing_question_args(question_arg, blank_config):
    with pytest.raises(ValueError, match="No question args provided"):
        meta.sign(question_arg, blank_config)

def test_blank_question_type(blank_question_type, blank_config):
    with pytest.raises(ValueError, match="No question type provided"):
        meta.sign(blank_question_type, blank_config)

def test_unknown_question_type(unknown_question_type, blank_config):
    with pytest.raises(
        ValueError, match="Unknown question type provided: UNKNOWN"
    ):
        meta.sign(unknown_question_type, blank_config)

def test_initial_question(initial_question_type, initial_question_config):
    assert (
        meta.sign(initial_question_type, initial_question_config) == "\tQ\t"
    )

def test_question_following_interrupt(
    interrupting_question_type,
    interrupting_question_config
):
    assert (
        meta.sign(
            interrupting_question_type,
            interrupting_question_config
        ) == "--\n\tQ\t"
   )

def test_question_following_statement(
    question_following_statement_type,
    question_following_statement_config
):
    assert (
        meta.sign(
          question_following_statement_type,
          question_following_statement_config
        ) == ".\n\tQ\t"
   )

def test_question_following_statement_then_yield_to_answer(
    question_following_statement_then_yield_to_answer_type,
    question_following_statement_then_yield_to_answer_config
):
    assert (
        meta.sign(
          question_following_statement_then_yield_to_answer_type,
          question_following_statement_then_yield_to_answer_config
        ) == ".\n\tQ\tOkay?\n\tA\t"
   )

def test_question_following_statement_then_elaborate(
    question_following_statement_then_elaborate_type,
    question_following_statement_then_elaborate_config
):
    assert (
        meta.sign(
            question_following_statement_then_elaborate_type,
            question_following_statement_then_elaborate_config
        ) == ".\n\tQ\tAll right. "
   )

def test_question_following_question(
    question_following_question_type,
    question_following_question_config
):
    assert (
        meta.sign(
          question_following_question_type,
          question_following_question_config
        ) == "?\n\tQ\t"
   )

def test_question_following_question_then_yield_to_answer(
    question_following_question_then_yield_to_answer_type,
    question_following_question_then_yield_to_answer_config
):
    assert (
        meta.sign(
          question_following_question_then_yield_to_answer_type,
          question_following_question_then_yield_to_answer_config
        ) == "?\n\tQ\tOkay?\n\tA\t"
   )

def test_question_following_question_then_elaborate(
    question_following_question_then_elaborate_type,
    question_following_question_then_elaborate_config
):
    assert (
        meta.sign(
            question_following_question_then_elaborate_type,
            question_following_question_then_elaborate_config
        ) == "?\n\tQ\tAll right. "
   )
