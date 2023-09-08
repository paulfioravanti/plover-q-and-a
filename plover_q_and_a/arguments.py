"""
This is the set of valid arguments that can be included in a top-level command.
"""

# Config

ARGUMENT_DIVIDER = ":"

# Arguments

RESET_CONFIG = "RESET_CONFIG"
SET_NAME = "SET_NAME"

BYLINE_SPEAKER_TYPES = [
    "DEFENSE_1",
    "DEFENSE_2",
    "PLAINTIFF_1",
    "PLAINTIFF_2"
]

SPEAKER_TYPES = BYLINE_SPEAKER_TYPES + [
    "BAILIFF",
    "CLERK",
    "COURT",
    "COURT_REPORTER",
    "VIDEOGRAPHER",
    "WITNESS"
]
