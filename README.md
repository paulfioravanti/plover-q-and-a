# Plover Q&A

[![Build Status][Build Status image]][Build Status url]

This [Plover][] [extension][] [plugin][] contains [metas][] for your
dictionaries that can assist with [Q&A][] (Question and Answer): the process of
recording lines of questioning in a conversation involving multiple people,
usually in a legal context.

More information about the concept of Q&A can be found at:

- [Platinum Steno Lesson 27 QA video][]

More information about the creation of, and reasoning behind, the outlines that
originally informed this plugin can be found at the following blog post:

- _[Plover For the Record][]_

## Install

Until this plugin is added to the Plover registry, download from GitHub or clone
using [git][]:

```sh
git clone git@github.com:paulfioravanti/plover-q-and-a.git
cd plover-q-and-a
plover -s plover_plugins install .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

- Restart Plover, open the Configuration screen (either click the Configuration
  icon, or from the main Plover application menu, select `Preferences...`)
- Open the Plugins tab
- Check the box next to `plover_q_and_a` to activate the plugin

\[Future\] Once this plugin is [added to the Plover registry][]:

1. In the Plover application, open the Plugins Manager (either click the Plugins
   Manager icon, or from the `Tools` menu, select `Plugins Manager`).
2. From the list of plugins, find `plover-q-and-a`
3. Click "Install/Update"
4. When it finishes installing, restart Plover
5. After re-opening Plover, open the Configuration screen (either click the
   Configuration icon, or from the main Plover application menu, select
   `Preferences...`)
6. Open the Plugins tab
7. Check the box next to `plover_q_and_a` to activate the plugin

## Config and Dictionaries

See the [`examples`][] directory for example configuration and dictionaries to
help you get up and running with using this plugin for Q&A.

## How To Use

See the [`INSTRUCTIONS`][] page.

## Development

Clone from GitHub with [git][]:

```sh
git clone git@github.com:paulfioravanti/plover-q-and-a.git
cd plover-q-and-a
```

### Python Version

Plover's Python environment currently uses version 3.9 (see Plover's
[`workflow_context.yml`][] to confirm the current version).

So, in order to avoid unexpected issues, use your runtime version manager to
make sure your local development environment also uses Python 3.9.x.

### Testing

Tests in this plugin were created with [Pytest][]. Run them with the following
command:

```sh
pytest
```

### Linting

Attempts have been made to have at least some kind of code quality baseline with
[Pylint][]. Run the linter over the codebase with the following command:

```sh
pylint plover_q_and_a
```

### Testing Changes

After making any code changes, install the plugin into Plover with the following
command:

```sh
plover -s plover_plugins install .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

[added to the Plover registry]: https://github.com/openstenoproject/plover_plugins_registry/pull/41
[Build Status image]: https://github.com/paulfioravanti/plover-q-and-a/actions/workflows/ci.yml/badge.svg
[Build Status url]: https://github.com/paulfioravanti/plover-q-and-a/actions/workflows/ci.yml
[`examples`]: ./examples
[extension]: https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
[git]: https://git-scm.com/
[Invoke Plover from the command line]: https://github.com/openstenoproject/plover/wiki/Invoke-Plover-from-the-command-line
[`INSTRUCTIONS`]: ./INSTRUCTIONS.md
[`immediate-responses.json`]: ./examples/immediate-responses.json
[`lawyers.json`]: ./examples/lawyers.json
[metas]: https://plover.readthedocs.io/en/latest/plugin-dev/metas.html
[`other-speakers-ncra-style.json`]: ./examples/other-speakers-ncra-style.json
[`other-speakers.json`]: ./examples/other-speakers.json
[Platinum Steno]: https://www.youtube.com/@PlatinumSteno
[Platinum Steno Lesson 27 QA video]: https://www.youtube.com/watch?v=tEgaJ7hWIvg
[Plover]: https://www.openstenoproject.org/
[Plover For the Record]: https://www.paulfioravanti.com/blog/plover-for-the-record/
[plugin]: https://plover.readthedocs.io/en/latest/plugins.html#types-of-plugins
[Pylint]: https://github.com/pylint-dev/pylint
[Pytest]: https://pytest.org/
[Q&A]: http://ilovesteno.com/2014/02/03/the-different-types-of-q-a/
[`workflow_context.yml`]: https://github.com/openstenoproject/plover/blob/master/.github/workflows/ci/workflow_context.yml
