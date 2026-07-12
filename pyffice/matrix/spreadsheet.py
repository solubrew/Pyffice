# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||
try:
    from pycel.excelformula import ExcelFormula
    from pycel import ExcelCompiler
except ImportError:

    # TODO need replace with functional system
    def formula_builder():
        class GenericClass(object):
            pass

        return GenericClass

    ExcelFormula = formula_builder()
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
    """Pyffice SpreadSheet is a single page spreadsheet that can be included in a Pyffice Matrix to create a workbook"""

    VERSION = "0.0.1.0.1.0"

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
        """"""
        if address in self.cells:
            self.set_cell(address, cfg["value"], cfg["format"], cfg["formula"])
        self.add_change("cells", None, cfg, "assign", {"address": address})
        self.cells[address] = PyfficeCell(cfg)
        return self

    def convert_column(self, column, syntax="arabic"):
        """"""
        if syntax == "arabic":
            column = calcArabicNumerals(column)
        elif syntax == "roman":
            logma.info(f"Convert Column {column}")
            column = calcExtendedRomanNumerals(column)
        else:
            raise Exception(f"Unknown Syntax {syntax}")
        return column

    def evaluate(self, address):
        """"""
        self.cells[address] = self.cells[address].evaluate()
        return self

    def get_cell(self, address):
        """"""
        return self.cells.get(address, None)

    def get_columns(self, count=None):
        """"""
        columns = []
        for column in range(1, count + 1):
            columns.append(self.convert_column(column))
        return columns

    def get_data(self, filters=None, return_format="table"):
        """return a dictionary or table of data"""
        data = self.data
        if return_format == "table":
            return data
        elif return_format == "dict":
            return self.cells
        else:
            raise Exception(f"Unknown Return Format {return_format}")

    def get_end_column(self, plus=0, minus=0):
        """"""
        end_column = self.convert_column(self.end_column, "arabic")
        return self.convert_column(end_column + plus - minus, "roman")

    def get_end_row(self, plus=0, minus=0):
        """"""
        return self.end_row + plus - minus

    def get_formula(self, address):
        """"""
        return self.cells[address].get_formula()

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.cells = {}
        self.set_name(document.get("name", None))
        self.set_data(document.get("data", None))
        self.set_size(document.get("size", None))
        return self

    def set_cell(self, address, value, format=None, formula=None):
        """"""
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
        """"""
        if widths is None:
            widths = {}
        if labels != self.column_labels:
            self.add_change("column_labels", self.column_labels, labels)
        self.column_labels = {x: widths.get(x, 30) for x in labels}
        return self

    def set_column_width(self, column, width):
        """"""
        if column not in self.column_labels:
            raise Exception(f"Column {column} not found")
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
        """"""
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
        """"""
        return self

    def set_row_labels(self, labels=None):
        """"""
        if labels != self.row_labels:
            self.add_change("row_labels", self.row_labels, labels)
        self.row_labels = labels
        return self

    def set_size(self, size):
        """"""
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
        """"""
        doc = super().to_dict()
        doc["document"]["cells"] = {x: cell.to_dict() for x, cell in self.cells.items()}
        doc["document"]["objects"] = {
            "tables": [x.to_dict() for x in self.tables],
            "charts": [x.to_dict() for x in self.charts],
            "images": [x.to_dict() for x in self.images],
        }
        self.document["document"] = {
            "data": self.data,
            "objects": {
                "tables": self.tables,
                "charts": self.charts,
                "images": self.images,
                "shapes": self.shapes,
            },
        }
        self.load_document(self.document["document"])
        return doc

    def _sanitize_sheet_name(self, name):
        """"""
        subs = ["[", "]", "/"]
        for sub in subs:
            if sub in name:
                name = name.replace(sub, "")
        return name


"""Pyffice Spreadsheet Module.

Provides spreadsheet handling, matrix operations, and numeral conversions.
"""

from dataclasses import dataclass, field
from typing import Any, Iterator


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


@dataclass
class PyfficeMatrix:
    """Matrix operations handler.

    Provides basic matrix operations for spreadsheet calculations.
    """

    rows: int = 0
    cols: int = 0
    _data: list[list[float]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize matrix with zeros if dimensions specified."""
        if self.rows > 0 and self.cols > 0 and not self._data:
            self._data = [[0.0] * self.cols for _ in range(self.rows)]

    @classmethod
    def from_list(cls, data: list[list[Any]]) -> "PyfficeMatrix":
        """Create matrix from 2D list."""
        if not data:
            return cls()
        rows = len(data)
        cols = len(data[0]) if data[0] else 0
        matrix = cls(rows=rows, cols=cols)
        matrix._data = [[float(cell) if cell is not None else 0.0 for cell in row] for row in data]
        return matrix

    @classmethod
    def identity(cls, size: int) -> "PyfficeMatrix":
        """Create identity matrix."""
        matrix = cls(rows=size, cols=size)
        for i in range(size):
            matrix._data[i][i] = 1.0
        return matrix

    def get(self, row: int, col: int) -> float:
        """Get cell value."""
        return self._data[row][col]

    def set(self, row: int, col: int, value: float) -> None:
        """Set cell value."""
        self._data[row][col] = value

    def add(self, other: "PyfficeMatrix") -> "PyfficeMatrix":
        """Add two matrices."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match")
        result = PyfficeMatrix(rows=self.rows, cols=self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result._data[i][j] = self._data[i][j] + other._data[i][j]
        return result

    def multiply(self, other: "PyfficeMatrix") -> "PyfficeMatrix":
        """Multiply two matrices."""
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions incompatible for multiplication")
        result = PyfficeMatrix(rows=self.rows, cols=other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                total = 0.0
                for k in range(self.cols):
                    total += self._data[i][k] * other._data[k][j]
                result._data[i][j] = total
        return result

    def transpose(self) -> "PyfficeMatrix":
        """Return transpose of matrix."""
        result = PyfficeMatrix(rows=self.cols, cols=self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                result._data[j][i] = self._data[i][j]
        return result

    def to_list(self) -> list[list[float]]:
        """Return matrix as 2D list."""
        return [row[:] for row in self._data]


@dataclass
class PyfficeSpreadSheet:
    """Spreadsheet handler for Pyffice.

    Provides spreadsheet-like operations with cells and formulas.
    """

    name: str = "Untitled"
    rows: int = 100
    cols: int = 26
    _cells: dict[tuple[int, int], Any] = field(default_factory=dict)

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

    def to_dict(self) -> dict[str, Any]:
        """Export spreadsheet as dictionary."""
        result = {}
        for (row, col), value in self._cells.items():
            ref = self.cell_ref(row, col)
            result[ref] = value
        return result


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
