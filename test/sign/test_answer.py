import pytest

from plover_q_and_a import sign


# Command Arguments

@pytest.fixture
def answer_arg():
    return ["ANSWER"]

@pytest.fixture
def blank_answer_type(answer_arg):
    return answer_arg + [""]

@pytest.fixture
def unknown_answer_type(answer_arg):
    return answer_arg + ["UNKNOWN"]

@pytest.fixture
def answer_following_interrupt_type(answer_arg):
    return answer_arg + ["FOLLOWING_INTERRUPT"]

@pytest.fixture
def answer_following_statement_type(answer_arg):
    return answer_arg + ["FOLLOWING_STATEMENT"]

@pytest.fixture
def answer_following_statement_then_yield_to_question_type(
    answer_following_statement_type
):
    return answer_following_statement_type + ["YIELD_AFTER", "Okay"]

@pytest.fixture
def answer_following_statement_then_elaborate_type(
    answer_following_statement_type
):
    return answer_following_statement_type + ["ELABORATE_AFTER", "All right"]

@pytest.fixture
def answer_following_question_type(answer_arg):
    return answer_arg + ["FOLLOWING_INTERROGATIVE"]

@pytest.fixture
def answer_following_question_then_yield_to_question_type(
    answer_following_question_type
):
    return answer_following_question_type + ["YIELD_AFTER", "Okay"]

@pytest.fixture
def answer_following_question_then_elaborate_type(
    answer_following_question_type
):
    return answer_following_question_type + ["ELABORATE_AFTER", "All right"]

# Config

@pytest.fixture
def blank_config():
    return {}

@pytest.fixture
def answer_following_interrupt_config():
    return { "ANSWER_FOLLOWING_INTERRUPT": " --\n\tA\t" }

@pytest.fixture
def answer_following_statement_config():
    return { "ANSWER_FOLLOWING_STATEMENT": ".\n\tA\t" }

@pytest.fixture
def question_following_statement_config():
    return { "QUESTION_FOLLOWING_STATEMENT": ".\n\tQ\t" }

@pytest.fixture
def answer_following_statement_then_yield_to_question_config(
    answer_following_statement_config,
    question_following_statement_config
):
    return (
        answer_following_statement_config
        | question_following_statement_config
    )

@pytest.fixture
def statement_elaborate_config():
    return { "STATEMENT_ELABORATE": ". " }

@pytest.fixture
def answer_following_statement_then_elaborate_config(
    answer_following_statement_config,
    statement_elaborate_config
):
    return answer_following_statement_config | statement_elaborate_config

@pytest.fixture
def answer_following_question_config():
    return { "ANSWER_FOLLOWING_INTERROGATIVE": "?\n\tA\t" }

@pytest.fixture
def answer_following_question_then_yield_to_question_config(
    answer_following_question_config,
    question_following_statement_config
):
    return (
        answer_following_question_config
        | question_following_statement_config
    )

@pytest.fixture
def answer_following_question_then_elaborate_config(
    answer_following_question_config,
    statement_elaborate_config
):
    return answer_following_question_config | statement_elaborate_config

# Tests

def test_missing_answer_args(answer_arg, blank_config):
    with pytest.raises(ValueError, match="No answer args provided"):
        sign.text(answer_arg, blank_config)

def test_blank_answer_type(blank_answer_type, blank_config):
    with pytest.raises(ValueError, match="No answer type provided"):
        sign.text(blank_answer_type, blank_config)

def test_unknown_answer_type(unknown_answer_type, blank_config):
    with pytest.raises(
        ValueError,
        match="Unknown answer type provided: UNKNOWN"
    ):
        sign.text(unknown_answer_type, blank_config)

def test_answer_following_interrupt(
    answer_following_interrupt_type,
    answer_following_interrupt_config
):
    assert (
        sign.text(
            answer_following_interrupt_type,
            answer_following_interrupt_config
        )
        == ("ANSWER", " --\n\tA\t")
   )

def test_answer_following_statement(
    answer_following_statement_type,
    answer_following_statement_config
):
    assert (
        sign.text(
          answer_following_statement_type,
          answer_following_statement_config
        ) == ("ANSWER", ".\n\tA\t")
   )

def test_answer_following_statement_then_yield_to_question(
    answer_following_statement_then_yield_to_question_type,
    answer_following_statement_then_yield_to_question_config
):
    assert (
        sign.text(
          answer_following_statement_then_yield_to_question_type,
          answer_following_statement_then_yield_to_question_config
        ) == ("QUESTION", ".\n\tA\tOkay.\n\tQ\t")
   )

def test_answer_following_statement_then_elaborate(
    answer_following_statement_then_elaborate_type,
    answer_following_statement_then_elaborate_config
):
    assert (
        sign.text(
            answer_following_statement_then_elaborate_type,
            answer_following_statement_then_elaborate_config
        ) == ("ANSWER", ".\n\tA\tAll right. ")
   )

def test_answer_following_question(
    answer_following_question_type,
    answer_following_question_config
):
    assert (
        sign.text(
          answer_following_question_type,
          answer_following_question_config
        ) == ("ANSWER", "?\n\tA\t")
   )

def test_answer_following_question_then_yield_to_question(
    answer_following_question_then_yield_to_question_type,
    answer_following_question_then_yield_to_question_config
):
    assert (
        sign.text(
          answer_following_question_then_yield_to_question_type,
          answer_following_question_then_yield_to_question_config
        ) == ("QUESTION", "?\n\tA\tOkay.\n\tQ\t")
   )

def test_answer_following_question_then_elaborate(
    answer_following_question_then_elaborate_type,
    answer_following_question_then_elaborate_config
):
    assert (
        sign.text(
          answer_following_question_then_elaborate_type,
          answer_following_question_then_elaborate_config
        ) == ("ANSWER", "?\n\tA\tAll right. ")
   )
