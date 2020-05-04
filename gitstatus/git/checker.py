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
        self.repo_issues = []
        self.branch_issues = {}

    def run_checks(self):
        # Check some things about the current status of the repo
        self.repo_issues
        self.data.update({
            "has_remote": self._repo.has_remote(),
            "on_branch": bool(self.repo.current_branch),
            "uncommitted_changes": self.repo.has_uncommitted_changes,
            "untracked_files": self.

        })["has_remote"] = self._repo_has_remote()
        self.data

        if not self._repo_has_remote():
            self.repo_issues.append() # TODO
            self.data["has_remote"] = False
            return

        # Is repo currently on a branch?
        if not self.repo.current_branch:
            self.data["on_branch"] = False

        # Any uncommitted changes?
        if self.repo.has_uncommitted_changes:
            self.data["uncommitted_changes"] 
            self.printer.echo(f"Repo {self.repo.path} has uncommitted "
                              "changes", level="debug", indent=1)

        # Any untracked files?
        if self.repo.has_untracked_files:
            self.printer.echo(f"Repo {self.repo.path} has untracked files",
                              level="debug", indent=1)

        # Git fetch
        if not self.kwargs.get("skip_fetch", False):
            try:
                self.repo.fetch()
            except Exception as ex:
                self.printer.echo(f"Error fetching remote for repo "
                                  "{self.repo.path}: {str(ex)}")

        # Get status of current refs and parse it
        refs = self.repo.get_refs()

        # Loop over branches and print status (behind, ahead, both, in-sync,
        # no remote)
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
                raise ValueError(f'Invalid branch status {branch["status"]}')

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
                    self.printer.error("Error pulling branch from remote")
                else:
                    self.printer.echo("Branch updated", level="debug")

    def _handler_both(self, msg: str, **kwargs):
        self.printer.error(msg)

    _handler_ahead = _handler_both

    def _handler_synced(self, msg: str, **kwargs):
        self.printer.info(msg)
