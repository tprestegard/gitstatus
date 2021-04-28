from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from git import Head, Repo


class RepoChecker:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.fetch = kwargs.get("fetch", False)
        self.repo_issues = []
        self.branch_issues = {}

    def check_repo(self, repo: "Repo") -> List["Issues"]:
        issues = []

        # Does repo have a remote?
        if len(repo.remotes) == 0:
            issues.append(REPO.NO_REMOTE)

        # Is repo currently on a branch?
        if not repo.active_branch:
            issues.append(REPO.NOT_ON_BRANCH)

        # Any uncommitted changes?
        if self.repo.has_uncommitted_changes:
            self.repo_issues.append(REPO.UNCOMMITTED_CHANGES)

        # Any untracked files?
        if len(repo.untracked_files) > 0:
            issues.append(REPO.UNTRACKED_FILES)

        # Any stashed changes?
        if repo.git.stash("list"):
            issues.append(REPO.STASHED_CHANGES)

        # Git fetch
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
        refs = self.repo.get_refs()

        # Loop over branches and check for issues
        for branch in repo.branches:
            issues.extend(self.check_branch(branch))

    def check_branch(self, branch: "Head") -> List["Issues"]:
        issues = []
        if not branch.tracking_branch():
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
