import os
from typing import List

import click

from .git import GitChecker, GitRepo
from .printer import Printer, LEVELS


@click.command()
@click.option("-i", "--include", multiple=True, type=str, default=[])
@click.option("-d", "--include-dir", multiple=True, type=str, default=[])
@click.option("-l", "--log-level", type=click.Choice(list(LEVELS)),
              default="info")
def main(include: List[str], include_dir: List[str], log_level: str):

    # Set up printer
    printer = Printer(level=log_level)

    for top_dir in include_dir:
        top_dir = os.path.abspath(os.path.expanduser(top_dir))
        printer.info(f"Getting all directories in {top_dir}")
        for sub_dir in os.listdir(top_dir):
            abs_path = os.path.join(top_dir, sub_dir)

            # Skip non-directories
            if not os.path.isdir(abs_path):
                printer.debug(f"{abs_path} is not a directory, skipping")
                continue

            # Skip non-repos without failing (TODO)

            # Analyze actual repos
            repo = GitRepo(abs_path, printer)
            checker = GitChecker(repo, printer)
            checker.run_checks()
    import sys; sys.exit()

    # Compile full list of directories to check
    # TODO: handle include_dir
    for path in include:
        path = os.path.abspath(os.path.expanduser(path))
        repo = GitRepo(path, printer)
        checker = GitChecker(repo, printer)
        checker.run_checks()
