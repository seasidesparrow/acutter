import subprocess

import click


@click.group()
def cli():
    pass


@cli.command()
def docs():
    """Will build documentation"""
    subprocess.check_call(["sphinx-build", "docs", ".docs"])


if __name__ == "__main__":
    cli()
