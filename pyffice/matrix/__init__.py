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
        """Evaluate formula (basic support for common formulas)
        
        Supported formulas:
        - SUM(A1:B2) - sum range
        - AVERAGE(A1:B2) - average range  
        - MAX(A1:B2) - max of range
        - MIN(A1:B2) - min of range
        - COUNT(A1:B2) - count numeric cells
        - Basic arithmetic: =A1+B2, =A1*2, etc.
        
        Args:
            cell_ref: The cell to store result (e.g., 'A1')
            formula: Formula string (e.g., '=SUM(A1:A10)')
        """
        import re
        
        def parse_cell(ref: str) -> tuple:
            """Parse cell reference to row, col"""
            match = re.match(r'([A-Z]+)(\d+)', ref.upper())
            if not match:
                raise ValueError(f"Invalid cell reference: {ref}")
            col = ord(match.group(1)) - ord('A')
            row = int(match.group(2)) - 1
            return row, col
        
        def get_range(ref: str) -> list:
            """Parse range like A1:B10"""
            start, end = ref.split(':')
            r1, c1 = parse_cell(start)
            r2, c2 = parse_cell(end)
            values = []
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    if r < self.rows and c < self.cols:
                        val = self.data[r][c]
                        if val is not None:
                            try:
                                values.append(float(val))
                            except (ValueError, TypeError):
                                pass
            return values
        
        # Remove = prefix if present
        formula = formula.lstrip('=')
        
        # SUM
        match = re.match(r'SUM\(([A-Z]+\d+):([A-Z]+\d+)\)', formula, re.IGNORECASE)
        if match:
            values = get_range(f"{match.group(1)}:{match.group(2)}")
            row, col = parse_cell(cell_ref)
            self.data[row][col] = sum(values)
            return
        
        # AVERAGE
        match = re.match(r'AVERAGE\(([A-Z]+\d+):([A-Z]+\d+)\)', formula, re.IGNORECASE)
        if match:
            values = get_range(f"{match.group(1)}:{match.group(2)}")
            row, col = parse_cell(cell_ref)
            self.data[row][col] = sum(values) / len(values) if values else 0
            return
        
        # MAX
        match = re.match(r'MAX\(([A-Z]+\d+):([A-Z]+\d+)\)', formula, re.IGNORECASE)
        if match:
            values = get_range(f"{match.group(1)}:{match.group(2)}")
            row, col = parse_cell(cell_ref)
            self.data[row][col] = max(values) if values else 0
            return
        
        # MIN
        match = re.match(r'MIN\(([A-Z]+\d+):([A-Z]+\d+)\)', formula, re.IGNORECASE)
        if match:
            values = get_range(f"{match.group(1)}:{match.group(2)}")
            row, col = parse_cell(cell_ref)
            self.data[row][col] = min(values) if values else 0
            return
        
        # COUNT
        match = re.match(r'COUNT\(([A-Z]+\d+):([A-Z]+\d+)\)', formula, re.IGNORECASE)
        if match:
            values = get_range(f"{match.group(1)}:{match.group(2)}")
            row, col = parse_cell(cell_ref)
            self.data[row][col] = len(values)
            return
        
        # Basic arithmetic: A1+B2, A1*2, etc.
        match = re.match(r'([A-Z]+\d+)\s*([+\-*/])\s*([A-Z]+\d+|\d+\.?\d*)', formula, re.IGNORECASE)
        if match:
            ref1, op, ref2 = match.groups()
            r1, c1 = parse_cell(ref1)
            val1 = float(self.data[r1][c1]) if self.data[r1][c1] else 0
            
            try:
                val2 = float(ref2)
            except ValueError:
                r2, c2 = parse_cell(ref2)
                val2 = float(self.data[r2][c2]) if self.data[r2][c2] else 0
            
            row, col = parse_cell(cell_ref)
            if op == '+':
                self.data[row][col] = val1 + val2
            elif op == '-':
                self.data[row][col] = val1 - val2
            elif op == '*':
                self.data[row][col] = val1 * val2
            elif op == '/':
                self.data[row][col] = val1 / val2 if val2 != 0 else 0
            return
        
        raise ValueError(f"Unsupported formula: {formula}")


def create_matrix(rows: int, cols: int, fill: Any = None) -> Matrix:
    """Create a new matrix"""
    data = [[fill for _ in range(cols)] for _ in range(rows)]
    return Matrix(data)
