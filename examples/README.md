# Config and Dictionaries

This plugin might only really be applicable for court reporting, but since
there are Q&A exercises in the [Platinum Steno][] lessons, this plugin attempts
to port the formatting used there to Plover (download the
[lesson 27 materials][Platinum Steno Lesson 27 lesson materials] for free to see
the briefs they use), but also allow you to customise every aspect of the output
to your liking.

Config and dictionary entries form the backbone of being able to use this
plugin, so examples of each are provided here in hopes they can get you started.

<!-- vim-markdown-toc GFM -->

* [Config](#config)
    - [Speaker](#speaker)
        + [Upcasing](#upcasing)
    - [Questions, Answers, and Bylines](#questions-answers-and-bylines)
    - [Other Formatting](#other-formatting)
    - [Prompts](#prompts)
    - [Customisation](#customisation)
* [Dictionaries](#dictionaries)

<!-- vim-markdown-toc -->

## Config

[`q_and_a.json`][] is an example config [JSON][] file containing all the
customisable parts of the various Q&A-related sign outputs. 

They are based on the formatting used in the [Platinum Steno][] Q&A exercises.
The values contained in this example config file are also hardcoded into the
plugin to act as default values when no config file is present, or values in
the config file are missing.

Therefore, if you are happy to use the defaults, there is _**no need for you to
create your own configuration file**_, and you can happily skip reading this
section.

If you are still here, the available options for configuration are:

### Speaker

Under the `"speaker"` key, you will find the a set of named types of people who
could potentially become speakers (or discussion participants) during Q&A:

| Key              | Meaning           | Default Value                 |
|:-----------------|:------------------|:------------------------------|
|`"plaintiff_1"`   |Plaintiff Lawyer 1 |`MR. STPHAO` (AKA "Mr. Snoo")  |
|`"defense_1"`     |Defense Lawyer 1   |`MR. EUFPLT` (AKA "Mr. Ifpelt")|
|`"plaintiff_2"`   |Plaintiff Lawyer 2 |`MR. SKWRAO` (AKA "Mr. Screw") |
|`"defense_2"`     |Defense Lawyer 2   |`MR. EURBGS` (AKA "Mr. Irbs")  |
|`"court"`         |The Judge/Court    |`THE COURT`                    |
|`"witness"`       |The Witness        |`THE WITNESS`                  |
|`"videographer"`  |The Videographer   |`THE VIDEOGRAPHER`             |
|`"court_reporter"`|The Court Reporter |`THE COURT REPORTER`           |
|`"clerk"`         |The Clerk          |`THE CLERK`                    |
|`"bailiff"`       |The Bailiff        |`THE BAILIFF`                  |

Each speaker has formatting that goes either side of the speaker name. You can
find these values under the `"formatting"` key inside the `"speaker"`:

| Key      | Meaning            | Default Value                |
|:---------|:-------------------|:-----------------------------|
|`"pre"`   |Pre-name formatting |`\t` (a Tab character)        |
|`"post"`  |Post-name formatting|`:  ` (colon, then two spaces)|
|`"upcase"`|Upcase formatting   |`true`                        |

Putting them all together, a back and forth between a lawyer and a judge using
default values could look like the following:

```
⇥···MR. STPHAO:  Objection, your Honor.
⇥···THE COURT:  Overruled.
```

> `⇥···` here represents a Tab character, and would not typically be visible on
> screen

#### Upcasing

Platinum Steno Q&A formatting has all names uppercased. By default, this plugin
follows that convention: when you either specify a speaker name in config, or
change it yourself using the `SET_NAME` command, the resulting value will
automatically be upcased.

If you want to keep lowercase characters in your speaker names, set
`"upcase": false` in your config inside the speaker formatting.

### Questions, Answers, and Bylines

Questions, answers, and bylines have similar sets of configuration under their
respective `"question"`, `"answer"`, and `"byline"` keys.

Each set of configuration has a `"marker"`, meaning the characters marking the
question, answer, or byline. They also each have a set of `"formatting"`,
same as speakers.

### Other Formatting

For the very discerning Q&A-er, other more minute configuration is available for
the following values:

| Key              | Meaning                                 | Default Value    |
|:-----------------|:----------------------------------------|:-----------------|
|`"question_end"`  |Marks the end of a question              |`?`               |
|`"statement_end"` |Marks the end of a statement             |`.`               |
|`"interrupt"`     |Marks a speaker interruption             |` --`             |
|`"yield"`         |Marks yielding control to another speaker|`\n` (line break) |
|`"sentence_space"`|Marker for directly after a sentence end |` ` (single space)|

Putting all of this together, we could have a 4-voice dialogue using default
values that outputs like the following:

```
BY MR. CHAMBERS:
⇥···Q⇥···All right. Miss Smith, where do you currently live?
⇥···A⇥···1892 Spring Drive in Riverside.
⇥···Q⇥···Did you live at that address in July of 2018?
⇥···A⇥···Yes, sir.
⇥···MR. DUGO:  Your Honor, I am having a difficult time hearing the witness.
⇥···THE COURT:  Miss Smith, I know it is tough, but have got to keep your voice up a little bit. It is hard to hear in this courtroom, okay?
⇥···THE WITNESS:  Yes, your Honor.
```

### Prompts

When you [change a speaker name][], you will see a text prompt that looks
something like this:

`[Set PLAINTIFF_1 (MR. STPHAO) =>] _`

> `_` represents the cursor position

This is how the prompt displays by default, but it is customisable via
configuration. In the config file, the prompt looks like this:

`"[Set {speaker_type} ({current_speaker_name}) =>] "`

The `{speaker_type}` and `{current_speaker_name}` parts are placeholders for the
speaker type (e.g. `PLAINTIFF_1`), and the current speaker name (e.g.
`MR. STPHAO`). If you customise your prompt, both of these parts **must** be
present in your custom prompt, or you will get an error when you try and reload
your config.

Configuration details for the prompt are:

| Key               | Meaning                                         | Default Value                                       |
|:------------------|:------------------------------------------------|:----------------------------------------------------|
|`"set_name_prompt"`|The prompt to display when setting a speaker name|`"[Set {speaker_type} ({current_speaker_name}) =>] "`|

### Customisation

If you want to customise how the signs output, create your own `q_and_a.json`
file and place it under Plover's configuration directory:

- Windows: `C:\Users\<your username>\AppData\Local\plover\plover`
- macOS: `~/Library/Application Support/plover`
- Linux: `~/.config/plover`

You do not need to add a full suite of entries as per the example config file.
If, say, you just want to change how the question and answer markers display by
putting the full words `QUESTION` and `ANSWER`, rather than the defaults of `Q`
and `A`, you could create a config file that just contains the following:

`q_and_a.json`

```json
{
  "question": {
    "marker": "QUESTION"
  },
  "answer": {
    "marker": "ANSWER"
  }
}
```

For all of the other values, the defaults will be used.

## Dictionaries

The [`dictionaries`][] directory contains a selection of JSON dictionaries
containing sample outlines that are drawn from, or take inspiration by,
[Platinum Steno][], but all the values output `plover-q-and-a` commands so they
can be used with this plugin.

Feel free to copy them into your own Plover dictionary sets, merge them all into
a single dictionary, or change them up a bit to make them your own.

The details around the rationale behind the example outlines can be found in the
blog post _[Plover For the Record][]_. But, to summarise:

- [`lawyers.json`][]: The `INITIAL` outlines for each speaker were taken from
  Platinum Steno, and all the rest were custom variations for the follow-on
  actions
- [`q-and-a.json`][]: Same situation as `lawyers.json`, but just for straight
  question and answer outlines
- [`other-speakers.json`][]: Similar to `lawyers.json`, but for non-lawyers
  only, and hence no byline-related outlines
- [`other-speakers-ncra-style.json`][]: Same values as `other-speakers.json`,
  but the outlines used there are from Platinum Steno's
  [NCRA Theory Dictionary][] (it's free; you just need to go through the
  checkout process for $0)
- [`immediate-responses.json`][]: Custom dictionary with outlines based on
  common responses given at the end of questions and answers. See [here][] for a
  detailed rationale.

Other dictionaries that may be of reference are:

- [Paul's Q&A dictionary][]: Custom dictionary by the author of this plugin.

For completeness' sake, support for other speakers who do not typically come up
in Q&A, but are used by court reporters (The Videographer, The Court Reporter,
The Clerk, and The Bailiff), has been added in. The example outlines for these
trial participants come from two sources:

- the [Platinum Steno Theory Dictionary (NCRS Theory)][], which would seem to
  potentially be derived from the theory used by the
  [National Court Reporters Association][] (NCRA)
- outlines I derived (read: made up) from the `STPHAOEUFPLT`-based outlines for
  The Court (since the Videographer, Court Reporter, Clerk, and Bailiff work
  with or for the Court, I figured their outlines could be grouped together)

Use whichever outlines feel comfortable to you, or make up entirely new ones!

[change a speaker name]: ../INSTRUCTIONS.md#changing-speaker-names
[`dictionaries`]: ./dictionaries
[here]: https://www.paulfioravanti.com/blog/plover-for-the-record/#update-25-november-2021-immediate-responses
[`immediate-responses.json`]: ./dictionaries/immediate-responses.json
[JSON]: https://www.json.org/json-en.html 
[`lawyers.json`]: ./dictionaries/lawyers.json
[National Court Reporters Association]: https://www.ncra.org/
[NCRA Theory Dictionary]: https://platinumsteno.com/downloads/platinum-steno-ncrs-theory-dictionary/
[`other-speakers.json`]: ./dictionaries/other-speakers.json
[`other-speakers-ncra-style.json`]: ./dictionaries/other-speakers-ncra-style.json
[Paul's Q&A dictionary]: https://github.com/paulfioravanti/steno-dictionaries/blob/main/dictionaries/q-and-a.md
[Platinum Steno]: https://www.youtube.com/@PlatinumSteno
[Platinum Steno Lesson 27 lesson materials]: https://platinumsteno.com/downloads/theory-lesson-27/
[Platinum Steno Theory Dictionary (NCRS Theory)]: https://platinumsteno.com/downloads/platinum-steno-ncrs-theory-dictionary/
[Plover For the Record]: https://www.paulfioravanti.com/blog/plover-for-the-record/
[`q-and-a.json`]: ./dictionaries/q-and-a.json
[`q_and_a.json`]: ./q_and_a.json
