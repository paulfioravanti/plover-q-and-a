import pytest


# Command Arguments

@pytest.fixture
def byline_arg():
    return ["BYLINE"]

@pytest.fixture
def too_few_byline_args(byline_arg):
    return byline_arg + ["PLAINTIFF_1"]

@pytest.fixture
def too_many_byline_args(too_few_byline_args):
    return too_few_byline_args + ["Foo", "Bar"]

@pytest.fixture
def blank_speaker_type_byline_args(byline_arg):
    return byline_arg + ["", "INITIAL"]

@pytest.fixture
def blank_sign_type_byline_args(byline_arg):
    return byline_arg + ["PLAINTIFF_1", ""]

@pytest.fixture
def unknown_speaker_type_byline_args(byline_arg):
    return byline_arg + ["COURT", "INITIAL"]

@pytest.fixture
def unknown_sign_type_byline_args(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "UNKNOWN"]

@pytest.fixture
def initial_byline_type(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "INITIAL"]

@pytest.fixture
def question_byline_following_interrogative_type(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "FOLLOWING_INTERROGATIVE"]

@pytest.fixture
def question_byline_following_statement_type(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "FOLLOWING_STATEMENT"]

@pytest.fixture
def question_byline_following_interrupt_type(byline_arg):
    return byline_arg + ["PLAINTIFF_1", "FOLLOWING_INTERRUPT"]

@pytest.fixture
def answer_byline_following_interrogative_type(byline_arg):
    return byline_arg + ["WITNESS", "FOLLOWING_INTERROGATIVE"]

@pytest.fixture
def answer_byline_following_statement_type(byline_arg):
    return byline_arg + ["WITNESS", "FOLLOWING_STATEMENT"]

@pytest.fixture
def answer_byline_following_interrupt_type(byline_arg):
    return byline_arg + ["WITNESS", "FOLLOWING_INTERRUPT"]

# Config

@pytest.fixture
def question_byline_speaker_config():
    return {
        "speaker_names": {
            "PLAINTIFF_1": "MR. STPHAO"
        }
    }

@pytest.fixture
def answer_byline_speaker_config():
    return {
        "speaker_names": {
            "WITNESS": "THE WITNESS"
        }
    }

@pytest.fixture
def no_byline_speaker_name_config_for_speaker_type():
    return {
        "speaker_names": {
            "PLAINTIFF_2": "MR. SKWRAO"
        }
    }

@pytest.fixture
def initial_byline_config(question_byline_speaker_config):
    return question_byline_speaker_config | {
        "BYLINE_FOR": (
            lambda speaker_type, speaker_name: f"BY {speaker_name}:\n\tQ\t"
        )
    }

@pytest.fixture
def question_byline_following_interrogative_config(
    question_byline_speaker_config
):
    return question_byline_speaker_config | {
        "BYLINE_FOLLOWING_INTERROGATIVE_FOR": (
            lambda _current_sign_type, _speaker_type, speaker_name: (
                f"?\nBY {speaker_name}:\n\tQ\t"
            )
        )
    }

@pytest.fixture
def question_byline_following_statement_config(question_byline_speaker_config):
    return question_byline_speaker_config | {
        "BYLINE_FOLLOWING_STATEMENT_FOR": (
            lambda _current_sign_type, _speaker_type, speaker_name: (
                f".\nBY {speaker_name}:\n\tQ\t"
            )
        )
    }

@pytest.fixture
def question_byline_following_interrupt_config(question_byline_speaker_config):
    return question_byline_speaker_config | {
        "BYLINE_FOLLOWING_INTERRUPT_FOR": (
            lambda _current_sign_type, _speaker_type, speaker_name: (
                f"--\nBY {speaker_name}:\n\tQ\t"
            )
        )
    }

@pytest.fixture
def answer_byline_following_interrogative_config(answer_byline_speaker_config):
    return answer_byline_speaker_config | {
        "BYLINE_FOLLOWING_INTERROGATIVE_FOR": (
            lambda _current_sign_type, _speaker_type, speaker_name: (
                f"?\n{speaker_name}:\tA\t"
            )
        )
    }

@pytest.fixture
def answer_byline_following_statement_config(answer_byline_speaker_config):
    return answer_byline_speaker_config | {
        "BYLINE_FOLLOWING_STATEMENT_FOR": (
            lambda _current_sign_type, _speaker_type, speaker_name: (
                f".\n{speaker_name}:\tA\t"
            )
        )
    }

@pytest.fixture
def answer_byline_following_interrupt_config(answer_byline_speaker_config):
    return answer_byline_speaker_config | {
        "BYLINE_FOLLOWING_INTERRUPT_FOR": (
            lambda _current_sign_type, _speaker_type, speaker_name: (
                f"--\n{speaker_name}:\tA\t"
            )
        )
    }
