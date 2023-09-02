import pytest

from plover_q_and_a import meta

@pytest.fixture
def blank_config():
    return {}

@pytest.fixture
def blank_args():
    return ""

@pytest.fixture
def unknown_args():
    return "UNKNOWN"

def test_blank_args(blank_args, blank_config):
    with pytest.raises(ValueError, match="No sign type provided"):
        meta.sign(blank_args, blank_config)

def test_unknown_args(unknown_args, blank_config):
    with pytest.raises(ValueError, match="Unknown sign type provided: UNKNOWN"):
        meta.sign(unknown_args, blank_config)
