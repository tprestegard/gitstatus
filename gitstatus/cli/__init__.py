import os
from typing import List

import click

from .printer import Printer
from ..git import GitChecker, GitRepo
from ..summary.summary import (
    SUMMARY_TYPES,
    DetailedSummary,
)


# Helper function
def check_repo(path: str, printer: Printer, **kwargs):
    # Skip non-directories
    if not os.path.isdir(path):
        printer.echo(f"{path} is not a directory, skipping", level="debug")
        return

    # Skip non-repos without failing
    try:
        repo = GitRepo(path)
    except FileNotFoundError:
        printer.echo(
            f"{path} does not appear to be a git repo, skipping", level="debug"
        )
        return

    # Analyze actual repos
    checker = GitChecker(repo, printer, **kwargs)
    checker.run_checks()

    # Combine issues and return
    return {
        "repo": checker.repo_issues,
        "branch": checker.branch_issues,
    }


@click.command()
@click.option("-i", "--include", multiple=True, type=str, default=[])
@click.option("-d", "--include-dir", multiple=True, type=str, default=[])
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode")
@click.option(
    "-s",
    "--summary-type",
    type=click.Choice(list(SUMMARY_TYPES)),
    default=list(SUMMARY_TYPES)[0],
    show_default=True,
    help="TBD",
)
@click.option(
    "--pull-behind",
    is_flag=True,
    help="Pull any branches that are behind remote. Only for cases "
    "where a simple pull will sync the branches.",
)
@click.option(
    "--skip-fetch",
    is_flag=True,
    help="Skip fetching from remote to speed up runtime.",
)
def main(
    include: List[str],
    include_dir: List[str],
    verbose: bool,
    summary_type: str,
    pull_behind: bool,
    skip_fetch: bool,
):
    """
    TBD full docstring
    """
    # Get log level based on verbose arg
    log_level = "debug" if verbose else "info"

    # Set up printer
    printer = Printer(level=log_level)

    # Dict for holding issues
    full_issues = {}

    # Loop over included directories
    for top_dir in include_dir:
        top_dir = os.path.abspath(os.path.expanduser(top_dir))
        for sub_dir in os.listdir(top_dir):
            abs_path = os.path.join(top_dir, sub_dir)
            issues = check_repo(
                abs_path,
                printer,
                pull_behind=pull_behind,
                skip_fetch=skip_fetch,
            )
            if issues is not None:
                full_issues[abs_path] = issues

    # Loop over repos that were directly included
    for path in include:
        abs_path = os.path.abspath(os.path.expanduser(path))
        issues = check_repo(
            abs_path, printer, pull_behind=pull_behind, skip_fetch=skip_fetch
        )
        if issues is not None:
            full_issues[abs_path] = issues

    # Print summary
    summarizer = DetailedSummary(full_issues)
    print(summarizer.summarize())
