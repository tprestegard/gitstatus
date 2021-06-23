from typing import List, TYPE_CHECKING

from git import Repo
from git.exc import InvalidGitRepositoryError

from .issues import BranchIssue, RepoIssue


if TYPE_CHECKING:  # pragma: no cover
    from git import Head
    from .issues import Issue


class RepoChecker:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.fetch = kwargs.get("fetch", False)
        self.repo_issues = []
        self.branch_issues = {}

    def check_repo(self, path: str) -> List["Issue"]:
        issues = []

        # Check if it's even a repo
        try:
            repo = Repo(path)
        except InvalidGitRepositoryError:
            return [RepoIssue.NOT_A_REPO]

        # Does repo have a remote?
        if len(repo.remotes) == 0:
            issues.append(RepoIssue.NO_REMOTE)

        # Is repo currently on a branch?
        if not repo.active_branch:
            issues.append(RepoIssue.NOT_ON_BRANCH)

        # Any uncommitted changes?
        if self.repo.has_uncommitted_changes:
            self.repo_issues.append(RepoIssue.UNCOMMITTED_CHANGES)

        # Any untracked files?
        if len(repo.untracked_files) > 0:
            issues.append(RepoIssue.UNTRACKED_FILES)

        # Any stashed changes?
        if repo.git.stash("list"):
            issues.append(RepoIssue.STASHED_CHANGES)

        # Optionally run a fetch
        if self.fetch:
            try:
                for remote in repo.remotes:
                    remote.fetch()
            except Exception as ex:
                self.printer.echo(
                    "Error fetching remote for repo "
                    f"{self.repo.path}: {str(ex)}"
                )

        # Get status of current refs and parse it
        #refs = self.repo.get_refs()

        # Loop over branches and check for issues
        for branch in repo.branches:
            issues.extend(self.check_branch(branch))

    def check_branch(self, branch: "Head") -> List["Issue"]:
        issues = []
        if not branch.tracking_branch():
            issues.append(BranchIssue.NO_REMOTE)
            return issues

        if "ahead" in branch["status"] and "behind" in branch["status"]:
            issues.append(BranchIssue.OUT_OF_SYNC_WITH_REMOTE)
        elif "ahead" in branch["status"]:
            issues.append(BranchIssue.AHEAD_OF_REMOTE)
        elif "behind" in branch["status"]:
            issues.append(BranchIssue.BEHIND_REMOTE)
        elif not branch["status"]:
            pass
        else:
            issues.append(BranchIssue.INVALID_STATUS)

        return issues
