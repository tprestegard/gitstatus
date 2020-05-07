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
    COLUMN_TITLES = None

    def __init__(self, issues: Dict[str, Any]):
        self.issues = issues

    @abstractmethod
    def _get_row(self, repo: str, issues: Dict[str, Any]) -> List[str]:
        pass

    def _calculate_col_widths(self) -> List[int]:
        rows = [self._get_row(k, v) for k, v in self.issues.items()]
        cols = list(map(list, zip(*rows)))
        col_widths = [max([len(item) for item in col]) for col in cols]
        col_widths = [
            max(min(cw, self.COLUMN_WIDTH[i]), len(self.COLUMN_TITLES[i]))
            for i, cw in enumerate(col_widths)
        ]
        return col_widths

    def _get_row_divider(self, col_widths: List[int], char = "-",
                         col_sep: str = "+") -> str:
        border_cols = [char * (col_widths[i] + 2) for i in
                       range(len(col_widths))]
        return col_sep + col_sep.join(border_cols) + col_sep
                         

    def _format_header(self, col_widths: List[int]) -> str:
        border = self._get_row_divider(col_widths, char="=")
        titles = self._format_row(self.COLUMN_TITLES, col_widths)
        return f"{border}\n{titles}\n{border}"

    def _pad_row(self, row: List[str], col_widths: List[int]) -> str:
        return [f"{col:<{col_widths[i]}}" for i, col in enumerate(row)]

    def _format_row(self, row: List[str], col_widths: List[int]) -> str:
        return "| " + " | ".join(self._pad_row(row, col_widths)) + " |"

    def _format_table(self):
        # Get rows
        rows = [self._get_row(k, v) for k, v in self.issues.items()]

        # Calculate column widths
        cols = list(map(list, zip(*rows)))
        col_widths = [max([len(item) for item in col]) for col in cols]
        col_widths = [min(cw, self.COLUMN_WIDTH[i]) for i, cw in 
                      enumerate(col_widths)]
        col_widths = self._calculate_col_widths()

        # Format header
        header = self._format_header(col_widths)

        # Format rows
        formatted_rows = [self._format_row(row, col_widths) for row in rows]

        # Get full table
        table = header + "\n" + \
            "\n".join(formatted_rows) + \
            "\n" + self._get_row_divider(col_widths, char="=")
            #f"\n{self._get_row_divider(col_widths)}\n".join(formatted_rows) + \
            #"\n" + self._get_row_divider(col_widths, char="=")

        return table


class BasicSummary(SummaryBase):
    COLUMN_WIDTH = [60, 10]
    COLUMN_TITLES = ["REPO", "STATUS"]

    def _get_row(self, repo: str, issues: Dict[str, Any]) -> List[str]:
        any_issues = bool(issues['repo']) or any(issues['branch'].values())
        return [repo, "NOT OK" if any_issues else "OK"]
        #status = click.style("NOT OK", fg="red") if any_issues \
        #    else click.style("OK", fg="green")
        #return [repo, status]

    def _format_row(self, row: List[str], col_widths: List[int]) -> str:
        padded_row = self._pad_row(row, col_widths)
        if row[1] == "NOT OK":
            padded_row[1] = padded_row[1].replace(
                "NOT OK", click.style("NOT OK", fg="red", bold=True)
            )
        elif row[1] == "OK":
            padded_row[1] = padded_row[1].replace(
                "OK", click.style("OK", fg="green", bold=True)
            )
        return "| " + " | ".join(padded_row) + " |"
