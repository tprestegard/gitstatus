from abc import ABC, abstractmethod
from typing import Any, Dict, List

import click


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
    COLUMN_WIDTHS = None

    def __init__(self, issues: Dict[str, Any]):
        self.issues = issues

    @abstractmethod
    def _get_row(self, repo: str, issues: Dict[str, Any]) -> List[str]:
        pass

    @abstractmethod
    def _get_header(self) -> List[str]:
        pass

    def _calculate_col_widths(self):
        rows = [self._get_row(k, v) for k, v in self.issues.items()]
        cols = list(map(list, zip(*rows)))
        col_widths = [max([len(item) for item in col]) for col in cols]
        col_widths = [min(cw, self.COLUMN_WIDTH[i]) for i, cw in 
                      enumerate(col_widths)]
        return col_widths

    def _format_header(self, table_width: str, col_widths: List[str]) -> str:
        border = "=" * table_width
        titles = ""
        return f"{border}\n{titles}\n{border}"

    def _format_row(self, row: List[str]) -> str:
        pass

    def _format_table(self):
        # Get rows
        rows = [self._get_row(k, v) for k, v in self.issues.items()]

        # Calculate column widths
        cols = list(map(list, zip(*rows)))
        col_widths = [max([len(item) for item in col]) for col in cols]
        col_widths = [min(cw, self.COLUMN_WIDTH[i]) for i, cw in 
                      enumerate(col_widths)]
        col_widths = self._calculate_col_widths()
        table_width = sum(col_widths) + 4 + 3*len(col_widths)
        import ipdb; ipdb.set_trace()

        # Format header


        # Format rows
        #formatted_rows = 



class BasicSummary(SummaryBase):
    COLUMN_WIDTH = [60, 10]
    def _get_header(self) -> List[str]:
        return ["REPO", "STATUS"]

    def _get_row(self, repo: str, issues: Dict[str, Any]) -> List[str]:
        any_issues = bool(issues['repo']) or any(issues['branch'].values())
        return [repo, "NOT OK" if any_issues else "OK"]
        #status = click.style("NOT OK", fg="red") if any_issues \
        #    else click.style("OK", fg="green")
        #return [repo, status]
