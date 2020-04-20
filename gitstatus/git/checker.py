import click

import typing

if typing.TYPE_CHECKING:
    from .repo import GitRepo
    from ..printer import Printer


LOG_MSG_HEADER = "Repo {repo} [{branch}]"
BRANCH_STATUSES = {
    "no-remote": "No remote",
    "ahead": "Ahead of remote",
    "behind": "Behind remote",
    "both": "Out of sync with remote (both ahead and behind)",
    "synced": "In sync with remote",
}
FULL_STATUS_LOG_MSGS = {k: " | ".join([LOG_MSG_HEADER, v])
                        for k, v in BRANCH_STATUSES.items()}


class GitChecker:
    def __init__(self, repo: 'GitRepo', printer: 'Printer'):
        self.repo = repo
        self.printer = printer

    def run_checks(self):
        # Check for any stashed changes
        self.printer.debug(f"Checking git repo {self.repo.path}")

        # Check if repo has a remote
        if not self._repo_has_remote():
            # TODO: print something
            return

        # Git fetch
        self.repo.fetch()

        # Check status of current branch: any uncommitted changes? Any untracked files?
        # TODO
        # Handle cases where current ref is not a branch (could be rebasing, merging, etc.)

        # Get status of current refs and parse it
        refs = self.repo.get_refs()

        # Loop over branches and print status (behind, ahead, both, in-sync, no remote)
        for branch in sorted(refs, key=lambda d: d["name"]):
            self.printer.debug(f"Checking branch {branch['name']}")
            if not branch["remote"]:
                msg = FULL_STATUS_LOG_MSGS.get("no-remote").format(
                    repo=self.repo.path, branch=branch["name"])
                self.printer.warning(msg)
                break

            print_method = "error"
            if "ahead" in branch["status"] and "behind" in branch["status"]:
                msg_key = "both"
            elif "ahead" in branch["status"]:
                msg_key = "ahead"
            elif "behind" in branch["status"]:
                msg_key = "behind"
            elif not branch["status"]:
                msg_key = "synced"
                print_method = "info"
            else:
                # TODO
                raise RuntimeError
            msg = FULL_STATUS_LOG_MSGS.get(msg_key).format(
                repo=self.repo.path, branch=branch["name"])
            getattr(self.printer, print_method)(msg)

    def _repo_has_remote(self):
        return "remote" in self.repo.config
