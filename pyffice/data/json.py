"""Pyffice JSON Module

Provides JSON file handling capabilities for Pyffice.
Uses PyfficeDataMixin for common operations.
"""

import json
from pathlib import Path
from typing import Any, Optional

from .base import PyfficeDataMixin


class PyfficeJSON(PyfficeDataMixin):
    """Handler for JSON file operations."""

    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize PyfficeJSON handler.
        
        Args:
            file_path: Optional path to JSON file
        """
        super().__init__()
        self.file_path = Path(file_path) if file_path else None

    def load(self, file_path: Optional[str] = None) -> "PyfficeJSON":
        """
        Load JSON from file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Self for chaining
        """
        path = Path(file_path) if file_path else self.file_path
        if not path:
            raise ValueError("No file path specified")
            
        with open(path, "r", encoding="utf-8") as f:
            self._data = json.load(f)
            
        return self

    def save(self, file_path: Optional[str] = None, indent: int = 2) -> "PyfficeJSON":
        """
        Save data to JSON file.
        
        Args:
            file_path: Optional path, uses self.file_path if not provided
            indent: JSON indentation level
            
        Returns:
            Self for chaining
        """
        path = Path(file_path) if file_path else self.file_path
        if not path:
            raise ValueError("No file path specified")
            
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=indent, ensure_ascii=False)
            
        return self

    def to_string(self, indent: int = 2) -> str:
        """
        Return JSON as formatted string.
        
        Args:
            indent: JSON indentation level
            
        Returns:
            Formatted JSON string
        """
        return json.dumps(self._data, indent=indent, ensure_ascii=False)

    @staticmethod
    def from_string(json_string: str) -> "PyfficeJSON":
        """
        Create PyfficeJSON from string.
        
        Args:
            json_string: JSON formatted string
            
        Returns:
            New PyfficeJSON instance
        """
        obj = PyfficeJSON()
        obj._data = json.loads(json_string)
        return obj
