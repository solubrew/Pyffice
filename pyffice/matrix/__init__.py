"""
Pyffice Matrix Module - Spreadsheet operations
"""

import csv
from typing import List, Dict, Any, Optional, Union
from pathlib import Path


class Matrix:
    """Handle spreadsheet/matrix operations"""
    
    def __init__(self, data: Optional[List[List[Any]]] = None, rows: int = 0, cols: int = 0):
        if data:
            self.data = data
            self.rows = len(data)
            self.cols = len(data[0]) if data else 0
        else:
            self.rows = rows
            self.cols = cols
            self.data = [[None for _ in range(cols)] for _ in range(rows)]
    
    def get(self, row: int, col: int) -> Any:
        """Get cell value"""
        return self.data[row][col]
    
    def set(self, row: int, col: int, value: Any):
        """Set cell value"""
        self.data[row][col] = value
    
    def append(self, row: List[Any]):
        """Append a row"""
        if len(row) != self.cols:
            raise ValueError(f"Row length {len(row)} != cols {self.cols}")
        self.data.append(row)
        self.rows += 1
    
    def append_col(self, values: List[Any]):
        """Append a column"""
        if len(values) != self.rows:
            raise ValueError(f"Values length {len(values)} != rows {self.rows}")
        for i, val in enumerate(values):
            self.data[i].append(val)
        self.cols += 1
    
    def transpose(self) -> 'Matrix':
        """Transpose the matrix"""
        new_data = [[self.data[r][c] for r in range(self.rows)] for c in range(self.cols)]
        return Matrix(new_data)
    
    def merge_cells(self, start_row: int, start_col: int, end_row: int, end_col: int, value: Any):
        """Merge cells (top-left holds value)"""
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                if r == start_row and c == start_col:
                    self.data[r][c] = value
                else:
                    self.data[r][c] = None
    
    def to_csv(self, file_path: str, delimiter: str = ','):
        """Export to CSV"""
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerows(self.data)
    
    @classmethod
    def from_csv(cls, file_path: str, delimiter: str = ',') -> 'Matrix':
        """Import from CSV"""
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=delimiter)
            data = list(reader)
        return cls(data)
    
    def formula(self, cell_ref: str, formula: str):
        """Evaluate formula (basic support)"""
        pass  # Placeholder for formula engine


def create_matrix(rows: int, cols: int, fill: Any = None) -> Matrix:
    """Create a new matrix"""
    data = [[fill for _ in range(cols)] for _ in range(rows)]
    return Matrix(data)
