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

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[browniebroke/cookiecutter-pyproject](https://github.com/browniebroke/cookiecutter-pyproject)
project template.
