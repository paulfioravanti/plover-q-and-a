# Instructions

This document outlines how to use the Plover Q&A plugin, what commands are
available, and some suggested configuration.

<!-- vim-markdown-toc GFM -->

* [Background](#background)
* [Commands](#commands)
    - [Questions](#questions)
    - [Answers](#answers)
    - [Named Speakers](#named-speakers)
    - [Changing Speaker Names](#changing-speaker-names)
    - [Bylines](#bylines)
    - [Immediate Responses](#immediate-responses)

<!-- vim-markdown-toc -->

## Background

Whenever someone starts speaking, you indicate this by "signing them in", either
by name, or marking them as the asker or answerer of a question.

The one thing that may not immediately intuitive about Q&A outline values is
that they are responsible for adding a speaker's final sentence punctuation
before another speaker starts talking.

They are responsible for marking how the last speaker ended what they said with
either:

- a question (default: `?`)
- an ending statement (default: `.`)
- an interruption (default: `--`)

Therefore, below you will see multiple variations of the same commands to mark
how the last speaker ended.

## Commands

Command arguments in Plover are separated using colons (`:`). So, when you see a
command like `{:Q_AND_A:QUESTION:INITIAL}`, this means you are running the
`Q_AND_A` command, and giving it two arguments: `QUESTION` and `INITIAL`.

### Questions

Questions, in the Q&A context, are always asked by lawyers to witnesses.

Question commands start with a `QUESTION` argument, followed by one of:

- `INITIAL`
- `FOLLOWING_STATEMENT`
- `FOLLOWING_QUESTION`
- `INTERRUPTING`

| Command                                 | Meaning                                                               | Suggested Outlines  |
|:----------------------------------------|:----------------------------------------------------------------------|:--------------------|
|`{:Q_AND_A:QUESTION:INITIAL}`            |Signs in the first lawyer question asked (no previous answer/statement)|`STKPWHR*`           |
|`{:Q_AND_A:QUESTION:FOLLOWING_STATEMENT}`|Ends a witness statement and signs in a lawyer question                |`STKPWHR`,`STKPWHR-R`|
|`{:Q_AND_A:QUESTION:FOLLOWING_QUESTION}` |Ends a witness question and signs in a lawyer question                 |`STKPWHR-F`          |
|`{:Q_AND_A:QUESTION:INTERRUPTING}`       |Signs in a lawyer question when they interrupt a witness               |`STKPWHR-RB`         |

### Answers

Answers are always given by witnesses under cross-examination.

Answer commands start with a `ANSWER` argument, followed by one of:

- `FOLLOWING_QUESTION`
- `FOLLOWING_STATEMENT`
- `INTERRUPTING`

| Command                               | Meaning                                                               | Suggested Outlines     |
|:--------------------------------------|:----------------------------------------------------------------------|:-----------------------|
|`{:Q_AND_A:ANSWER:FOLLOWING_QUESTION}` |Ends a lawyer question and signs in a witness answer                   |`-FRPBLGTS`,`H-FRPBLGTS`|
|`{:Q_AND_A:ANSWER:FOLLOWING_STATEMENT}`|Ends a lawyer's question as a statement, and signs in a witness answer |`R-FRPBLGTS`            |
|`{:Q_AND_A:ANSWER:INTERRUPTING}`       |Signs in a witness answer when they interrupt a lawyer                 |`WR-FRPBLGTS`           |

> No Initial Answer command exists since it would seem that there are never
> answers given without a question in Q&A.

### Named Speakers

Whenever anything is said outside the context of a Q&A cross-examination back
and forth (e.g. an opposing lawyer makes an objection etc), everything said by
any speaker needs to be specifically signed in using their name (for lawyers) or
title (anyone else).

The types of speakers, and their command arguments, recognised by this plugin
are:

- Plaintiff Lawyer 1 (`PLAINTIFF_1`)
- Defense Lawyer 1 (`DEFENSE_1`)
- Plaintiff Lawyer 2 (`PLAINTIFF_2`)
- Defense Lawyer 2 (`DEFENSE_2`)
- The Court \[ie the presiding judge\] (`COURT`)
- The Witness (`WITNESS`)
- The Videographer (`VIDEOGRAPHER`)
- The Court Reporter (`COURT_REPORTER`)
- The Clerk (`CLERK`)
- The Bailiff (`BAILIFF`)

Speaker commands start with the speaker command argument, followed by one of:

- `INITIAL`
- `FOLLOWING_QUESTION`
- `FOLLOWING_STATEMENT`
- `INTERRUPTING`

As an example of a set of known speaker commands, the following is a full list
of the commands and suggested outlines for The Court:

| Command                                 | Meaning                                                      | Suggested Outlines  |
|:----------------------------------------|:-------------------------------------------------------------|:--------------------|
|`{:Q_AND_A:COURT:INITIAL}`               |Signs in The Court as the first speaker (no previous speaker) |`STPHAOEUFPLT`       |
|`{:Q_AND_A:COURT:FOLLOWING_QUESTION}`    |Ends the previous speaker's question and signs in The Court   |`STPHAO*EUFPLT`      |
|`{:Q_AND_A:COURT:FOLLOWING_STATEMENT}`   |Ends the previous speaker's statement and signs in The Court  |`STPHAOEUFRPLT`      |
|`{:Q_AND_A:COURT:INTERRUPTING}`          |Signs in The Court when they interrupt a speaker              |`STPHAOEUFRPBLT`     |

The following is the set of `INITIAL` commands and suggested outlines for all of
the other known speaker types, who all also have their equivalent commands for
`FOLLOWING_QUESTION`, `FOLLOWING_STATEMENT`, and `INTERRUPTING` variations (see
the [`lawyers.json`][], [`other-speakers.json`][] and
[`other-speakers-ncra-style.json`][] dictionaries for those commands and their
example outlines):

| Command                           | Meaning                                         | Suggested Outlines            |
|:----------------------------------|:------------------------------------------------|:------------------------------|
|`{:Q_AND_A:PLAINTIFF_1:INITIAL}`   |Signs in Plaintiff lawyer 1 as the first speaker |`STPHAO`                       |
|`{:Q_AND_A:PLAINTIFF_2:INITIAL}`   |Signs in Plaintiff lawyer 2 as the first speaker |`SKWRAO`                       |
|`{:Q_AND_A:DEFENSE_1:INITIAL}`     |Signs in Defense lawyer 1 as the first speaker   |`EUFPLT`                       |
|`{:Q_AND_A:DEFENSE_2:INITIAL}`     |Signs in Defense lawyer 2 as the first speaker   |`EURBGS`                       |
|`{:Q_AND_A:WITNESS:INITIAL}`       |Signs in The Witness as the first speaker        |`SKWRAOEURBGS`,`W-PBS/W-PBS`   |
|`{:Q_AND_A:VIDEOGRAPHER:INITIAL}`  |Signs in The Videographer as the first speaker   |`STPHAEUFPLT`,`SREUD/SREUD`    |
|`{:Q_AND_A:COURT_REPORTER:INITIAL}`|Signs in The Court Reporter as the first speaker |`STPHOEUFPLT`,`RORP/RORP`      |
|`{:Q_AND_A:CLERK:INITIAL}`         |Signs in The Clerk as the first speaker          |`STPHAOEFPLT`,`KHRERBG/KHRERBG`|
|`{:Q_AND_A:BAILIFF:INITIAL}`       |Signs in The Bailiff as the first speaker        |`STPHAOUFPLT`,`PWHR-F/PWHR-F`  |

### Changing Speaker Names

> :tophat: Hat tip to [Plover Speaker ID][] for inspiration behind performing
> speaker name changes via a text prompt.

Although it is possible to change the default values for speaker names via the
[config][`examples`], there may be times where you want to change speaker names
on the fly, but not necessarily have them be saved as the defaults.

This is where the `SET_NAME` command comes in: it allows you to set a speaker
name via a text prompt that looks something like this:

`[Set PLAINTIFF_1 (MR. STPHAO) =>] _`

> `_` represents the cursor position

Once you have finished defining the new speaker name, you send a `SET_NAME:DONE`
command to "save" it, and the prompt is automatically deleted.

The names you set using `SET_NAME` persist even when you press the "Reconnect"
button on the Plover application, or when you send a `{:COMMAND:SET_CONFIG}`
command to reload dictionaries. You can, though, reset all the names back to
their defaults by sending a `RESET_CONFIG` command.

The following is a list of some example `SET_NAME`-related commands, and some
suggested outlines:

| Command                         | Meaning                                                            | Suggested Outlines        |
|:--------------------------------|:-------------------------------------------------------------------|:--------------------------|
|`{:Q_AND_A:SET_NAME:PLAINTIFF_1}`|Shows the current Plaintiff lawyer 1 name, and a prompt to change it|`SET/STPHAO` ("Set Snoo")  |
|`{:Q_AND_A:SET_NAME:PLAINTIFF_2}`|Shows the current Plaintiff lawyer 2 name, and a prompt to change it|`SET/SKWRAO` ("Set Screw") |
|`{:Q_AND_A:SET_NAME:DEFENSE_1}`  |Shows the current Defense lawyer 1 name, and a prompt to change it  |`SET/EUFPLT` ("Set Ifpelt")|
|`{:Q_AND_A:SET_NAME:DEFENSE_2}`  |Shows the current Defense lawyer 2 name, and a prompt to change it  |`SET/EURBGS` ("Set Irbs")  |
|`{:Q_AND_A:SET_NAME:DONE}`       |Saves the specified new speaker name, given after the prompt        |`STKPWHRAO`,`EUFRPBLGTS`   |
|`{:Q_AND_A:RESET_CONFIG}`        |Resets all speaker names back to their defaults                     |`R-FT/R-FT` ("ReSeT")      |

The `SET_NAME` command supports setting names of any known speaker
(`COURT_REPORTER`, `BAILIFF` etc), but the examples above were given because in
Q&A, typically only the lawyers are referred to by their given names, rather
than just their titles.

### Bylines

Bylines are used to indicate the lawyer that owns, or is in charge of, the
current line of questioning to a witness. Lawyers are the only speakers that get
bylines.

[Platinum Steno][]'s convention is to output the lawyer's title and surname,
all in capital letters, and then sign in a question. This plugin uses that
convention as the default output (but this can be changed via configuration).

Byline commands start with a `BYLINE` argument, followed by one of the lawyer
type command arguments:

- `PLAINTIFF_1`
- `PLAINTIFF_2`
- `DEFENSE_1`
- `DEFENSE_2`

Then, followed by one of the following arguments:

- `INITIAL`
- `FOLLOWING_STATEMENT`
- `FOLLOWING_QUESTION`
- `INTERRUPTING`

The following is a full list of the byline commands and suggested outlines for
Plaintiff Lawyer 1 (see the [`lawyers.json`][] example dictionary for the
equivalent example byline commands and suggested outlines for the other lawyer
types):

| Command                                           | Meaning                                                                      | Suggested Outlines |
|:--------------------------------------------------|:-----------------------------------------------------------------------------|:-------------------|
|`{:Q_AND_A:BYLINE:PLAINTIFF_1:INITIAL}`            |Signs in Plaintiff Lawyer 1's byline (no previous answer/statement)           |`STPHAO*`           |
|`{:Q_AND_A:BYLINE:PLAINTIFF_1:FOLLOWING_STATEMENT}`|Ends the previous speaker's statement and signs in Plaintiff Lawyer 1's byline|`STPHAO*R`          |
|`{:Q_AND_A:BYLINE:PLAINTIFF_1:FOLLOWING_QUESTION}` |Ends the previous speaker's question and signs in Plaintiff Lawyer 1's byline |`STPHAO*F`          |
|`{:Q_AND_A:BYLINE:PLAINTIFF_1:INTERRUPTING}`       |Signs in Plaintiff Lawyer 1's byline when they interrupt a speaker            |`STPHAO*RB`         |

### Immediate Responses

Immediate Response commands can be considered optional helpers: they are not
needed to perform Q&A, but if ever you find that common responses or phrases
come up immediately after a speaker switch during Q&A, this plugin provides
commands that can help you stroke them a bit quicker.

For example, some common words and phrases that begin an answer from witnesses
could be:

- Affirmative statements: "Yes.", "Yes, sir.", "Yeah.", "Correct.", "Right.",
  "Sure.", "Uh-huh." etc
- Negative statements: "No.", "No, sir." etc
- Unsure statements: "I don’t know." etc

Likewise, after witness statements, lawyers could say things like:

- Answer acknowledgements: "Okay.", "All right." etc
- Question versions of those acknowledgements: "Okay?", "All right?" etc

Following these responses either side could either:

- Yield control back to the other speaker
- Elaborate further

It is these two types of scenarios, after either a question or answer speaker
switch, that this plugin provides commands for.

Immediate Response commands piggy-back off the existing Question and Answer
`FOLLOWING_STATEMENT` and `FOLLOWING_QUESTION` commands, but add one of the
following arguments:

- `ELABORATE_AFTER`
- `YIELD_AFTER`

Following that, you specify the word or phrase you want to use.

Some examples of using these commands could be the following (see the
[`immediate-responses.json`][] for more examples):

| Command                                                           | Meaning                                                                                                    | Suggested Outlines |
|:------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------|:-------------------|
|`{:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:ELABORATE_AFTER:Okay}`     |Ends witness statement, signs in lawyer question, then outputs statement "Okay."                            |`STKPWHR-BG`        |
|`{:Q_AND_A:QUESTION:FOLLOWING_STATEMENT:YIELD_AFTER:Okay}`         |Ends witness statement, signs in lawyer question, outputs statement "Okay.", then signs in answer           |`STKPWHR*BG`        |
|`{:Q_AND_A:ANSWER:FOLLOWING_QUESTION:ELABORATE_AFTER:I don't know}`|Ends a lawyer question, signs in a witness answer, then outputs statement "I don't know."                   |`KWROEFRPBLGTS`     |
|`{:Q_AND_A:ANSWER:FOLLOWING_QUESTION:YIELD_AFTER:I don't know}`    |Ends a lawyer question, signs in a witness answer, outputs statement "I don't know.", then signs in question|`KWRO*EFRPBLGTS`    |

[`examples`]: ./examples
[`immediate-responses.json`]: ./examples/immediate-responses.json
[`lawyers.json`]: ./examples/lawyers.json
[`other-speakers-ncra-style.json`]: ./examples/other-speakers-ncra-style.json
[`other-speakers.json`]: ./examples/other-speakers.json
[Platinum Steno]: https://www.youtube.com/@PlatinumSteno
[Plover Speaker ID]: https://github.com/sammdot/plover-speaker-id
