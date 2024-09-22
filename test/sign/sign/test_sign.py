import pytest

from plover_q_and_a import sign


def test_blank_args(blank_args, blank_config):
    with pytest.raises(ValueError, match="No sign type provided"):
        sign.text(None, blank_args, blank_config)

def test_unknown_args(unknown_args, blank_config):
    with pytest.raises(ValueError, match="Unknown sign type provided: UNKNOWN"):
        sign.text(None, unknown_args, blank_config)
