"""
Pyffice CSV Data Handler
"""

import csv
from pathlib import Path
from typing import List, Dict, Any, Optional, Iterator


def read(filepath: str, delimiter: str = ",", encoding: str = "utf-8") -> List[Dict[str, Any]]:
    """Read CSV file and return list of dictionaries."""
    with open(filepath, "r", encoding=encoding, newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return list(reader)


def read_rows(filepath: str, delimiter: str = ",", encoding: str = "utf-8") -> List[List[str]]:
    """Read CSV file and return list of rows."""
    with open(filepath, "r", encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        return list(reader)


def write(filepath: str, data: List[Dict[str, Any]], delimiter: str = ",", encoding: str = "utf-8") -> None:
    """Write list of dictionaries to CSV file."""
    if not data:
        return
    fieldnames = list(data[0].keys())
    with open(filepath, "w", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)


def write_rows(filepath: str, rows: List[List[str]], delimiter: str = ",", encoding: str = "utf-8") -> None:
    """Write list of rows to CSV file."""
    with open(filepath, "w", encoding=encoding, newline="") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)


def append(filepath: str, row: Dict[str, Any], delimiter: str = ",", encoding: str = "utf-8") -> None:
    """Append single row to CSV file."""
    file_path = Path(filepath)
    write_header = not file_path.exists() or file_path.stat().st_size == 0
    
    with open(filepath, "a", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys(), delimiter=delimiter)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def append_row(filepath: str, row: List[str], delimiter: str = ",", encoding: str = "utf-8") -> None:
    """Append single row (list) to CSV file."""
    with open(filepath, "a", encoding=encoding, newline="") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(row)

class PyfficeCSV:
    """Handler for CSV file operations."""

    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize PyfficeCSV handler.

        Args:
            file_path: Optional path to CSV file
        """
        self.file_path = Path(file_path) if file_path else None
        self.headers: list[str] = []
        self._data: list[dict[str, Any]] = []

    def load(self, file_path: str) -> "PyfficeCSV":
        """
        Load CSV file from path.

        Args:
            file_path: Path to CSV file

        Returns:
            Self for chaining
        """
        self.file_path = Path(file_path)
        self._data = []

        with open(self.file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames or []
            self._data = list(reader)

        return self

    def save(self, file_path: Optional[str] = None) -> "PyfficeCSV":
        """
        Save data to CSV file.

        Args:
            file_path: Optional path, uses self.file_path if not provided

        Returns:
            Self for chaining
        """
        path = Path(file_path) if file_path else self.file_path
        if not path:
            raise ValueError("No file path specified")

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self._data)

        return self

    def read(self) -> list[dict[str, Any]]:
        """Return all rows as list of dictionaries."""
        return self._data.copy()

    def rows(self) -> Iterator[dict[str, Any]]:
        """Iterate over rows."""
        for row in self._data:
            yield row

    def append(self, row: dict[str, Any]) -> "PyfficeCSV":
        """
        Append a row to the data.

        Args:
            row: Dictionary of column:value pairs

        Returns:
            Self for chaining
        """
        if not self.headers:
            self.headers = list(row.keys())
        self._data.append(row)
        return self

    def extend(self, rows: list[dict[str, Any]]) -> "PyfficeCSV":
        """
        Extend data with multiple rows.

        Args:
            rows: List of row dictionaries

        Returns:
            Self for chaining
        """
        for row in rows:
            self.append(row)
        return self

    def filter(self, predicate: callable) -> list[dict[str, Any]]:
        """
        Filter rows using predicate function.

        Args:
            predicate: Function that takes row dict and returns bool

        Returns:
            Filtered list of rows
        """
        return [row for row in self._data if predicate(row)]

    def select(self, columns: list[str]) -> list[dict[str, Any]]:
        """
        Select specific columns from all rows.

        Args:
            columns: List of column names to select

        Returns:
            List of rows with only selected columns
        """
        return [{col: row.get(col) for col in columns} for row in self._data]

    def group_by(self, column: str) -> dict[str, list[dict[str, Any]]]:
        """
        Group rows by column value.

        Args:
            column: Column name to group by

        Returns:
            Dictionary mapping column values to row lists
        """
        result: dict[str, list[dict[str, Any]]] = {}
        for row in self._data:
            key = row.get(column, "")
            if key not in result:
                result[key] = []
            result[key].append(row)
        return result

    def count(self) -> int:
        """Return number of rows."""
        return len(self._data)

    def clear(self) -> "PyfficeCSV":
        """Clear all data."""
        self._data = []
        return self
