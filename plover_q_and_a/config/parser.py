"""
Module to handle parsing the application JSON config file.
"""
import re
from typing import (
    Any,
    Callable,
    Tuple,
    cast
)

# Default config values

## Lawyer Names (most frequently changed)
_LAWYER_PLAINTIFF_1_NAME = "MR. STPHAO" # aka "Mr. Snoo"
_LAWYER_DEFENSE_1_NAME = "MR. EUFPLT"   # aka "Mr. Ifpelt"
_LAWYER_PLAINTIFF_2_NAME = "MR. SKWRAO" # aka "Mr. Screw"
_LAWYER_DEFENSE_2_NAME = "MR. EURBGS"   # aka "Mr. Irbs"

## Other participant names
_COURT_NAME = "THE COURT"
_WITNESS_NAME = "THE WITNESS"
_VIDEOGRAPHER_NAME = "THE VIDEOGRAPHER"
_COURT_REPORTER_NAME = "THE COURT REPORTER"
_CLERK_NAME = "THE CLERK"
_BAILIFF_NAME = "THE BAILIFF"

_SPEAKER_NAME_PRE_FORMATTING = "\t"
_SPEAKER_NAME_POST_FORMATTING = ":  "
_SPEAKER_NAME_UPCASE_FORMATTING = True

## Bylines, and their formatting
_BYLINE_MARKER = "BY "
_BYLINE_PRE_FORMATTING = ""
_BYLINE_POST_FORMATTING = ":\n"

## Question and Answer markers, and their formatting
_QUESTION_BEGIN_MARKER = "Q"
_QUESTION_BEGIN_MARKER_PRE_FORMATTING = "\t"
_QUESTION_BEGIN_MARKER_POST_FORMATTING = "\t"

_ANSWER_BEGIN_MARKER = "A"
_ANSWER_BEGIN_MARKER_PRE_FORMATTING = "\t"
_ANSWER_BEGIN_MARKER_POST_FORMATTING = "\t"

## Other formatting
_STATEMENT_END_MARKER = "."
_QUESTION_END_MARKER = "?"
_INTERRUPT_MARKER = " --"
_YIELD_MARKER = "\n"
_SENTENCE_SPACE = " "
_SET_NAME_PROMPT = "[Set {speaker_type} ({current_speaker_name}) =>] "

# Prompt must contain both {speaker_type} and {current_speaker_name} in the
# string, otherwise it is invalid.
_SET_NAME_PROMPT_MATCH_CONDITION = re.compile(
    r"(?=.*{speaker_type})(?=.*{current_speaker_name})"
)

def parse(data: dict[str, Any]) -> Tuple[Any, ...]:
    """
    Parse config data, providing defaults values where not provided.
    """
    formatted_question = _formatted_question(data)
    question_end = _question_end(data)
    formatted_answer = _formatted_answer(data)
    statement_end = _statement_end(data)
    statement_elaborate = _statement_elaborate(data)
    interrupt = _interrupt(data)
    formatted_byline = _formatted_byline(data)
    set_name_prompt = _set_name_prompt(data)
    speaker = data.get("speaker", {})
    speaker_formatting = speaker.get("formatting", {})
    speaker_upcase = (
        speaker_formatting.get(
            "upcase",
            _SPEAKER_NAME_UPCASE_FORMATTING
        )
    )
    speaker_names = _speaker_names(speaker, speaker_upcase)
    formatted_speaker = _formatted_speaker(speaker_formatting)

    return ( # pylint: disable-msg=duplicate-code
        formatted_question,
        question_end,
        formatted_answer,
        statement_end,
        statement_elaborate,
        interrupt,
        formatted_byline,
        set_name_prompt,
        speaker_upcase,
        speaker_names,
        formatted_speaker
    )

def _formatted_answer(data: dict[str, Any]) -> str:
    answer = data.get("answer", {})
    answer_formatting = answer.get("formatting", {})
    return cast(str, (
        answer_formatting.get(
            "pre", _ANSWER_BEGIN_MARKER_PRE_FORMATTING
        )
        + answer.get("marker", _ANSWER_BEGIN_MARKER)
        + answer_formatting.get(
            "post", _ANSWER_BEGIN_MARKER_POST_FORMATTING
        )
    ))

def _formatted_byline(data: dict[str, Any]) -> Callable[[str], str]:
    byline = data.get("byline", {})
    byline_formatting = byline.get("formatting", {})
    return lambda speaker_name: (
        byline_formatting.get("pre", _BYLINE_PRE_FORMATTING)
        + byline.get("marker", _BYLINE_MARKER)
        + speaker_name
        + byline_formatting.get("post", _BYLINE_POST_FORMATTING)
        + _formatted_question(data)
    )

def _formatted_question(data: dict[str, Any]) -> str:
    question = data.get("question", {})
    question_formatting = question.get("formatting", {})
    return cast(str, (
        question_formatting.get(
            "pre", _QUESTION_BEGIN_MARKER_PRE_FORMATTING
        )
        + question.get("marker", _QUESTION_BEGIN_MARKER)
        + question_formatting.get(
            "post", _QUESTION_BEGIN_MARKER_POST_FORMATTING
        )
    ))

def _formatted_speaker(
    speaker_formatting: dict[str, str]
) -> Callable[[str], str]:
    return lambda speaker_name: (
        speaker_formatting.get("pre", _SPEAKER_NAME_PRE_FORMATTING)
        + speaker_name
        + speaker_formatting.get("post", _SPEAKER_NAME_POST_FORMATTING)
    )

def _interrupt(data: dict[str, Any]) -> str:
    return (
        cast(str, data.get("interrupt", _INTERRUPT_MARKER))
        + _yield_marker(data)
    )

def _question_end(data: dict[str, Any]) -> str:
    return _question_end_marker(data) + _yield_marker(data)

def _question_end_marker(data: dict[str, Any]) -> str:
    return cast(str, data.get("question_end", _QUESTION_END_MARKER))

def _set_name_prompt(data: dict[str, Any]) -> str:
    prompt = cast(str, data.get("set_name_prompt", _SET_NAME_PROMPT))

    if not re.match(_SET_NAME_PROMPT_MATCH_CONDITION, prompt):
        raise ValueError(
            "Both {speaker_type} and {current_speaker_name} must be "
            "present in the set_name_prompt."
        )

    return prompt

def _speaker_names(
    speaker: dict[str, str],
    speaker_upcase: bool
) -> dict[str, str]:
    speaker_names = {
        "BAILIFF": speaker.get("bailiff", _BAILIFF_NAME),
        "CLERK": speaker.get("clerk", _CLERK_NAME),
        "COURT": speaker.get("court", _COURT_NAME),
        "COURT_REPORTER": speaker.get(
            "court_reporter", _COURT_REPORTER_NAME
        ),
        "DEFENSE_1": speaker.get("defense_1", _LAWYER_DEFENSE_1_NAME),
        "DEFENSE_2": speaker.get("defense_2", _LAWYER_DEFENSE_2_NAME),
        "PLAINTIFF_1": speaker.get(
            "plaintiff_1", _LAWYER_PLAINTIFF_1_NAME
        ),
        "PLAINTIFF_2": speaker.get(
            "plaintiff_2", _LAWYER_PLAINTIFF_2_NAME
        ),
        "VIDEOGRAPHER": speaker.get("videographer", _VIDEOGRAPHER_NAME),
        "WITNESS": speaker.get("witness", _WITNESS_NAME)
    }

    if speaker_upcase:
        upcased_speaker_names = speaker_names.copy()

        for key, value in speaker_names.items():
            upcased_speaker_names[key] = value.upper()

        return upcased_speaker_names

    return speaker_names

def _statement_elaborate(data: dict[str, Any]) -> str:
    return (
        _statement_end_marker(data)
        + cast(str, data.get("sentence_space", _SENTENCE_SPACE))
    )

def _statement_end(data: dict[str, Any]) -> str:
    return _statement_end_marker(data) + _yield_marker(data)

def _statement_end_marker(data: dict[str, Any]) -> str:
    return cast(str, data.get("statement_end", _STATEMENT_END_MARKER))

def _yield_marker(data: dict[str, Any]) -> str:
    return cast(str, data.get("yield", _YIELD_MARKER))
