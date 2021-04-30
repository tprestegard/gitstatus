from .base import Issue, IssueType


class BranchIssue(Issue):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, type_=IssueType.BRANCH, *args, **kwargs)
