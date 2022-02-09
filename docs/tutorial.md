# Tutorial on how to use acutter and what to pay attention to

`acutter` is a cookie cutter template for ADS projects; both exploratory and production quality ones.

This document will list things that are important for developers.


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



### config.py + local_config.py

As opposed to build tools (which are configured in `pyproject.toml`) we put all of our configurations in:

- `config.py` for defaults, it is committed into Github
- `local_config.py` for customizations, it is **never** committed to Github

Our packages evolved to follow the convention of using `UPPER_CAMEL_CASE`. A value can be overriden by `env` variable but only if it was previously defined in `config.py`.


### requirements.txt

This was the old way to specify dependencies. Don't use it anymore. Instead, specify dependencies inside **project.dependencies** or in **optional-dependencies.\[name\]**.

### README

Basic info about the project, but it signal to the world the state (of maintenance/disrepair). It should point to:

- current status (passing/failing)
- code coverage
- documentation
- who is the main maintainer

### \.github/workflows


Every project will start with the Github CI configuration. These actions are ran on every pull request.

Various actions can be configured, by default we do:

- linting
- code formatting
- unittest

Optionally:

- generating documentation
- pushing release into PYPI

Also note the branch name. Github actions are configured to run against branch `main` (old projects had `master` to be their main branch; if you are updating an old project, you'll want to modify the `ci.yaml`)

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

When this happens, fix until you get:




## Usage

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


### Documentation

Yes, it is not easy...but try your best.

You can use `sphinx` [documentation style](https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html)

To regenerate: `acutter docs`

The documentation (when configured) will be automatically re-generated and uploaded to {{cookiecutter.package_name}}.readthedocs.io
