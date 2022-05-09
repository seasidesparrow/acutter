import os
import subprocess
from pathlib import Path


def run_cmd(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def run_pip(args):
    cmd = [".venv/bin/python", "-m", "pip"]
    cmd += args
    run_cmd(cmd)


def check_command_exists(cmd):
    try:
        run_cmd([cmd, "-h"], capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{cmd} command is not installed")
        return False
    return True


def install_virtualenv():
    if not check_command_exists("virtualenv"):
        return

    run_cmd(["virtualenv", ".venv"])

    run_pip(["install", "-e", ".[dev]"])
    run_pip(["install", ".[docs]"])

    print(
        """Virtualenv created inside {folder}/.venv
    
    In case of problems, you can run (manually):

    cd {folder}
    source .venv/bin/activate
    pip install -e .[dev]
    pip install .[docs]
    """.format(
            folder=os.path.abspath(".")
        )
    )


def initial_commit():
    # Init local repo
    run_cmd(["git", "init"])
    run_cmd(
        [
            "git",
            "remote",
            "add",
            "origin",
            "git@github.com:{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}.git",
        ]
    )
    run_cmd(["git", "add", "."])
    run_cmd(["git", "commit", "-m", "'feat: initial commit'"])
    run_cmd(["git", "branch", "-M", "main"])


def setup_github():
    """Create Github repo and set it up as remote."""
    if not check_command_exists("gh"):
        return

    # Create it on Github
    github_username = "{{ cookiecutter.github_username }}"
    # project_slug = "{{ cookiecutter.project_slug }}"
    project_name = "{{ cookiecutter.project_name }}"
    run_cmd(
        [
            "gh",
            "repo",
            "create",
            f"{github_username}/{project_name}",
            "-d",
            "{{ cookiecutter.project_short_description }}",
            "--{{cookiecutter.private_or_public}}",
            "--disable-wiki",
        ]
    )
    run_cmd(
        [
            "gh",
            "secret",
            "set",
            "PYPI_TOKEN",
            "-b'changeme'",
            "-R",
            f"{github_username}/{project_name}",
        ]
    )
    run_cmd(
        [
            "gh",
            "secret",
            "set",
            "GH_PAT",
            "-b'changeme'",
            "-R",
            f"{github_username}/{project_name}",
        ]
    )


def setup_pre_commit():
    if check_command_exists(".venv/bin/pre-commit"):
        # Run pre-commit install
        run_cmd([".venv/bin/pre-commit", "install"])
    elif check_command_exists("pre-commit"):
        # Run pre-commit install
        run_cmd(["pre-commit", "install"])


def main():

    package_name = "{{ cookiecutter.package_name }}"
    init_file = os.path.join(package_name, "__init__.py")
    if not os.path.exists(init_file):
        Path(init_file).touch()

    if "{{ cookiecutter.run_virtualenv_install }}" == "y":
        install_virtualenv()

    if "{{ cookiecutter.initial_commit }}" == "y":
        initial_commit()

    if "{{ cookiecutter.setup_github }}" == "y":
        setup_github()

    if "{{ cookiecutter.setup_pre_commit }}" == "y":
        setup_pre_commit()


if __name__ == "__main__":
    main()
