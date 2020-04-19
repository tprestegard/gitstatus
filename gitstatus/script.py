import os
from typing import List

import click

from .git import GitChecker, GitRepo
from .printer import Printer, LEVELS


# Helper function
def check_repo(path, printer: Printer):
   # Skip non-directories
   if not os.path.isdir(path):
       printer.debug(f"{path} is not a directory, skipping")
       return

   # Skip non-repos without failing
   try:
       repo = GitRepo(path, printer)
   except FileNotFoundError as ex:
       printer.debug(f"{path} does not appear to be a git repo, skipping")
       return

   # Analyze actual repos
   checker = GitChecker(repo, printer)
   checker.run_checks()

# TODO add option to pull branches that are behind. Possible issues with
# entering passwords for ssh keys?
# Add functionality like "stash_switch_branch_perform_action_and_switch_back
# to git repo to facilitate this
@click.command()
@click.option("-i", "--include", multiple=True, type=str, default=[])
@click.option("-d", "--include-dir", multiple=True, type=str, default=[])
@click.option("-l", "--log-level", default="info",
              type=click.Choice([k for k in LEVELS if k != "quiet"]))
def main(include: List[str], include_dir: List[str], log_level: str):

    # Set up printer
    printer = Printer(level=log_level)

    for top_dir in include_dir:
        top_dir = os.path.abspath(os.path.expanduser(top_dir))
        printer.debug(f"Getting all directories in {top_dir}")
        for sub_dir in os.listdir(top_dir):
            abs_path = os.path.join(top_dir, sub_dir)
            check_repo(abs_path, printer)

    # Compile full list of directories to check
    for path in include:
        path = os.path.abspath(os.path.expanduser(path))
        check_repo(path, printer)
