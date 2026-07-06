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
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
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
        matrix._data = [[float(cell) if cell is not None else 0.0 
                        for cell in row] for row in data]
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
            col = col * 26 + (ord(char) - ord('A') + 1)
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
