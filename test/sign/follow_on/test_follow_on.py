import pytest

from plover_q_and_a import sign


def test_no_follow_on_args(no_follow_on_args_type, no_follow_on_args_config):
    assert (
        sign.text(None, no_follow_on_args_type, no_follow_on_args_config)
        == ("QUESTION", ".\n\tQ\t")
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
        sign.text(None, too_few_follow_on_args_type, follow_on_args_config)

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
        sign.text(None, too_many_follow_on_args_type, follow_on_args_config)

def test_unknown_follow_on_action(
    unknown_follow_on_action_type,
    follow_on_args_config
):
    with pytest.raises(
        ValueError,
        match="Unknown follow on action provided: SHOUT"
    ):
        sign.text(None, unknown_follow_on_action_type, follow_on_args_config)
