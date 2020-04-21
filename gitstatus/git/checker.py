import click

import typing

if typing.TYPE_CHECKING:
    from .repo import GitRepo
    from ..printer import Printer


class GitChecker:
    def __init__(self, repo: 'GitRepo', printer: 'Printer'):
        self.repo = repo
        self.printer = printer

    def run_checks(self):
        # Check for any stashed changes
        self.printer.info(f"Checking git repo {self.repo.path}")

        # Check if repo has a remote
        if not self._repo_has_remote():
            # TODO: print something
            return

        # Git fetch
        #self.repo.fetch()

        # Check status of current branch: any uncommitted changes? Any untracked files?
        # TODO
        # Handle cases where current ref is not a branch (could be rebasing, merging, etc.)

        # Get status of current refs and parse it
        refs = self.repo.get_refs()

        # Loop over branches and print status (behind, ahead, both, in-sync, no remote)
        for branch in sorted(refs, key=lambda d: d["name"]):
            self.printer.debug(f"Checking branch {branch['name']}", indent=1)
            if not branch["remote"]:
                msg = f"Branch '{branch['name']}' has no remote"
                self.printer.warning(msg, indent=1)
                break

            if "ahead" in branch["status"] and "behind" in branch["status"]:
                msg = (f"Branch '{branch['name']}' is out of sync with remote "
                       "(ahead and behind)")
                self.printer.error(msg, indent=1)
            elif "ahead" in branch["status"]:
                msg = f"Branch '{branch['name']}' is ahead of remote"
                self.printer.error(msg, indent=1)
            elif "behind" in branch["status"]:
                msg = "Branch '{branch['name']}' is behind remote"
                self.printer.error(msg, indent=1)
            elif not branch["status"]:
                msg = f"Branch '{branch['name']}' is synced with remote"
                self.printer.info(msg, indent=1)
            else:
                # TODO
                raise RuntimeError

    def _repo_has_remote(self):
        return "remote" in self.repo.config
