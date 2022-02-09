# Cookiecutter PyPackage

![release](https://github.com/romanchyla/acutter/actions/workflows/ci.yml/badge.svg)

<a href="https://github.com/cookiecutter/cookiecutter">
  <img src="https://img.shields.io/badge/cookiecutter-template-D4AA00.svg?style=flat-square&logo=cookiecutter" alt="Cookiecutter template badge">
</a>

Cookiecutter template for a Python Project. This is good both for libraries and applications (just delete features that you don't need).

## Features

The newly cut project will have those:

- Uses `pyproject.toml`.
- Provides automatically generated `setup.py` (to work around current tooling defficiencies).
- Testing with Pytest (locally and using Github actions).
- Follows the [black] style guide with [flake8] and [isort].
- Style guide enforced on CI.
- Follow to [the conventional commits][conventional-commits] specification.
- Automated releasing using [python-semantic-release][python-semantic-release].
- Documentation configured with Sphinx and [MyST Parser][myst].
- Standardised list of GitHub labels synchronised on push to master using [the labels CLI][pylabels].
- VSCode settings
- When used locally: ability to upgrade/convert existing projects/libraries

## Recommended Usage

Checkout the project locally, create a `virtualenv` and setup the project in a development mode (this way you can modify the code, and hopefully, submit a PR)

```bash
git clone https://github.com/romanchyla/cookiecutter-pyproject
virtualenv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```shell
cookiecutter https://github.com/romanchyla/cookiecutter-pyproject
```

Or locally:

```
cookiecutter . -o /some/path
```

This will create a new python package based on the template from the current folder - and as an output folder, it will write it into `/some/path/<project-name>`.

Before writing, cookiecutter will initiate series of questions that will determine details.

## Updating Cut Projects

If you have created a project/library using this template, you can update it later following those steps:

1. check out cookiecutter and your library into a local filesystem
1. make sure to commit all changes in your library
1. call `rtool update /path/to/library`

We'll read settings from your library's `pyproject.toml` and generate a new template overwriting your files. So your last step is to review all changes and accept those that should stay, i.e.

```shell
cd /path/to/library
git status
git diff
....
git checkout -- README.md # to revert to the previous version
...
git commit -am "feat: Updated project tooling"
```

## Upgrading Existing Projects

If you want to convert a project/library which wasn't created from the template, follow these steps:

1. check out cookiecutter and your library into a local filesystem
1. call `rtool provision /path/to/library`
1. follow step above for updating a project

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

[black]: https://github.com/psf/black
[flake8]: https://pypi.org/project/flake8/
[isort]: https://pypi.org/project/isort/
[pre-commit]: https://pre-commit.com/
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
[browniebroke/cookiecutter-pyproject](https://github.com/browniebroke/cookiecutter-pyproject)
project template.
