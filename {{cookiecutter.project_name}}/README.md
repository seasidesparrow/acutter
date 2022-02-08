# {{ cookiecutter.project_name }}


<p align="center">
  
  ![CI Status](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}/actions/workflows/ci.yml/badge.svg)
  
  <!--
  <a href="https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}">
    <img src="https://img.shields.io/codecov/c/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
  //-->
</p>

{{ cookiecutter.project_short_description }}

## Installation

Install this via pip (or your favourite package manager):

```bash
pip install {{ cookiecutter.project_slug }}
```


## Development

Install locally into virtualenv

```bash
virtualenv .venv
source .venv/bin/activate
python rtool.py install
```

## Documentation

[documentation](https://{{cookiecutter.project_slug}}.readthedocs.io)

