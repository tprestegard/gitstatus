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
    def __init__(self, repo: 'GitRepo', printer: 'Printer', **kwargs):
        self.repo = repo
        self.printer = printer
        self.kwargs = kwargs

    def run_checks(self):
        # Check for any stashed changes
        self.printer.debug(f"Checking git repo {self.repo.path}")

        # Check if repo has a remote
        if not self._repo_has_remote():
            self.printer.error(f"Git repo {self.repo.path} has no remote")
            return

        # Git fetch
        if not self.kwargs.get("skip_fetch", False):
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
                continue

            if "ahead" in branch["status"] and "behind" in branch["status"]:
                msg_key = "both"
            elif "ahead" in branch["status"]:
                msg_key = "ahead"
            elif "behind" in branch["status"]:
                msg_key = "behind"
            elif not branch["status"]:
                msg_key = "synced"
            else:
                # TODO
                raise RuntimeError

            # Get handler and run
            msg = FULL_STATUS_LOG_MSGS.get(msg_key).format(
                repo=self.repo.path, branch=branch["name"])
            handler = getattr(self, f"_handler_{msg_key}")
            handler(msg, branch_name=branch["name"])

    def _repo_has_remote(self):
        return "remote" in self.repo.config

    def _handler_behind(self, msg: str, **kwargs):
        self.printer.error(msg)
        if self.kwargs.get("pull_behind", False):
            branch_name = kwargs.get("branch_name", None)
            if branch_name:
                try:
                    self.repo.pull_branch(branch_name)
                except Exception:
                    self.printer.error("error pulling")
                    raise
                self.printer.info("Branch updated")

    def _handler_both(self, msg: str, **kwargs):
        self.printer.error(msg)

    _handler_ahead = _handler_both

    def _handler_synced(self, msg: str, **kwargs):
        self.printer.info(msg)
