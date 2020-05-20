from abc import ABC, abstractmethod
from typing import Any, Dict, List

import click

from .table import SimpleTable
from .types import BoldGreenStr, BoldRedStr


SUMMARY_TYPES = {
    "repo": "",
    "branch": "",
    "both": ""
}

# Summary is a dict with keys that are repo names and values
# that are dicts with keys "branch" and "repo". "branch" values
# are dicts of branch name and list of error pairs. "repo" values
# are lists of errors.


class SummaryBase(ABC):
    COLUMN_TITLES = None
    COLUMN_WIDTHS = None
    TABLE_CLASS = SimpleTable

    def __init__(self, issues: Dict[str, Any]):
        self._raw_issues = issues
        self.rows = self._process_issues(issues)

    @abstractmethod
    def _process_issues(self, issues: Dict[str, Any]):
        pass

    def summarize(self) -> str:
        return self.TABLE_CLASS(self.rows, self.COLUMN_TITLES,
                                self.COLUMN_WIDTHS).as_str()


class BasicSummary(SummaryBase):
    COLUMN_TITLES = ["REPO", "STATUS"]
    COLUMN_WIDTHS = [60, 10]

    def _process_issues(self, issues: Dict[str, Any]):
        rows = []
        for k, v in issues.items():
            any_issues = bool(v['repo']) or any(v['branch'].values())
            result = BoldRedStr("NOT OK") if any_issues else BoldGreenStr("OK")
            rows.append([k, result])
        return rows


class RepoSummary(SummaryBase):
    COLUMN_TITLES = ["REPO", "ISSUES"]
    COLUMN_WIDTHS = [50, 25]

    def _process_issues(self, issues: Dict[str, Any]):
        rows = []
        for k, v in issues.items():
            issues = ", ".join([str(issue) for issue in v["repo"]])
            if not issues:
                issues = BoldGreenStr("OK")
            rows.append([k, issues])
        return rows
