from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .repo import GitRepo
    from ..printer import Printer

from .issues import repo as REPO, branch as BRANCH


class GitChecker:
    def __init__(self, repo: "GitRepo", printer: "Printer", **kwargs):
        self.repo = repo
        self.printer = printer
        self.kwargs = kwargs
        self.repo_issues = []
        self.branch_issues = {}

    def run_checks(self):
        # Does repo have a remote?
        if not self._repo_has_remote():
            self.repo_issues.append(REPO.NO_REMOTE)

        # Is repo currently on a branch?
        if not self.repo.current_branch:
            self.repo_issues.append(REPO.NOT_ON_BRANCH)

        # Any uncommitted changes?
        if self.repo.has_uncommitted_changes:
            self.repo_issues.append(REPO.UNCOMMITTED_CHANGES)

        # Any untracked files?
        if self.repo.has_untracked_files:
            self.repo_issues.append(REPO.UNTRACKED_FILES)

        # TODO: any stashed changes?

        # Git fetch
        if not self.kwargs.get("skip_fetch", False):
            try:
                self.repo.fetch()
            except Exception as ex:
                self.printer.echo(
                    "Error fetching remote for repo "
                    f"{self.repo.path}: {str(ex)}"
                )

        # Get status of current refs and parse it
        refs = self.repo.get_refs()

        # Loop over branches and check for issues
        for branch in sorted(refs, key=lambda d: d["name"]):
            self.branch_issues[branch["name"]] = self.check_branch(branch)

    def check_branch(self, branch: Dict[str, str]):
        issues = []
        if not branch["remote"]:
            issues.append(BRANCH.NO_REMOTE)
            return issues

        if "ahead" in branch["status"] and "behind" in branch["status"]:
            issues.append(BRANCH.AHEAD_OF_REMOTE)
            issues.append(BRANCH.BEHIND_REMOTE)
        elif "ahead" in branch["status"]:
            issues.append(BRANCH.AHEAD_OF_REMOTE)
        elif "behind" in branch["status"]:
            issues.append(BRANCH.BEHIND_REMOTE)
        elif not branch["status"]:
            pass
        else:
            issues.append(BRANCH.INVALID_STATUS)

        return issues

    def _repo_has_remote(self):
        return "remote" in self.repo.config
