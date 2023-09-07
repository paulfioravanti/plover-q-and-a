"""
This is the set of valid arguments that can be included in a top-level command.
"""

# Name

SET_NAME = "SET_NAME"
DONE = "DONE"

# All

ARGUMENT_DIVIDER = ":"

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
