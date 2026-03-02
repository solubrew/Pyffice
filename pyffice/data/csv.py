"""
Pyffice CSV Module - Read/Write CSV files
"""

import csv
from typing import List, Dict, Any, Optional
from pathlib import Path


class PyfficeCSV:
    """Handle CSV file operations"""
    
    SUPPORTED_EXTENSIONS = ['.csv', '.tsv', '.txt']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self, delimiter: str = ',', skip_rows: int = 0) -> List[Dict[str, Any]]:
        """Read CSV as list of dictionaries"""
        rows = []
        with open(self.file_path, 'r', encoding=self.encoding, newline='') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for _ in range(skip_rows):
                next(reader)
            for row in reader:
                rows.append(dict(row))
        return rows
    
    def read_raw(self, delimiter: str = ',') -> List[List[str]]:
        """Read CSV as raw rows"""
        rows = []
        with open(self.file_path, 'r', encoding=self.encoding, newline='') as f:
            reader = csv.reader(f, delimiter=delimiter)
            for row in reader:
                rows.append(row)
        return rows
    
    def write(self, data: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None):
        """Write list of dictionaries to CSV"""
        if not data:
            return
        fieldnames = fieldnames or list(data[0].keys())
        with open(self.file_path, 'w', encoding=self.encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            writer.writerows(data)
    
    def write_raw(self, data: List[List[str]], delimiter: str = ','):
        """Write raw rows to CSV"""
        with open(self.file_path, 'w', encoding=self.encoding, newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerows(data)


def read_csv(file_path: str, **kwargs) -> List[Dict[str, Any]]:
    """Convenience function to read CSV"""
    return PyfficeCSV(file_path).read(**kwargs)


def write_csv(file_path: str, data: List[Dict[str, Any]], **kwargs):
    """Convenience function to write CSV"""
    PyfficeCSV(file_path).write(data, **kwargs)
