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

_SpeakerMarker = dict[str, Union[str, bool]]

def marker(data: dict[str, Any]) -> Callable[[str], str]:
    """
    Format a speaker from config.
    """
    speaker_marker: _SpeakerMarker = _speaker_marker(data)
    pre_formatting: str = cast(
        str,
        speaker_marker.get("pre", _SPEAKER_NAME_PRE_FORMATTING)
    )
    post_formatting: str = cast(
        str,
        speaker_marker.get("post", _SPEAKER_NAME_POST_FORMATTING)
    )

    return lambda speaker_name: (
        pre_formatting + speaker_name + post_formatting
    )

def names(data: dict[str, Any]) -> dict[str, str]:
    """
    Format speaker names from config.
    """
    speaker_marker: _SpeakerMarker = _speaker_marker(data)
    speaker_names: dict[str, str] = {
        "BAILIFF": cast(str, speaker_marker.get("bailiff", _BAILIFF_NAME)),
        "CLERK": cast(str, speaker_marker.get("clerk", _CLERK_NAME)),
        "COURT": cast(str, speaker_marker.get("court", _COURT_NAME)),
        "COURT_REPORTER": cast(str,
            speaker_marker.get("court_reporter", _COURT_REPORTER_NAME)
        ),
        "DEFENSE_1": cast(str,
            speaker_marker.get("defense_1", _LAWYER_DEFENSE_1_NAME)
        ),
        "DEFENSE_2": cast(str,
            speaker_marker.get("defense_2", _LAWYER_DEFENSE_2_NAME)
        ),
        "PLAINTIFF_1": cast(str,
            speaker_marker.get("plaintiff_1", _LAWYER_PLAINTIFF_1_NAME)
        ),
        "PLAINTIFF_2": cast(str,
             speaker_marker.get("plaintiff_2", _LAWYER_PLAINTIFF_2_NAME)
        ),
        "VIDEOGRAPHER": cast(str,
            speaker_marker.get("videographer", _VIDEOGRAPHER_NAME)
        ),
        "WITNESS": cast(str, speaker_marker.get("witness", _WITNESS_NAME))
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
        _speaker_marker(data).get("upcase", _SPEAKER_NAME_UPCASE_FORMATTING)
    )

def _speaker_marker(data: dict[str, Any]) -> _SpeakerMarker:
    return _speaker(data).get("marker", {})

def _speaker(data: dict[str, Any]) -> dict[str, _SpeakerMarker]:
    return cast(dict[str, _SpeakerMarker], data.get("speaker", {}))
