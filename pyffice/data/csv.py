"""
Pyffice CSV Data Handler
"""

import csv
from pathlib import Path
from typing import List, Dict, Any, Optional


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
