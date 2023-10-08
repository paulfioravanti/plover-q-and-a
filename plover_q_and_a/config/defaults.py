"""
Default values used for Q&A signs if they are not specified in the config file.
"""

## Lawyer Names (most frequently changed)
LAWYER_PLAINTIFF_1_NAME = "MR. STPHAO" # aka "Mr. Snoo"
LAWYER_DEFENSE_1_NAME = "MR. EUFPLT"   # aka "Mr. Ifpelt"
LAWYER_PLAINTIFF_2_NAME = "MR. SKWRAO" # aka "Mr. Screw"
LAWYER_DEFENSE_2_NAME = "MR. EURBGS"   # aka "Mr. Irbs"

## Other participant names
COURT_NAME = "THE COURT"
WITNESS_NAME = "THE WITNESS"
VIDEOGRAPHER_NAME = "THE VIDEOGRAPHER"
COURT_REPORTER_NAME = "THE COURT REPORTER"
CLERK_NAME = "THE CLERK"
BAILIFF_NAME = "THE BAILIFF"

SPEAKER_NAME_PRE_FORMATTING = "\t"
SPEAKER_NAME_POST_FORMATTING = ":  "
SPEAKER_NAME_UPCASE_FORMATTING = True

## Bylines, and their formatting
BYLINE_MARKER = "BY "
BYLINE_PRE_FORMATTING = ""
BYLINE_POST_FORMATTING = ":\n"

## Question and Answer markers, and their formatting
QUESTION_BEGIN_MARKER = "Q"
QUESTION_BEGIN_MARKER_PRE_FORMATTING = "\t"
QUESTION_BEGIN_MARKER_POST_FORMATTING = "\t"

ANSWER_BEGIN_MARKER = "A"
ANSWER_BEGIN_MARKER_PRE_FORMATTING = "\t"
ANSWER_BEGIN_MARKER_POST_FORMATTING = "\t"

## Other formatting
STATEMENT_END_MARKER = "."
QUESTION_END_MARKER = "?"
INTERRUPT_MARKER = " --"
YIELD_MARKER = "\n"
SENTENCE_SPACE = " "
SET_NAME_PROMPT = "[Set {speaker_type} ({current_speaker_name}) =>] "
