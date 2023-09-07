"""
Config module that imports JSON data containing sign output customisations.
"""
import json
from pathlib import Path

from . import defaults


def load(config_filepath: Path) -> dict[str, any]:
    """
    Reads in the config JSON file, munges the data into outputtable signs and
    provides defaults in case values aren't specified.

    Raises an error if the specified config file is not JSON format.
    """
    try:
        with (config_filepath).open(encoding="utf-8") as file:
            data = json.load(file)
            file.close()
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError as exc:
        raise ValueError("Config file must contain a JSON object") from exc

    formatted_question = _formatted_question(data)
    question_end = _question_end(data)
    formatted_answer = _formatted_answer(data)
    statement_end = _statement_end(data)
    statement_elaborate = _statement_elaborate(data)
    interrupt = _interrupt(data)
    formatted_byline = _formatted_byline(data)
    speaker = data.get("speaker", {})
    speaker_names = _speaker_names(speaker)
    formatted_speaker = _formatted_speaker(speaker)

    return {
        "ANSWER_FOLLOWING_INTERRUPT": interrupt + formatted_answer,
        "ANSWER_FOLLOWING_QUESTION": question_end + formatted_answer,
        "ANSWER_FOLLOWING_STATEMENT": statement_end + formatted_answer,
        "BYLINE_FOR": formatted_byline,
        "BYLINE_FOLLOWING_INTERRUPT_FOR": lambda speaker_name: (
            interrupt + formatted_byline(speaker_name)
        ),
        "BYLINE_FOLLOWING_QUESTION_FOR": lambda speaker_name: (
            question_end + formatted_byline(speaker_name)
        ),
        "BYLINE_FOLLOWING_STATEMENT_FOR": lambda speaker_name: (
            statement_end + formatted_byline(speaker_name)
        ),
        "PREV_ATTACH_MARKERS": [
            _question_end_marker(data),
            _statement_end_marker(data)
        ],
        "QUESTION": formatted_question,
        "QUESTION_FOLLOWING_INTERRUPT": interrupt + formatted_question,
        "QUESTION_FOLLOWING_QUESTION": question_end + formatted_question,
        "QUESTION_FOLLOWING_STATEMENT": statement_end + formatted_question,
        "SPEAKER_FOR": formatted_speaker,
        "SPEAKER_FOLLOWING_INTERRUPT_FOR": lambda speaker_name: (
            interrupt + formatted_speaker(speaker_name)
        ),
        "SPEAKER_FOLLOWING_QUESTION_FOR": lambda speaker_name: (
            question_end + formatted_speaker(speaker_name)
        ),
        "SPEAKER_FOLLOWING_STATEMENT_FOR": lambda speaker_name: (
            statement_end + formatted_speaker(speaker_name)
        ),
        "speaker_names": speaker_names,
        "STATEMENT_ELABORATE": statement_elaborate,
    }

def _formatted_answer(data):
    answer = data.get("answer", {})
    answer_formatting = answer.get("formatting", {})
    return (
        answer_formatting.get(
            "pre", defaults.ANSWER_BEGIN_MARKER_PRE_FORMATTING
        )
        + answer.get("marker", defaults.ANSWER_BEGIN_MARKER)
        + answer_formatting.get(
            "post", defaults.ANSWER_BEGIN_MARKER_POST_FORMATTING
        )
    )

def _formatted_byline(data):
    byline = data.get("byline", {})
    byline_formatting = byline.get("formatting", {})
    return lambda speaker_name: (
        byline_formatting.get("pre", defaults.BYLINE_PRE_FORMATTING)
        + byline.get("marker", defaults.BYLINE_MARKER)
        + speaker_name
        + byline_formatting.get("post", defaults.BYLINE_POST_FORMATTING)
        + _formatted_question(data)
    )

def _formatted_question(data):
    question = data.get("question", {})
    question_formatting = question.get("formatting", {})
    return (
        question_formatting.get(
            "pre", defaults.QUESTION_BEGIN_MARKER_PRE_FORMATTING
        )
        + question.get("marker", defaults.QUESTION_BEGIN_MARKER)
        + question_formatting.get(
            "post", defaults.QUESTION_BEGIN_MARKER_POST_FORMATTING
        )
    )

def _formatted_speaker(speaker):
    speaker_formatting = speaker.get("formatting", {})
    return lambda speaker_name: (
        speaker_formatting.get("pre", defaults.SPEAKER_NAME_PRE_FORMATTING)
        + speaker_name
        + speaker_formatting.get("post", defaults.SPEAKER_NAME_POST_FORMATTING)
    )

def _interrupt(data):
    return (
        data.get("interrupt", defaults.INTERRUPT_MARKER)
        + _yield_marker(data)
    )

def _question_end(data):
    return _question_end_marker(data) + _yield_marker(data)

def _question_end_marker(data):
    return data.get("question_end", defaults.QUESTION_END_MARKER)

def _speaker_names(speaker):
    return {
        "BAILIFF": speaker.get("bailiff", defaults.BAILIFF_NAME),
        "CLERK": speaker.get("clerk", defaults.CLERK_NAME),
        "COURT": speaker.get("court", defaults.COURT_NAME),
        "COURT_REPORTER": speaker.get(
            "court_reporter", defaults.COURT_REPORTER_NAME
        ),
        "DEFENSE_1": speaker.get("defense_1", defaults.LAWYER_DEFENSE_1_NAME),
        "DEFENSE_2": speaker.get("defense_2", defaults.LAWYER_DEFENSE_2_NAME),
        "PLAINTIFF_1": speaker.get(
            "plaintiff_1", defaults.LAWYER_PLAINTIFF_1_NAME
        ),
        "PLAINTIFF_2": speaker.get(
            "plaintiff_2", defaults.LAWYER_PLAINTIFF_2_NAME
        ),
        "VIDEOGRAPHER": speaker.get("videographer", defaults.VIDEOGRAPHER_NAME),
        "WITNESS": speaker.get("witness", defaults.WITNESS_NAME)
    }

def _statement_elaborate(data):
    return (
        _statement_end_marker(data)
        + data.get("sentence_space", defaults.SENTENCE_SPACE)
    )

def _statement_end(data):
    return _statement_end_marker(data) + _yield_marker(data)

def _statement_end_marker(data):
    return data.get("statement_end", defaults.STATEMENT_END_MARKER)

def _yield_marker(data):
    return data.get("yield", defaults.YIELD_MARKER)
