from .base import Issue


class RepoIssue(Issue):
    def __init__(self, name: str):
        super().__init__(name, type="repo")


# Instances
NO_REMOTE = RepoIssue("NO_REMOTE")
NOT_ON_BRANCH = RepoIssue("NOT_ON_BRANCH")
UNCOMMITTED_CHANGES = RepoIssue("UNCOMMITTED_CHANGES")
UNTRACKED_FILES = RepoIssue("UNTRACKED_FILES")
