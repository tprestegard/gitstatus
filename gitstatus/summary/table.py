from textwrap import wrap
from typing import Any, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .types import StyledStr


def _transpose(array: List[List[Any]]) -> List[List[Any]]:
    return list(map(list, zip(*array)))


def _pad(cell: Union[str, "StyledStr"], width: int, align: str = "l") -> str:
    diff = width - len(cell)
    if diff < 0:
        # TODO
        raise Exception()

    # Get content
    content = cell.styled if hasattr(cell, "styled") else cell

    # Pad
    if align == "l":
        output = content + " " * diff
    else:
        # TODO
        raise NotImplementedError()

    return output


class DividerFormatter:
    def __init__(self, elem: str = "-", edge: str = "+", col_sep: str = "+"):
        self.elem = elem
        self.edge = edge
        self.col_sep = col_sep

    def format(self, col_widths: List[str]):
        cols = [self.elem * cl for cl in col_widths]
        return f"{self.edge}{self.col_sep.join(cols)}{self.edge}"


class RowFormatter:
    def __init__(self, edge: str = "|", col_sep: str = "|", padding: int = 1):
        self.edge = edge
        self.col_sep = col_sep
        self.padding = padding

    def format(self, columns: List[str]):
        padding = self.padding * " "
        col_sep = f"{padding}{self.col_sep}{padding}"
        return (
            f"{self.edge}{padding}{col_sep.join(columns)}{padding}{self.edge}"
        )


class Row:
    def __init__(self, cols: List[str]):
        # Assign attributes
        self._raw_cols = cols
        self._wrapped_cols = None
        self._is_wrapped = False

    def wrap(self, widths: List[int], force: bool = False):
        if self._is_wrapped and not force:
            # TODO
            raise ValueError("")

        # Wrap each column as necessary
        cols = []
        for i, col in enumerate(self._raw_cols):
            wrapped_col = wrap(col, widths[i])

            # Handle restyling
            if hasattr(col, "styled"):
                wrapped_col = [col.__class__(cell) for cell in wrapped_col]
            cols.append(wrapped_col)

        # Add blank rows where necessary
        max_rows = max([len(col) for col in cols])
        for col in cols:
            rows_to_add = max_rows - len(col)
            col.extend([""] * rows_to_add)

        # Transpose and assign
        self._wrapped_cols = _transpose(cols)
        self._is_wrapped = True

    def get_col_widths(self) -> List[int]:
        if self._is_wrapped:
            # Check all rows
            cols = _transpose(self._wrapped_cols)
            return [max([len(row) for row in col]) for col in cols]
        else:
            return [len(col) for col in self._raw_cols]

    def format(
        self, row_formatter: RowFormatter, widths: List[int] = None
    ) -> str:
        # Pad and style
        if widths:
            padded_rows = [
                [_pad(cell, widths[i]) for i, cell in enumerate(row)]
                for row in self._wrapped_cols
            ]
        else:
            padded_rows = self._wrapped_cols

        # Formatting
        return "\n".join([row_formatter.format(row) for row in padded_rows])
        # if self._is_wrapped:
        # else:
        #    return row_formatter.format(self._raw_cols)

    def as_str(self, formatter: RowFormatter) -> str:
        self._wrap()
        # TODO: after wrapping, we need to reevaluate how wide the columns need
        # to be
        padded_rows = [
            [f"{col:<{self.widths[i]}}" for i, col in enumerate(row)]
            for row in self.subrows
        ]
        self._str = "\n".join(
            [self.formatter.format(row) for row in padded_rows]
        )
        return self._str


class TableBase:
    def __init__(
        self,
        row_list: List[List[str]],
        column_titles: List[str],
        max_column_widths: List[int],
        row_formatter: RowFormatter,
        header_formatter: DividerFormatter,
        title: str = None,
        footer_formatter: DividerFormatter = None,
        row_divider_formatter: DividerFormatter = None,
    ):

        # Assign attributes
        self._raw_rows = row_list
        self._raw_titles = column_titles
        self.title = title
        self.max_widths = max_column_widths
        self.row_formatter = row_formatter
        self.header_formatter = header_formatter
        self.footer_formatter = footer_formatter
        self.divider_formatter = row_divider_formatter

        # Formatted attributes
        self.rows = None
        self.titles = None
        self._str = None

    def _calculate_column_widths(self, rows: List[Row]) -> List[int]:
        current_widths = [
            max(width)
            for width in _transpose([row.get_col_widths() for row in rows])
        ]

        # Widths to use
        return [
            min(cw, self.max_widths[i]) for i, cw in enumerate(current_widths)
        ]
        # Transpose
        # cols = _transpose(rows)

        # Current widths
        # current_widths = [max([len(item) for item in col]) for col in cols]

        # Widths to use
        # return [min(cw, self.max_widths[i]), for i, cw in
        #        enumerate(current_widths)]

    def as_str(self) -> str:
        if self._str:
            return self._str

        # Convert titles to a Row object
        self.titles = Row(self._raw_titles)

        # Convert rows to a list of Row objects
        self.rows = [Row(row) for row in self._raw_rows]

        # Combine things to simplify
        combined = [self.titles] + self.rows

        # Calculate column widths
        widths = self._calculate_column_widths(combined)

        # Wrap titles and rows
        for row in combined:
            row.wrap(widths)

        # Recalculate column widths - may have changed due to flexibility
        # in wrapping breakpoints
        widths = self._calculate_column_widths(combined)

        # Wrap again
        for row in combined:
            row.wrap(widths, force=True)

        # Pad and format titles
        titles_str = self.titles.format(self.row_formatter, widths)

        # Construct full header
        divider_widths = [w + 2 for w in widths]
        header_divider = self.header_formatter.format(divider_widths)
        header_str = header_divider + "\n" + titles_str + "\n" + header_divider

        # Add full table title, if provided
        # if self.title:
        #    table_title =

        # Pad and format rows
        rows_list = [
            row.format(self.row_formatter, widths) for row in self.rows
        ]

        # Join rows with divider (if provided)
        row_divider = "\n"
        if self.divider_formatter:
            row_divider += self.divider_formatter.format(divider_widths) + "\n"
        rows_str = row_divider.join(rows_list)

        # Combine header and rows and footer; assign to self._str
        self._str = (
            header_str
            + "\n"
            + rows_str
            + "\n"
            + self.footer_formatter.format(divider_widths)
        )
        return self._str


class SimpleTable(TableBase):
    def __init__(
        self,
        row_list: List[List[str]],
        column_titles: List[str],
        max_column_widths: List[int],
    ):
        row_formatter = RowFormatter()
        header_formatter = DividerFormatter(elem="=")
        row_divider_formatter = DividerFormatter()
        super().__init__(
            row_list,
            column_titles,
            max_column_widths,
            row_formatter,
            header_formatter,
            footer_formatter=row_divider_formatter,
            row_divider_formatter=row_divider_formatter,
        )
