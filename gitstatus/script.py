import os
from typing import List

import click

from .git import GitChecker, GitRepo
from .printer import Printer, LEVELS


# Helper function
def check_repo(path: str, printer: Printer, **kwargs):
    # Skip non-directories
    if not os.path.isdir(path):
        printer.debug(f"{path} is not a directory, skipping")
        return

    # Skip non-repos without failing
    try:
        repo = GitRepo(path)
    except FileNotFoundError:
        printer.debug(f"{path} does not appear to be a git repo, skipping")
        return

    # Get parameters from kwargs
    pull_behind = kwargs.get("pull_behind", False)
    skip_fetch = kwargs.get("skip_fetch", False)

    # Analyze actual repos
    checker = GitChecker(repo, printer, pull_behind=pull_behind,
                         skip_fetch=skip_fetch)
    checker.run_checks()


@click.command()
@click.option("-i", "--include", multiple=True, type=str, default=[])
@click.option("-d", "--include-dir", multiple=True, type=str, default=[])
@click.option("-l", "--log-level", default="info",
              type=click.Choice([k for k in LEVELS if k != "quiet"]))
@click.option("--pull-behind", is_flag=True,
              help="Pull any branches that are behind remote. Only for cases "
                   "where a simple pull will sync the branches.")
@click.option("--skip-fetch", is_flag=True,
              help="Skip fetching from remote to speed up runtime.")
def main(include: List[str], include_dir: List[str], log_level: str,
         pull_behind: bool, skip_fetch: bool):
    """
    TBD full docstring
    """

    # Set up printer
    printer = Printer(level=log_level)

    # Loop over included directories
    for top_dir in include_dir:
        top_dir = os.path.abspath(os.path.expanduser(top_dir))
        printer.debug(f"Getting all directories in {top_dir}")
        for sub_dir in os.listdir(top_dir):
            abs_path = os.path.join(top_dir, sub_dir)
            check_repo(abs_path, printer, pull_behind=pull_behind,
                       skip_fetch=skip_fetch)

    # Loop over repos that were directly included
    for path in include:
        path = os.path.abspath(os.path.expanduser(path))
        check_repo(path, printer, pull_behind=pull_behind,
                   skip_fetch=skip_fetch)
