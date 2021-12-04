import subprocess


def run_cmd(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def check_command_exists(cmd):
    try:
        run_cmd([cmd, "-h"], capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{cmd} command is not installed")
        return False
    return True


def run_virtualenv_install():
    if not check_command_exists("virtualenv"):
        return

    run_cmd(["virtualenv", ".venv"])
    run_cmd(["pip", "install", ".[dev]"])


def initial_commit():
    # Init local repo
    run_cmd(["git", "init"])
    run_cmd(
        [
            "git",
            "remote",
            "add",
            "origin",
            "git@github.com:{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git",
        ]
    )
    run_cmd(["git", "add", "."])
    run_cmd(["git", "commit", "-m", "'feat: initial commit'"])


def setup_github():
    """Create Github repo and set it up as remote."""
    if not check_command_exists("gh"):
        return

    # Create it on Github
    github_username = "{{ cookiecutter.github_username }}"
    project_slug = "{{ cookiecutter.project_slug }}"
    run_cmd(
        [
            "gh",
            "repo",
            "create",
            f"{github_username}/{project_slug}",
            "-d",
            "{{ cookiecutter.project_short_description }}",
            "--public",
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
            f"{github_username}/{project_slug}",
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
            f"{github_username}/{project_slug}",
        ]
    )


def setup_pre_commit():
    if not check_command_exists("pre-commit"):
        return

    # Run pre-commit install
    run_cmd(["pre-commit", "install"])


def main():
    if "{{ cookiecutter.run_virtualenv_install }}" == "y":
        run_virtualenv_install()

    if "{{ cookiecutter.initial_commit }}" == "y":
        initial_commit()

    if "{{ cookiecutter.setup_github }}" == "y":
        setup_github()

    if "{{ cookiecutter.setup_pre_commit }}" == "y":
        setup_pre_commit()


if __name__ == "__main__":
    main()
