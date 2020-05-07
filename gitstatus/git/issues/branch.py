from .base import Issue


class BranchIssue(Issue):
    def __init__(self, name: str):
        super().__init__(name, type="branch")


# Instances
NO_REMOTE = BranchIssue("NO_REMOTE")
AHEAD_OF_REMOTE = BranchIssue("AHEAD_OF_REMOTE")
BEHIND_REMOTE = BranchIssue("BEHIND_REMOTE")
INVALID_STATUS = BranchIssue("INVALID_STATUS")
