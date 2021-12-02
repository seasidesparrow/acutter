# Cookiecutter PyPackage

<a href="https://github.com/browniebroke/cookiecutter-pypackage/actions?query=workflow%3ACI">
  <img src="https://img.shields.io/github/workflow/status/browniebroke/cookiecutter-pypackage/CI/main?label=Test&logo=github&style=flat-square" alt="CI Status" >
</a>
<a href="https://github.com/cookiecutter/cookiecutter">
  <img src="https://img.shields.io/badge/cookiecutter-template-D4AA00.svg?style=flat-square&logo=cookiecutter" alt="Cookiecutter template badge">
</a>

Cookiecutter template for a Python Package.

## Installation

In order to use `cookiecutter` you'll want to have `poetry` installed; for linux these are the steps:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source ~/.poetry/env
```

After which you can set the project up:

```bash
poetry install
```

Poetry will create a python virtualenv inside the project `.venv` folder. To activate it:

```
poetry shell
```

And now you can start cutting cookies.

## Usage

```
cookiecutter . -o /dvt/workspace
```

This will create a new python package based on the template from the current folder - and as an output folder, it will write it into `/dvt/workspace/<package-name>`. Before writing, cookiecutter will initiate series of questions that will determine details.


## Additional Features (Github)

The project can be set up with github hooks and additional goodies. In order to use that functionality, you'll need to have `gh` installed on the command line:

For linux:

```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

And after that, do `gh auth login` and follow instructions to generate/save access token.



## Features

- Project for Python 3.7+.
- Testing with Pytest using Github actions.
- Packaging powered by [poetry]
- Follows the [black] style guide with [flake8] and [isort].
- Comes with [pre-commit] hook config for black, isort, flake8 and [pyupgrade](https://github.com/asottile/pyupgrade).
- Style guide enforced on CI.
- Dependencies kept up to date by [Renovate].
- Follow to [the conventional commits][conventional-commits] specification.
- Automated releasing using [python-semantic-release][python-semantic-release].
- Documentation configured with Sphinx and [MyST Parser][myst].
- Standardised list of GitHub labels synchronised on push to master using [the labels CLI][pylabels].

## Usage

Generate a new project with:

```shell
cookiecutter https://github.com/browniebroke/cookiecutter-pypackage
```

This will prompt you for a few questions and create new directory with the name you used as project slug.

### Start developing

The project uses [Poetry] for dependencies management and packaging. Make sure you have it installed in your development machine. To install the development dependencies in a virtual environment, type:

```shell
poetry install
```

This will also generate a `poetry.lock` file, you should track this file in version control. To execute the test suite, call pytest inside Poetry's virtual environment via `poetry run`:

```shell
poetry run pytest
```

Check out the [Poetry] documentation for more information on the available commands.

### GitHub Actions

When you first push to GitHub, it'll start a `ci` GitHub workflow that you can see in the "Actions" tab of your repository. This workflow runs a couple of jobs:

- The `test` job will run your test suite with Pytest against all Python version from 3.7 to 3.9
- A few things will run in the lint job:
  - black in check mode
  - isort in check mode
  - flake8
  - pyupgrade for Python 3.7+

A `labels` workflow will also run and synchronise the GitHub labels based on the `.github/labels.toml` file.

### Secrets

The workflows need [a few secrets][gh-secrets] to be setup in your GitHub repository:

- `PYPI_TOKEN` to publish releases to [PyPI][pypi]. This one should be created as `release` environment secret.
- `GH_PAT` a [personal access token (PAT) with the `repo` scope][create-pat] for opening pull requests and updating the repository topics. This is used by the `hacktoberfest` workflow.
- `CODECOV_TOKEN` to upload coverage data to [codecov.io][codecov] in the Test workflow (optional for public repos).

If you have the GitHub CLI installed and chose to set up GitHub, they will be created with a dummy value.

### Automated release

By following the conventional commits specification, we're able to completely automate versioning and releasing to PyPI. This is handled by the `semantic-release.yml` workflow. It is triggered manually by default, but can be configured to run on every push to your main branch.

Here is an overview of its features:

- Check the commit log since the last release, and determine the next version to be released.
- If no significant change detected, stop here (e.g. just dependencies update).
- Otherwise, bump the version in code locations specified in `setup.cfg`.
- Update the `CHANGELOG.md` file.
- Commit changes.
- Create a git tag.
- Push to GitHub.
- Create a release in GitHub with the changes as release notes.
- Build the source and binary distribution (wheel).
- Upload the sources to PyPI and attach them to the Github release.

For more details, check out the [conventional commits website][conventional-commits] and [Python semantic release][python-semantic-release] Github action.

### Pre-commit

The project comes with the config for [pre-commit]. If you're not familiar with it, follow their documentation on how to install it and set it up.

### Documentation

The project assumes that the documentation will be hosted on Read the Docs and written in Markdown with the [MyST parser for Sphinx][myst].

To enable it, you might need to go [into your dashboard][rtd-dashboard] and import the project from Github. Everything else should work out of the box.

### Dependencies update

The project dependencies are kept up to date with [Renovate] which requires [the Github app][renovate-gh-app] to be installed.

The main advantage of Renovate over Dependabot is the auto-merge option, which is configured to automatically merge minor/patch updates with all the CI checks passing. It supports a variety of package managers, including Poetry, GitHub actions and pre-commit hooks which are used by default.



[poetry]: https://python-poetry.org/
[black]: https://github.com/psf/black
[flake8]: https://pypi.org/project/flake8/
[isort]: https://pypi.org/project/isort/
[pre-commit]: https://pre-commit.com/
[renovate]: https://docs.renovatebot.com/
[renovate-gh-app]: https://github.com/apps/renovate
[conventional-commits]: https://www.conventionalcommits.org
[python-semantic-release]: https://github.com/relekang/python-semantic-release
[myst]: https://myst-parser.readthedocs.io
[pylabels]: https://github.com/hackebrot/labels
[gh-secrets]: https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets
[codecov]: https://codecov.io/
[pypi]: https://pypi.org/
[create-pat]: https://github.com/settings/tokens/new?scopes=repo
[rtd-dashboard]: https://readthedocs.org/dashboard/


## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[browniebroke/cookiecutter-pypackage](https://github.com/browniebroke/cookiecutter-pypackage)
project template.
