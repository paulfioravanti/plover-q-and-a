"""
Module to handle parsing the application JSON config file.
"""
import re
from typing import (
    Any,
    Callable,
    Pattern,
    Tuple,
    Union,
    cast
)

# Default config values

## Lawyer Names (most frequently changed)
_LAWYER_PLAINTIFF_1_NAME: str = "MR. STPHAO" # aka "Mr. Snoo"
_LAWYER_DEFENSE_1_NAME: str = "MR. EUFPLT"   # aka "Mr. Ifpelt"
_LAWYER_PLAINTIFF_2_NAME: str = "MR. SKWRAO" # aka "Mr. Screw"
_LAWYER_DEFENSE_2_NAME: str = "MR. EURBGS"   # aka "Mr. Irbs"

## Other participant names
_COURT_NAME: str = "THE COURT"
_WITNESS_NAME: str = "THE WITNESS"
_VIDEOGRAPHER_NAME: str = "THE VIDEOGRAPHER"
_COURT_REPORTER_NAME: str = "THE COURT REPORTER"
_CLERK_NAME: str = "THE CLERK"
_BAILIFF_NAME: str = "THE BAILIFF"

_SPEAKER_NAME_PRE_FORMATTING: str = "\t"
_SPEAKER_NAME_POST_FORMATTING: str = ":  "
_SPEAKER_NAME_UPCASE_FORMATTING: bool = True

## Bylines, and their formatting
_BYLINE_MARKER: str = "BY "
_BYLINE_PRE_FORMATTING: str = ""
_BYLINE_POST_FORMATTING: str = ":\n"

## Question and Answer markers, and their formatting
_QUESTION_BEGIN_MARKER: str = "Q"
_QUESTION_BEGIN_MARKER_PRE_FORMATTING: str = "\t"
_QUESTION_BEGIN_MARKER_POST_FORMATTING: str = "\t"

_ANSWER_BEGIN_MARKER: str = "A"
_ANSWER_BEGIN_MARKER_PRE_FORMATTING: str = "\t"
_ANSWER_BEGIN_MARKER_POST_FORMATTING: str = "\t"

## Other formatting
_STATEMENT_END_MARKER: str = "."
_QUESTION_END_MARKER: str = "?"
_INTERRUPT_MARKER: str = " --"
_YIELD_MARKER: str = "\n"
_SENTENCE_SPACE: str = " "
_SET_NAME_PROMPT: str = "[Set {speaker_type} ({current_speaker_name}) =>] "

# Prompt must contain both {speaker_type} and {current_speaker_name} in the
# string, otherwise it is invalid.
_SET_NAME_PROMPT_MATCH_CONDITION: Pattern[str] = re.compile(
    r"(?=.*{speaker_type})(?=.*{current_speaker_name})"
)

def parse(data: dict[str, Any]) -> Tuple[Any, ...]:
    """
    Parse config data, providing defaults values where not provided.
    """
    formatted_question: str = _formatted_question(data)
    question_end: str = _question_end(data)
    formatted_answer: str = _formatted_answer(data)
    statement_end: str = _statement_end(data)
    statement_elaborate: str = _statement_elaborate(data)
    interrupt: str = _interrupt(data)
    formatted_byline: Callable[[str], str] = _formatted_byline(data)
    set_name_prompt: str = _set_name_prompt(data)
    speaker: dict[str, Union[str, dict[str, Union[str, bool]]]] = (
        data.get("speaker", {})
    )
    speaker_formatting: dict[str, Union[str, bool]] = (
        cast(dict[str, Union[str, bool]], speaker.get("formatting", {}))
    )
    speaker_upcase: bool = cast(bool,
        speaker_formatting.get(
            "upcase",
            _SPEAKER_NAME_UPCASE_FORMATTING
        )
    )
    speaker_names: dict[str, str] = _speaker_names(speaker, speaker_upcase)
    formatted_speaker = (
        _formatted_speaker(speaker_formatting)
    )

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
    answer: dict[str, Union[str, dict[str, str]]] = data.get("answer", {})
    answer_formatting: dict[str, str] = cast(dict[str, str],
        answer.get("formatting", {})
    )
    return (
        answer_formatting.get(
            "pre", _ANSWER_BEGIN_MARKER_PRE_FORMATTING
        )
        + cast(str, answer.get("marker", _ANSWER_BEGIN_MARKER))
        + answer_formatting.get(
            "post", _ANSWER_BEGIN_MARKER_POST_FORMATTING
        )
    )

def _formatted_byline(data: dict[str, Any]) -> Callable[[str], str]:
    byline: dict[str, Union[str, dict[str, str]]] = (
        cast(dict[str, Union[str, dict[str, str]]], data.get("byline", {}))
    )
    byline_formatting: dict[str, str] = cast(dict[str, str],
        byline.get("formatting", {})
    )

    return lambda speaker_name: (
        byline_formatting.get("pre", _BYLINE_PRE_FORMATTING)
        + cast(str, byline.get("marker", _BYLINE_MARKER))
        + speaker_name
        + byline_formatting.get("post", _BYLINE_POST_FORMATTING)
        + _formatted_question(data)
    )

def _formatted_question(data: dict[str, Any]) -> str:
    question: dict[str, Union[str, dict[str, str]]] = data.get("question", {})
    question_formatting: dict[str, str] = cast(dict[str, str],
        question.get("formatting", {})
    )
    return (
        question_formatting.get(
            "pre", _QUESTION_BEGIN_MARKER_PRE_FORMATTING
        )
        + cast(str, question.get("marker", _QUESTION_BEGIN_MARKER))
        + question_formatting.get(
            "post", _QUESTION_BEGIN_MARKER_POST_FORMATTING
        )
    )

def _formatted_speaker(
    speaker_formatting: dict[str, Union[str, bool]]
) -> Callable[[str], str]:
    return lambda speaker_name: (
        cast(str, speaker_formatting.get("pre", _SPEAKER_NAME_PRE_FORMATTING))
        + speaker_name
        + cast(str,
            speaker_formatting.get("post", _SPEAKER_NAME_POST_FORMATTING)
        )
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
    prompt: str = cast(str, data.get("set_name_prompt", _SET_NAME_PROMPT))

    if not re.match(_SET_NAME_PROMPT_MATCH_CONDITION, prompt):
        raise ValueError(
            "Both {speaker_type} and {current_speaker_name} must be "
            "present in the set_name_prompt."
        )

    return prompt

def _speaker_names(
    speaker: dict[str, Union[str, dict[str, Union[str, bool]]]],
    speaker_upcase: bool
) -> dict[str, str]:
    speaker_names: dict[str, str] = {
        "BAILIFF": cast(str, speaker.get("bailiff", _BAILIFF_NAME)),
        "CLERK": cast(str, speaker.get("clerk", _CLERK_NAME)),
        "COURT": cast(str, speaker.get("court", _COURT_NAME)),
        "COURT_REPORTER": cast(str,
            speaker.get("court_reporter", _COURT_REPORTER_NAME)
        ),
        "DEFENSE_1": cast(str,
            speaker.get("defense_1", _LAWYER_DEFENSE_1_NAME)
        ),
        "DEFENSE_2": cast(str,
            speaker.get("defense_2", _LAWYER_DEFENSE_2_NAME)
        ),
        "PLAINTIFF_1": cast(str,
            speaker.get("plaintiff_1", _LAWYER_PLAINTIFF_1_NAME)
        ),
        "PLAINTIFF_2": cast(str,
             speaker.get("plaintiff_2", _LAWYER_PLAINTIFF_2_NAME)
        ),
        "VIDEOGRAPHER": cast(str,
            speaker.get("videographer", _VIDEOGRAPHER_NAME)
        ),
        "WITNESS": cast(str, speaker.get("witness", _WITNESS_NAME))
    }

    if speaker_upcase:
        upcased_speaker_names: dict[str, str] = speaker_names.copy()

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
