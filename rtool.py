import json
import os
import pprint
import shutil
import subprocess
import tempfile

import click
import slugify
import toml
from cookiecutter.main import cookiecutter


@click.group()
def cli():
    pass


@cli.command()
@click.argument("folder", type=click.Path(exists=True))
def provision(folder):
    """
    Generate pyproject.toml for a repository which doesn't have it.
    After this command was successful; you can run 'upgrade'
    """

    inputfile = os.path.join(folder, "pyproject.toml")
    if os.path.exists(inputfile):
        raise Exception(
            "This repo does have pyproject.toml file. Perhaps try 'update' command?"
            "Or delete {}".format(inputfile)
        )

    print(
        "First, we'll generate new cookiecutter - please answer these questions"
        "(do not worry, original repository will be unchanged"
    )
    # first run cookiecutter
    templatedir = os.path.dirname(__file__)
    tmpdir = tempfile.mkdtemp()
    context = {
        "initial_commit": "n",
        "setup_github": "n",
        "setup_pre_commit": "n",
        "private_or_public": "private",
        "run_virtualenv_install": "n",
        "project_name": os.path.basename(folder),
    }
    result = cookiecutter(
        templatedir,
        no_input=False,
        extra_context=context,
        overwrite_if_exists=True,
        output_dir=tmpdir,
    )

    # now grab the generated pyproject.toml and copy it
    newtoml = os.path.join(result, "pyproject.toml")

    if os.path.exists(newtoml):
        shutil.copyfile(newtoml, inputfile)
        print("New config written into: {}".format(inputfile))
    else:
        print("Process interrupted; no configuration generated")
        print(result)


@cli.command()
@click.argument("folder", type=click.Path(exists=True))
@click.option("--dry-run", default=False)
def upgrade(folder, dry_run):
    """Update repository which contains pyproject.toml

    When given path pointing to a repository (that was previously) created
    using our ookie cutter template, it will read info off that repo and
    regenerate the project; effectively updating the files.

    CAREFUL: you must manually review the changes and revert those that
    should not be accepted: i.e. use `git checkout -- <path>` to get them back

    """

    inputfile = os.path.join(folder, "pyproject.toml")
    if not os.path.exists(inputfile):
        raise Exception(
            "This repo doesnt have pyproject.toml file. Perhaps try 'provision' command?"
        )

    templatedir = os.path.dirname(__file__)
    context = get_project_context(inputfile, templatedir)
    output_dir = os.path.abspath(os.path.join(folder, ".."))

    if not dry_run:
        cookiecutter(
            templatedir,
            no_input=True,
            extra_context=context,
            overwrite_if_exists=True,
            output_dir=output_dir,
        )
    else:
        print("Would have called cookiecutter with:")
        pprint.pprint(
            dict(
                templatedir=templatedir,
                no_input=True,
                extra_context=context,
                overwrite_if_exists=True,
                output_dir=output_dir,
            )
        )


def get_project_context(inputfile, templatedir, template="cookiecutter.json"):

    # <project>/pyproject.toml
    tomldata = toml.load(inputfile)

    # cookiecutter json stuff
    with open(os.path.join(templatedir, template), "r") as fi:
        jdata = json.load(fi)

    project = tomldata["project"]
    print("Settings loaded from: {}\n".format(inputfile))
    pprint.pprint(project)
    print("-" * 80)

    print("Current cookicutter template defaults:\n")
    pprint.pprint(jdata)
    print("-" * 80)

    # those things should not be changed (in existing repository)
    out = {
        "initial_commit": "n",
        "setup_github": "n",
        "setup_pre_commit": "n",
        "private_or_public": "private",
        "run_virtualenv_install": "n",
    }

    # take the first entry name
    out["email"] = project.get("authors", [{"email": None}])[0].get(
        "email", jdata["email"]
    )
    out["full_name"] = project.get("authors", [{"name": None}])[0].get(
        "name", jdata["full_name"]
    )
    repo = project.get("repository", None)
    if repo:
        parts = repo.rsplit("/", 2)
        out["github_username"] = parts[1]
        out["project_name"] = parts[2].replace(".git", "")
        out["package_name"] = project.get(
            "packages", [slugify.slugify(out["project_name"])]
        )[0]
        out["project_slug"] = out["package_name"]

    out["open_source_license"] = project.get(
        "license", {"text": "Not open source"}
    ).get("text")
    out["version"] = project.get("version", jdata["version"])
    out["project_short_description"] = project.get(
        "description", jdata["project_short_description"]
    )

    print("And this is what we'll use:\n")
    pprint.pprint(out)
    print("-" * 80)
    return out


if __name__ == "__main__":
    import sys

    sys.argv.append("provision")
    sys.argv.append("/dvt/workspace/rprojc/")
    cli()
