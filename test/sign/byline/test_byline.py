import pytest

from plover_q_and_a import sign


def test_missing_byline_args(byline_arg, blank_config):
    with pytest.raises(
        ValueError,
        match="Two byline arguments must be provided. You gave: "
    ):
        sign.text(None, byline_arg, blank_config)

def test_too_few_byline_args(too_few_byline_args, blank_config):
    with pytest.raises(
        ValueError,
        match="Two byline arguments must be provided. You gave: PLAINTIFF_1"
    ):
        sign.text(None, too_few_byline_args, blank_config)

def test_too_many_byline_args(too_many_byline_args, blank_config):
    with pytest.raises(
        ValueError,
        match=(
            "Two byline arguments must be provided. "
            "You gave: PLAINTIFF_1:Foo:Bar"
        )
    ):
        sign.text(None, too_many_byline_args, blank_config)

def test_blank_speaker_type_args(blank_speaker_type_byline_args, blank_config):
    with pytest.raises(ValueError, match="No speaker type provided"):
        sign.text(None, blank_speaker_type_byline_args, blank_config)

def test_blank_sign_type_args(blank_sign_type_byline_args, blank_config):
    with pytest.raises(ValueError, match="No sign type provided"):
        sign.text(None, blank_sign_type_byline_args, blank_config)

def test_unknown_speaker_type_args(
    unknown_speaker_type_byline_args,
    question_byline_speaker_config
):
    with pytest.raises(
        ValueError,
        match="Unknown byline speaker type provided: COURT"
    ):
        sign.text(
            None,
            unknown_speaker_type_byline_args,
            question_byline_speaker_config
        )

def test_unknown_sign_type_args(
    unknown_sign_type_byline_args,
    question_byline_speaker_config
):
    with pytest.raises(
        ValueError,
        match="Unknown sign type provided for PLAINTIFF_1 byline: UNKNOWN"
    ):
        sign.text(
            None,
            unknown_sign_type_byline_args,
            question_byline_speaker_config
        )

def test_no_speaker_name_config_for_speaker_type(
    initial_byline_type,
    no_byline_speaker_name_config_for_speaker_type
):
    with pytest.raises(
        ValueError,
        match="No speaker name entry for: PLAINTIFF_1"
    ):
        sign.text(
            None,
            initial_byline_type,
            no_byline_speaker_name_config_for_speaker_type
        )

def test_initial_question_byline(initial_byline_type, initial_byline_config):
    assert (
        sign.text(
            None,
            initial_byline_type,
            initial_byline_config
        ) == ("QUESTION", "BY MR. STPHAO:\n\tQ\t")
    )

def test_question_byline_following_interrogative(
    question_byline_following_interrogative_type,
    question_byline_following_interrogative_config
):
    assert (
        sign.text(
            None,
            question_byline_following_interrogative_type,
            question_byline_following_interrogative_config
        ) == ("QUESTION", "?\nBY MR. STPHAO:\n\tQ\t")
    )

def test_question_byline_following_statement(
    question_byline_following_statement_type,
    question_byline_following_statement_config
):
    assert (
        sign.text(
            None,
            question_byline_following_statement_type,
            question_byline_following_statement_config
        ) == ("QUESTION", ".\nBY MR. STPHAO:\n\tQ\t")
    )

def test_question_byline_following_interrupt(
    question_byline_following_interrupt_type,
    question_byline_following_interrupt_config
):
    assert (
        sign.text(
            None,
            question_byline_following_interrupt_type,
            question_byline_following_interrupt_config
        ) == ("QUESTION", "--\nBY MR. STPHAO:\n\tQ\t")
    )

def test_answer_byline_following_interrogative(
    answer_byline_following_interrogative_type,
    answer_byline_following_interrogative_config
):
    assert (
        sign.text(
            None,
            answer_byline_following_interrogative_type,
            answer_byline_following_interrogative_config
        ) == ("ANSWER", "?\nTHE WITNESS:\tA\t")
    )

def test_answer_byline_following_statement(
    answer_byline_following_statement_type,
    answer_byline_following_statement_config
):
    assert (
        sign.text(
            None,
            answer_byline_following_statement_type,
            answer_byline_following_statement_config
        ) == ("ANSWER", ".\nTHE WITNESS:\tA\t")
    )

def test_answer_byline_following_interrupt(
    answer_byline_following_interrupt_type,
    answer_byline_following_interrupt_config
):
    assert (
        sign.text(
            None,
            answer_byline_following_interrupt_type,
            answer_byline_following_interrupt_config
        ) == ("ANSWER", "--\nTHE WITNESS:\tA\t")
    )
