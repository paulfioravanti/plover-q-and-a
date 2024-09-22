import pytest

from plover_q_and_a import sign


def test_missing_answer_args(answer_arg, blank_config):
    with pytest.raises(ValueError, match="No answer args provided"):
        sign.text(None, answer_arg, blank_config)

def test_blank_answer_type(blank_answer_type, blank_config):
    with pytest.raises(ValueError, match="No answer type provided"):
        sign.text(None, blank_answer_type, blank_config)

def test_unknown_answer_type(unknown_answer_type, blank_config):
    with pytest.raises(
        ValueError,
        match="Unknown answer type provided: UNKNOWN"
    ):
        sign.text(None, unknown_answer_type, blank_config)

def test_answer_following_interrogative(
    answer_following_interrogative_type,
    answer_following_interrogative_config
):
    assert (
        sign.text(
          None,
          answer_following_interrogative_type,
          answer_following_interrogative_config
        ) == ("ANSWER", "?\n\tA\t")
   )

def test_answer_following_interrogative_then_yield_to_question(
    answer_following_interrogative_then_yield_to_question_type,
    answer_following_interrogative_then_yield_to_question_config
):
    assert (
        sign.text(
          None,
          answer_following_interrogative_then_yield_to_question_type,
          answer_following_interrogative_then_yield_to_question_config
        ) == ("QUESTION", "?\n\tA\tOkay.\n\tQ\t")
   )

def test_answer_following_interrogative_then_elaborate(
    answer_following_interrogative_then_elaborate_type,
    answer_following_interrogative_then_elaborate_config
):
    assert (
        sign.text(
          None,
          answer_following_interrogative_then_elaborate_type,
          answer_following_interrogative_then_elaborate_config
        ) == ("ANSWER", "?\n\tA\tAll right. ")
   )

def test_answer_following_statement(
    answer_following_statement_type,
    answer_following_statement_config
):
    assert (
        sign.text(
          None,
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
          None,
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
            None,
            answer_following_statement_then_elaborate_type,
            answer_following_statement_then_elaborate_config
        ) == ("ANSWER", ".\n\tA\tAll right. ")
   )

def test_answer_following_interrupt(
    answer_following_interrupt_type,
    answer_following_interrupt_config
):
    assert (
        sign.text(
            None,
            answer_following_interrupt_type,
            answer_following_interrupt_config
        )
        == ("ANSWER", " --\n\tA\t")
   )
