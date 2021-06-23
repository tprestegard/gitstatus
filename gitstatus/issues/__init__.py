import enum

from .base import Issue  # noqa: F401
from .branch import BranchIssue as BRANCH
from .repo import RepoIssue as REPO


class BranchIssue(enum.Enum):
    NO_REMOTE = BRANCH("NO_REMOTE")
    AHEAD_OF_REMOTE = BRANCH("AHEAD_OF_REMOTE")
    BEHIND_REMOTE = BRANCH("BEHIND_REMOTE")
    OUT_OF_SYNC_WITH_REMOTE = BRANCH("OUT_OF_SYNC_WITH_REMOTE")
    INVALID_STATUS = BRANCH("INVALID_STATUS")


class RepoIssue(enum.Enum):
    NO_REMOTE = REPO("NO_REMOTE")
    NOT_ON_BRANCH = REPO("NOT_ON_BRANCH")
    UNCOMMITTED_CHANGES = REPO("UNCOMMITTED_CHANGES")
    UNTRACKED_FILES = REPO("UNTRACKED_FILES")
    STASHED_CHANGES = REPO("STASHED_CHANGES")
