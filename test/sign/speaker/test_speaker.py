import pytest

from plover_q_and_a import sign


def test_blank_sign_type_args(blank_sign_type_speaker_args, blank_config):
    with pytest.raises(ValueError, match="No sign type provided"):
        sign.text("", blank_sign_type_speaker_args, blank_config)

def test_unknown_speaker_type(initial_speaker_type, unknown_speaker_config):
    with pytest.raises(
        ValueError,
        match="Unknown speaker type provided: WITNESS"
    ):
        sign.text("", initial_speaker_type, unknown_speaker_config)

def test_unknown_sign_type_args(
    unknown_sign_type_speaker_args,
    speaker_config
):
    with pytest.raises(
        ValueError,
        match="Unknown sign type provided for WITNESS: UNKNOWN"
    ):
        sign.text("", unknown_sign_type_speaker_args, speaker_config)

def test_initial_speaker(initial_speaker_type, initial_speaker_config):
    assert (
        sign.text(
            "",
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
            "",
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
            "",
            speaker_following_statement_type,
            speaker_following_statement_config
        ) == ("SPEAKER", ".\n\tTHE WITNESS:  ")
    )

def test_speaker_following_interrogative(
    speaker_following_interrogative_type,
    speaker_following_interrogative_config
):
    assert (
        sign.text(
            "QUESTION",
            speaker_following_interrogative_type,
            speaker_following_interrogative_config
        ) == ("SPEAKER", "?\n\tTHE WITNESS:  ")
    )
