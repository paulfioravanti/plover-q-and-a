"""
Module to handle parsing and formatting of a byline from config.
"""
from typing import (
    Any,
    Callable,
    Union,
    cast
)


# Default values

## Formatting
_SPEAKER_NAME_PRE_FORMATTING: str = "\t"
_SPEAKER_NAME_POST_FORMATTING: str = ":  "
_SPEAKER_NAME_UPCASE_FORMATTING: bool = True

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

def formatted_speaker(data: dict[str, Any]) -> Callable[[str], str]:
    """
    Format a speaker from config.
    """
    speaker_formatting: dict[str, Union[str, bool]] = _speaker_formatting(data)

    return lambda speaker_name: (
        cast(str, speaker_formatting.get("pre", _SPEAKER_NAME_PRE_FORMATTING))
        + speaker_name
        + cast(str,
            speaker_formatting.get("post", _SPEAKER_NAME_POST_FORMATTING)
        )
    )

def names(data: dict[str, Any]) -> dict[str, str]:
    """
    Format speaker names from config.
    """
    speaker: dict[str, Union[str, dict[str, Union[str, bool]]]] = _speaker(data)
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

    if should_upcase(data):
        upcased_speaker_names: dict[str, str] = speaker_names.copy()

        for key, value in speaker_names.items():
            upcased_speaker_names[key] = value.upper()

        return upcased_speaker_names

    return speaker_names

def should_upcase(data: dict[str, Any]) -> bool:
    """
    Get config value that determines whether to upcase speaker names.
    """
    return cast(
        bool,
        _speaker_formatting(data).get("upcase", _SPEAKER_NAME_UPCASE_FORMATTING)
    )

def _speaker_formatting(data: dict[str, Any]) -> dict[str, Union[str, bool]]:
    return cast(
        dict[str, Union[str, bool]],
        _speaker(data).get("formatting", {})
    )

def _speaker(
    data: dict[str, Any]
) -> dict[str, Union[str, dict[str, Union[str, bool]]]]:
    return cast(
        dict[str, Union[str, dict[str, Union[str, bool]]]],
        data.get("speaker", {})
    )
