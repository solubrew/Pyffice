# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        Pyffice Spreadsheet Module.

Provides spreadsheet handling, matrix operations, and numeral conversions.
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from dataclasses import dataclass, field
from typing import Any, Iterator

# ======================================3rd Party Library Modules======================================================||
# T-NEW-054 (Option B): pycel removed. The formulas module
# provides its own protocol-based execution; this module no
# longer needs an Excel formula parser.

from pandas import read_csv, read_excel, DataFrame

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument
from pyffice.items.cells import PyfficeCell
from thingery.numbers.numerals import calcExtendedRomanNumerals, calcArabicNumerals


# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "spreadsheet.yaml")


class PyfficeSpreadSheet(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """Pyffice SpreadSheet is a single page spreadsheet that can be included in a Pyffice Matrix to create a workbook"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeSpreadSheet").override(cfg))
        self.cells = None
        self.charts = None  # a Dictionary of Chart objects
        self.column_labels = None
        self.data = None  # a DataFrame table
        self.images = None
        self.num_cols = None
        self.num_rows = None
        self.start_column = None
        self.start_row = None
        self.end_column = None
        self.end_row = None
        self.shapes = None
        self.tables = None

    def add_cell(self, address, cfg):
        """Add a cell.
        
        Args:
            address: Parameter.
            cfg: Parameter.
        
        Returns:
            Self for chaining.
        """
        if address in self.cells:
            self.set_cell(address, cfg["value"], cfg["format"], cfg["formula"])
        self.add_change("cells", None, cfg, "assign", {"address": address})
        self.cells[address] = PyfficeCell(cfg)
        return self

    def convert_column(self, column, syntax="arabic"):
        """Convert column.
        
        Args:
            column: Parameter.
            syntax: Parameter.
        
        Returns:
            Self for chaining.
        """
        from pyffice.pyffice import UnknownSyntaxError
        if syntax == "arabic":
            column = calcArabicNumerals(column)
        elif syntax == "roman":
            logma.info(f"Convert Column {column}")
            column = calcExtendedRomanNumerals(column)
        else:
            raise UnknownSyntaxError(f"Unknown Syntax {syntax}")
        return column

    def evaluate(self, address):
        """Evaluate.
        
        Args:
            address: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.cells[address] = self.cells[address].evaluate()
        return self

    def get_cell(self, address):
        """Return the cell.
        
        Args:
            address: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self.cells.get(address, None)

    def get_columns(self, count=None):
        """Return the columns.
        
        Args:
            count: Parameter.
        
        Returns:
            Self for chaining.
        """
        if count is None:
            count = 0
        columns = []
        for column in range(1, count + 1):
            columns.append(self.convert_column(column))
        return columns

    def get_data(self, filters=None, return_format="table"):
        """return a dictionary or table of data"""
        from pyffice.pyffice import UnknownReturnFormatError
        data = self.data
        if return_format == "table":
            return data
        elif return_format == "dict":
            return self.cells
        else:
            raise UnknownReturnFormatError(f"Unknown Return Format {return_format}")

    def get_end_column(self, plus=0, minus=0):
        """Return the end column.
        
        Args:
            plus: Parameter.
            minus: Parameter.
        
        Returns:
            Self for chaining.
        """
        end_column = self.convert_column(self.end_column, "arabic")
        return self.convert_column(end_column + plus - minus, "roman")

    def get_end_row(self, plus=0, minus=0):
        """Return the end row.
        
        Args:
            plus: Parameter.
            minus: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self.end_row + plus - minus

    def get_formula(self, address):
        """Return the formula.
        
        Args:
            address: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self.cells[address].get_formula()

    def get_rows(self):
        """Group cells by row index and return a list of row dicts.

        Each row dict maps column-letter to the cell at that
        position. Cells without a parseable 'I|<n>' address are
        skipped. Empty self.cells returns an empty list.
        """
        if not self.cells:
            return []
        rows = {}
        for address, cell in self.cells.items():
            if not isinstance(address, str) or "|" not in address:
                continue
            col, _, row_str = address.partition("|")
            try:
                row_idx = int(row_str)
            except ValueError:
                continue
            rows.setdefault(row_idx, {})[col] = cell
        return [{"row": idx, "cells": cells}
                for idx, cells in sorted(rows.items())]

    def load_document(self, document=None):
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_name(document.get("name", None))
        self.set_data(document.get("data", None))
        self.set_size(document.get("size", None))
        return self

    def set_cell(self, address, value, format=None, formula=None):
        """Set the cell.
        
        Args:
            address: Parameter.
            value: Parameter.
            format: Parameter.
            formula: Parameter.
        
        Returns:
            Self for chaining.
        """
        # T-NEW-058 follow-up: initialize self.cells on first use
        # (was previously assumed non-None, breaking get_cell /
        # get_rows on fresh instances).
        if self.cells is None:
            self.cells = {}
        if address not in self.cells:
            column = address.split("|")[0]
            if self.convert_column(column, "arabic") > self.end_column:
                self.end_column = self.convert_column(column, "arabic")
            row = address.split("|")[1]
            if int(row) > self.end_row:
                self.end_row = int(row)
            self.set_size([self.end_row, self.end_column])
        cfg = {"value": value, "format": format, "formula": formula}
        cell = PyfficeCell(cfg)
        if cell != self.cells.get(address, None):
            self.add_change("cells", cell, self.cells.get(address, None), "assign", address)
        self.cells[address] = cell
        return self

    def set_column_labels(self, labels=None, widths=None):
        """Set the column labels.
        
        Args:
            labels: Parameter.
            widths: Parameter.
        
        Returns:
            Self for chaining.
        """
        if widths is None:
            widths = {}
        if labels != self.column_labels:
            self.add_change("column_labels", self.column_labels, labels)
        self.column_labels = {x: widths.get(x, 30) for x in labels}
        return self

    def set_column_width(self, column, width):
        """Set the column width.
        
        Args:
            column: Parameter.
            width: Parameter.
        
        Returns:
            Self for chaining.
        """
        from pyffice.pyffice import ColumnNotFoundError
        if column not in self.column_labels:
            raise ColumnNotFoundError(f"Column {column} not found")
        if int(width) != self.column_labels[column]:
            self.add_change(
                "column_labels",
                self.column_labels[column],
                int(width),
                "assign",
                {"key": column},
            )
        self.column_labels[column] = int(width)
        return self

    def set_data(self, data):
        """Set the data.
        
        Args:
            data: Parameter.
        
        Returns:
            Self for chaining.
        """
        if data is None:
            data = {}
        row = 0
        rows = []
        data_ = []
        self.cells = data
        for address, value in data.items():
            if row != address.split("|")[1]:
                row = address.split("|")[1]
                if len(data) > 0 and len(rows) < len(data[0]):
                    rows += [None] * (len(data[0]) - len(rows))
                data_.append(rows)
                rows = [value]
            else:
                rows.append(value)
        self.data = DataFrame(data_, columns=self.get_columns())
        return self

    def set_objects(self, objects):
        """Set objects."""
        _p = True  # placeholder
        return self

    def set_row_labels(self, labels=None):
        """Set the row labels.
        
        Args:
            labels: Parameter.
        
        Returns:
            Self for chaining.
        """
        if labels != self.row_labels:
            self.add_change("row_labels", self.row_labels, labels)
        self.row_labels = labels
        return self

    def set_size(self, size):
        """Set the size.
        
        Args:
            size: Parameter.
        
        Returns:
            Self for chaining.
        """
        if size is None:
            size = (50, 20)
        num_rows = size[0]
        num_cols = size[1]
        if self.data is not None and len(self.data) > 0:
            self.num_rows = len(self.data) if len(self.data) > num_rows else num_rows
            self.num_cols = len(self.data[0]) if len(self.data[0]) > num_cols else num_cols
            self.end_row = self.get_end_row(plus=self.num_rows)
            self.end_column = self.get_end_column(plus=self.num_cols)
        else:
            self.num_rows = num_rows
            self.num_cols = num_cols
            row = [None] * num_cols
            self.data = DataFrame([row] * num_rows, columns=self.get_columns(count=self.num_cols))
            self.end_row = self.get_end_row(plus=num_rows)
            self.end_column = self.get_end_column(plus=num_cols)
        return self

    def to_dict(self):
        """Convert this document to dict.
        
        Returns:
            Self for chaining.
        """
        doc = super().to_dict()
        doc["data"]["document_type"] = "sheet"
        self._ensure_init_state({
            "cells": {},
            "tables": [],
            "charts": [],
            "images": [],
            "shapes": [],
        })
        doc["data"]["cells"] = {x: cell.to_dict() for x, cell in self.cells.items()}
        doc["data"]["objects"] = {
            "tables": [x.to_dict() for x in self.tables],
            "charts": [x.to_dict() for x in self.charts],
            "images": [x.to_dict() for x in self.images],
            "shapes": [x.to_dict() for x in self.shapes],
        }
        columns = self.get_columns()
        doc["data"]["columns"] = {"ranges": [], "counts": len(columns)}
        rows = self.get_rows()
        doc["data"]["rows"] = {"ranges": [], "counts": len(rows)}
        return self._canonicalize(doc)

    def _sanitize_sheet_name(self, name):
        """"""
        subs = ["[", "]", "/"]
        for sub in subs:
            if sub in name:
                name = name.replace(sub, "")
        return name

    def cell_ref(self, row: int, col: int) -> str:
        """Convert row/col to cell reference (e.g., A1)."""
        col_letter = chr(65 + col) if col < 26 else f"{chr(65 + col // 26 - 1)}{chr(65 + col % 26)}"
        return f"{col_letter}{row + 1}"

    def parse_cell_ref(self, ref: str) -> tuple[int, int]:
        """Parse cell reference to row/col."""
        col_str = ""
        row_str = ""
        for char in ref:
            if char.isalpha():
                col_str += char
            else:
                row_str += char

        col = 0
        for char in col_str.upper():
            col = col * 26 + (ord(char) - ord("A") + 1)
        col -= 1
        row = int(row_str) - 1
        return (row, col)

    def get(self, cell_ref: str) -> Any:
        """Get cell value by reference."""
        row, col = self.parse_cell_ref(cell_ref)
        return self._cells.get((row, col))

    def set(self, cell_ref: str, value: Any) -> None:
        """Set cell value by reference."""
        row, col = self.parse_cell_ref(cell_ref)
        self._cells[(row, col)] = value

    def sum_range(self, start_ref: str, end_ref: str) -> float:
        """Sum a range of cells."""
        start_row, start_col = self.parse_cell_ref(start_ref)
        end_row, end_col = self.parse_cell_ref(end_ref)
        total = 0.0
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                value = self._cells.get((row, col))
                if isinstance(value, (int, float)):
                    total += value
        return total

    def avg_range(self, start_ref: str, end_ref: str) -> float:
        """Average a range of cells."""
        start_row, start_col = self.parse_cell_ref(start_ref)
        end_row, end_col = self.parse_cell_ref(end_ref)
        total = 0.0
        count = 0
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                value = self._cells.get((row, col))
                if isinstance(value, (int, float)):
                    total += value
                    count += 1
        return total / count if count > 0 else 0.0

    def clear(self) -> None:
        """Clear all cells."""
        self._cells.clear()


def calcArabicNumerals(roman: str) -> int:
    """Convert Roman numerals to Arabic (integer).

    Args:
        roman: Roman numeral string (e.g., "XIV")

    Returns:
        Integer value
    """
    roman_values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    result = 0
    prev = 0
    for char in reversed(roman.upper()):
        if char not in roman_values:
            return 0
        curr = roman_values[char]
        if curr < prev:
            result -= curr
        else:
            result += curr
        prev = curr
    return result


def calcExtendedRomanNumerals(arabic: int) -> str:
    """Convert Arabic number to extended Roman numerals.

    Args:
        arabic: Integer value (supports numbers > 3999)

    Returns:
        Extended Roman numeral string
    """
    if arabic <= 0:
        return ""

    # Extended Roman numerals for large numbers
    extended = [
        (1000000, "M̅"),
        (900000, "C̅M̅"),
        (500000, "D̅"),
        (400000, "C̅D̅"),
        (100000, "C̅"),
        (90000, "X̅C̅"),
        (50000, "L̅"),
        (40000, "X̅L̅"),
        (10000, "X̅"),
        (9000, "MX"),
        (5000, "V̅"),
        (4000, "MV"),
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    result = ""
    for value, numeral in extended:
        while arabic >= value:
            result += numeral
            arabic -= value
    return result


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
