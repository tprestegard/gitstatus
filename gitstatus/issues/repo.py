from .base import Issue, IssueType


class RepoIssue(Issue):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, type_=IssueType.REPO, *args, **kwargs)
