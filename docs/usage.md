# Usage

```bash
$ acutter --help
```


## Creating a New Project

This will generate a new project:

```shell
$ cookiecutter https://github.com/romanchyla/acutter
```

Or using local repository (recommended):

```
$ git clone https://github.com/romanchyla/acutter
$ cd acutter
$ cookiecutter . -o /some/path
```

A new python project based on the template from the current folder will be written into `/some/path/<project-name>`.

Cookiecutter will ask you several details about the project.


## Updating Existing Projects

If you have created a project/library using this template, you can update it later:

1. check out cookiecutter and your library into a local filesystem
1. make sure to commit all changes in your library
1. call `acutter update /path/to/library`

We'll read settings from your library's `pyproject.toml` and generate a new template overwriting your files. So your last step is to review all changes and accept those that should stay, i.e.

```shell
$ cd /path/to/library
$ git status
$ git diff
$ ....
$ git checkout -- README.md # to revert to the previous version
$ ...
$ git commit -am "feat: Updated project tooling"
```

## Upgrading Existing Projects

If you want to convert a project/library which wasn't created from the template, follow these steps:

1. check out cookiecutter and your library into a local filesystem
1. call `acutter provision /path/to/library`
1. follow steps above for updating the project
