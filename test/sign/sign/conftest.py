import pytest


@pytest.fixture
def blank_args():
    return [""]

@pytest.fixture
def unknown_args():
    return ["UNKNOWN"]
