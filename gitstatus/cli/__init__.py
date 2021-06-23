import os
from typing import List

import click

# from .printer import Printer
# from ..checker import RepoChecker
from ..summary.summary import (
    SUMMARY_TYPES,
    DetailedSummary,
)


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
    # printer = Printer(level=log_level)

    # Dict for holding issues
    full_issues = {}

    # Get list of all repositories to check
    all_dirs = []

    # Loop over included directories
    for top_dir in include_dir:
        top_dir = os.path.abspath(os.path.expanduser(top_dir))
        sub_dirs = [
            os.path.join(top_dir, s)
            for s in os.listdir(top_dir)
            if os.path.isdir(os.path.join(top_dir, s))
        ]
        all_dirs.extend(sub_dirs)

    # Add repositories that were directly included
    all_dirs.extend(
        [os.path.abspath(os.path.expanduser(path)) for path in include]
    )

    # TODO: Loop over all repositories
    for repo in all_dirs:
        pass

    # Print summary
    summarizer = DetailedSummary(full_issues)
    print(summarizer.summarize())
