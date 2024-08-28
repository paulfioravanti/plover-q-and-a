# Plover Q&A

[![Build Status][Build Status image]][Build Status url] [![PyPI - Version][PyPI version image]][PyPI url] [![PyPI - Downloads][PyPI downloads image]][PyPI url] [![linting: pylint][linting image]][linting url]

This [Plover][] [extension][] [plugin][] contains [metas][] for your
dictionaries that can assist with [Q&A][] (Question and Answer): the process of
recording lines of questioning in a conversation involving multiple people,
usually in a legal context.

More information about the concept of Q&A can be found at:

- [Platinum Steno Lesson 27 QA video][]

More information about the creation of, and reasoning behind, the outlines that
originally informed this plugin can be found at the following blog post:

- _[Plover For the Record][]_

You can see a video of the plugin in action here:

- [Steno Legal Q&A Test with Plover and Vim][]

(And if you are a [Vim][] user and want the syntax highlighting, you can find it
in the [Vim Steno Q&A][] plugin)

## Install

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

```console
git clone git@github.com:paulfioravanti/plover-q-and-a.git
cd plover-q-and-a
python -m pip install --editable ".[test]"
```

If you are a [Tmuxinator][] user, you may find my [plover_q_and_a project
file][] of reference.

### Python Version

Plover's Python environment currently uses version 3.9 (see Plover's
[`workflow_context.yml`][] to confirm the current version).

So, in order to avoid unexpected issues, use your runtime version manager to
make sure your local development environment also uses Python 3.9.x.

### Testing

- [Pytest][] is used for testing in this plugin.
- [Coverage.py][] and [pytest-cov][] are used for test coverage, and to run
  coverage within Pytest
- [Pylint][] is used for code quality
- [Mypy][] is used for static type checking

Currently, the only parts able to be tested are ones that do not rely directly
on Plover.

Run tests, coverage, and linting with the following commands:

```console
pytest --cov --cov-report=term-missing
pylint plover_q_and_a
mypy plover_q_and_a
```

To get a HTML test coverage report:

```console
coverage run --module pytest
coverage html
open htmlcov/index.html
```

If you are a [`just`][] user, you may find the [`justfile`][] useful during
development in running multiple test commands. You can run the following command
from the project root directory:

```console
just --working-directory . --justfile test/justfile
```

### Deploying Changes

After making any code changes, install the plugin into Plover with the following
command:

```console
plover --script plover_plugins install --editable .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

When necessary, the plugin can be uninstalled via the command line with the
following command:

```console
plover --script plover_plugins uninstall plover-q-and-a
```

[Build Status image]: https://github.com/paulfioravanti/plover-q-and-a/actions/workflows/ci.yml/badge.svg
[Build Status url]: https://github.com/paulfioravanti/plover-q-and-a/actions/workflows/ci.yml
[Coverage.py]: https://github.com/nedbat/coveragepy 
[`examples`]: ./examples
[extension]: https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
[git]: https://git-scm.com/
[Invoke Plover from the command line]: https://github.com/openstenoproject/plover/wiki/Invoke-Plover-from-the-command-line
[`INSTRUCTIONS`]: ./INSTRUCTIONS.md
[`just`]: https://github.com/casey/just
[`justfile`]: ./test/justfile
[linting image]: https://img.shields.io/badge/linting-pylint-yellowgreen
[linting url]: https://github.com/pylint-dev/pylint
[metas]: https://plover.readthedocs.io/en/latest/plugin-dev/metas.html
[Mypy]: https://github.com/python/mypy
[Platinum Steno]: https://www.youtube.com/@PlatinumSteno
[Platinum Steno Lesson 27 QA video]: https://www.youtube.com/watch?v=tEgaJ7hWIvg
[Plover]: https://www.openstenoproject.org/
[Plover For the Record]: https://www.paulfioravanti.com/blog/plover-for-the-record/
[plover_q_and_a project file]: https://github.com/paulfioravanti/dotfiles/blob/master/tmuxinator/plover_q_and_a.yml
[plugin]: https://plover.readthedocs.io/en/latest/plugins.html#types-of-plugins
[Pylint]: https://github.com/pylint-dev/pylint
[PyPI downloads image]:https://img.shields.io/pypi/dm/plover-q-and-a
[PyPI version image]: https://img.shields.io/pypi/v/plover-q-and-a
[PyPI url]: https://pypi.org/project/plover-q-and-a/
[Pytest]: https://pytest.org/
[pytest-cov]: https://github.com/pytest-dev/pytest-cov/
[Q&A]: http://ilovesteno.com/2014/02/03/the-different-types-of-q-a/
[Steno Legal Q&A Test with Plover and Vim]: https://www.youtube.com/watch?v=wZFj0q0d9uo
[Tmuxinator]: https://github.com/tmuxinator/tmuxinator
[Vim]: https://www.vim.org/
[Vim Steno Q&A]: https://github.com/paulfioravanti/vim-steno-q-and-a
[`workflow_context.yml`]: https://github.com/openstenoproject/plover/blob/master/.github/workflows/ci/workflow_context.yml
