# What Devs Need to Understand

`acutter` is a cookie cutter template for ADS projects; both exploratory and production quality ones.

This document will list things that are important for developers.

## acutter


### Installation

Package: `pip install <package>`

Optional dependencies: `pip install <package>.[docs]`


### Development

You **should want** to work in local development mode, it is by far the easiest for making changes.

It is **strongly recommended** to use a **virtualenv** (or its cousins):

```bash
virtualenv .venv
source .venv/bin/activate
```

Installation: `pip install -e .`

This will create symbolic links to the code you are updating; all changes are automatically available.

NOTE: Sometimes you have to re-do `pip install -e .` after you have run another `pip install...`.


### Automated release (XXX)

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


### Making a release manually

```bash
$ semantic-release version --patch
```

Will make a new release and publish the tag to Github. (and optionally: upload the package to PYPI). 

This process could be automated (in Github actions) but don't do that.

Our automated deployment picks and tries to deploy (to DEV namespace) any new release/tag it finds. You as a developer are the **intelligent agent** responsible for making the decision: is my code ready to be deployed? If the answer is YES, then use `semantic-release` tool version with appropriate tags (`--patch/minor/major`).

And yes: you could publish a release which does not pass all checks and unittests. That is OK, but it is **NOT OK** to do that systematically.


### Documentation

Yes, it is not easy...but try your best to write it.

The project assumes that the documentation will be hosted on Read the Docs and written in Markdown with the [MyST Parser][myst].

To enable it, you might need to go [into your dashboard][https://readthedocs.org/dashboard/] and import the project from Github. Everything else should work out of the box.

To generate documentation: `acutter docs`

And easy to publish: TBD

The documentation (when configured) will be automatically re-generated and uploaded to {{cookiecutter.package_name}}.readthedocs.io


## pyproject.toml

`pyproject.toml` is the new Python standard for configuring projects.


It looks like this:

```{literalinclude} ../pyproject.toml

```

### \[dependencies\]

As opposed to `pip`'s requirements.txt everything inside this section must have this format:

```python

dependencies = [
    'click==8.0.3',
    'package@git+ssh://git@github.com/adsabs/repo-name@[v1.1]#egg=some-pkg',
    'package@git+https://github.com/someorgname/pkg-repo-name@[v1.1]#egg=some-pkg',
]
```

It is **strongly recommended** that you always specify `==version`.


### \[build-system\]

This section looks innocent, but it is very consequential. Thanks to it, a package, when installed, is compiled in **an independent** python environment, using whichever build tool we say it should be used.

Notice for instance that during build we depend on `ppsetuptools` but that package is not part of `dependencies`.

BUT! Be careful what packaging tool you are using. Many of them profess to be the new Mesiah, but are just opinionated fools - and for example cannot deal efficiently with package dependencies (and run in quadratic time which really is going to slow you down) or outright make it impossible to deploy packages that normally just produce a warning (e.g. if your package depends on a library that has not been updated and lists old requirements).

Best if you leave this section as it is.



### \[tool.xxxx\]

These sections contain configuration for **dependencies** of your project. Sometimes the dependency doesn't support `.toml` format yet, in which case we place configuration inside `setup.cfg`

Example is:

```{literalinclude} ../setup.cfg
```

### \[xsetup....\]

This section is non-standard, a hack, or rather a clever workaround. Certain build tools do not yet support `pyproject.toml` and they require `setup.py build...` - but that would mean that the same configuration had to live in two different places, and eventually and inevitably diverge...

So we have built a custom `setup.py` which will read the values from `pyproject.toml` and serve them to the rest of the `setuptools` eco system. Keep it. It is good!



## Parts that matter


### Typical project structure

Most of our projects will have this, time tested, structure:

```bash
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── README.md
├── setup.cfg
├── setup.py
├── config.py
├── local_confi.py
├── docs
│   └── ...
├── {{cookiecutter.package_name}}
│   ├── __init__.py
│   ├── cli.py
│   └── version.py
└── tests
    └── __init__.py
```

### README

Basic info about the project, but it signal to the world the state (of maintenance/disrepair). It should point to:

- current status (passing/failing)
- code coverage
- documentation
- who is the main maintainer


### config.py + local_config.py

As opposed to build tools (which are configured in `pyproject.toml`) we put all of our configurations in:

- `config.py` for defaults, it is committed into Github
- `local_config.py` for customizations, it is **never** committed to Github

Our packages evolved to follow the convention of using `UPPER_CAMEL_CASE`. A value can be overriden by `env` variable but only if it was previously defined in `config.py`.




### Github Actions (\.github/workflows)

When you first push to GitHub, it'll start a `ci` GitHub workflow that you can see in the "Actions" tab of your repository. This workflow runs a couple of jobs:

- The `test` job will run your test suite with Pytest against all Python version from 3.7 to 3.9
- A few things will run in the lint job:
  - black in check mode
  - isort in check mode
  - flake8

A `labels` workflow will also run and synchronise the GitHub labels based on the `.github/labels.toml` file.

Various other actions can be configured, by default we do:

- linting
- code formatting
- unittest

Optionally:

- generating documentation
- pushing release into PYPI

Also note the branch name. Github actions are configured to run against branch `main` (old projects had `master` to be their main branch; if you are updating an old project, you'll want to modify the `ci.yaml`)


### Secrets

The workflows need [a few secrets][https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets] to be setup in your GitHub repository:

- `PYPI_TOKEN` to publish releases to [PyPI][pypi]. This one should be created as `release` environment secret.
- `GH_PAT` a [personal access token (PAT) with the `repo` scope][create-pat] for opening pull requests and updating the repository topics. This is used by the `hacktoberfest` workflow.
- `CODECOV_TOKEN` to upload coverage data to [codecov.io][codecov] in the Test workflow (optional for public repos).

If you have the GitHub CLI installed and chose to set up GitHub, they will be created with a dummy value.


### hooks

Customizations to a cookiecutter template. You'll not find them in a normal (generated) project.

### \.pre-commit-config.yaml

Checks and actions that will be ran before every commit.

You can select whether these `pre-commit`s are installed when a project is generated, but you can always activate it by: `pre-commit install`

```{literalinclude} ../.pre-commit-config.yaml
```

Here is an example of how stuff looks when checks fail:

```bash
git commit -am "feat: refactoring and writing a tutorial"
Trim Trailing Whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook

Fixing docs/tutorial.md

Fix End of Files.........................................................Failed
- hook id: end-of-file-fixer
- exit code: 1
- files were modified by this hook

Fixing .gitignore
Fixing docs/tutorial.md

Debug Statements (Python)................................................Passed
isort....................................................................Passed
black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted acutter/cli.py
All done! ✨ 🍰 ✨
1 file reformatted, 2 files left unchanged.

flake8...................................................................Passed
```

When this happens, fix until you get all passed:


```bash
git commit -am "feat: refactoring and writing a tutorial"
Fix End of Files.........................................................Passed
Debug Statements (Python)................................................Passed
isort....................................................................Passed
black....................................................................Passed
flake8...................................................................Passed
```


But even when then a failure can happen. Checks only examine the files you have changed, sometimes you'll want to use this:

```bash
$ pre-commit run --all-files
```

## Additional Features (Github)

The project can be set up with github hooks and additional goodies. In order to use that functionality, you'll need to have `gh` installed on the command line:

For linux:

```bash
$ curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/$ null
$ sudo apt update
$ sudo apt install gh
```

And after that, do `gh auth login` and follow instructions to generate/save access token.


### requirements.txt

This was the old way to specify dependencies. Don't use it anymore. Instead, specify dependencies inside **project.dependencies** or in **optional-dependencies.\[name\]**.




[black]: https://github.com/psf/black
[flake8]: https://pypi.org/project/flake8/
[isort]: https://pypi.org/project/isort/
[pre-commit]: https://pre-commit.com/
[conventional-commits]: https://www.conventionalcommits.org
[python-semantic-release]: https://github.com/relekang/python-semantic-release
[myst]: https://myst-parser.readthedocs.io
[pylabels]: https://github.com/hackebrot/labels
[codecov]: https://codecov.io/
[pypi]: https://pypi.org/
[create-pat]: https://github.com/settings/tokens/new?scopes=repo
