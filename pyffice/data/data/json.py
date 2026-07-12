"""
Pyffice JSON Module

Provides JSON file handling capabilities for Pyffice.
"""

import json
from pathlib import Path
from typing import Any, Optional, Union


class PyfficeJSON:
    """Handler for JSON file operations."""

    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize PyfficeJSON handler.
        
        Args:
            file_path: Optional path to JSON file
        """
        self.file_path = Path(file_path) if file_path else None
        self._data: Any = None

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

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value by key (supports dot notation).
        
        Args:
            key: Key or path like "user.profile.name"
            default: Default value if key not found
            
        Returns:
            Value at key or default
        """
        if self._data is None:
            return default
            
        keys = key.split(".")
        value = self._data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
                
        return value

    def set(self, key: str, value: Any) -> "PyfficeJSON":
        """
        Set value by key (supports dot notation).
        
        Args:
            key: Key or path like "user.profile.name"
            value: Value to set
            
        Returns:
            Self for chaining
        """
        if self._data is None:
            self._data = {}
            
        keys = key.split(".")
        data = self._data
        
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
            
        data[keys[-1]] = value
        return self

    def keys(self) -> list[str]:
        """Return top-level keys."""
        if isinstance(self._data, dict):
            return list(self._data.keys())
        return []

    def values(self) -> list[Any]:
        """Return top-level values."""
        if isinstance(self._data, dict):
            return list(self._data.values())
        return []

    def items(self) -> list[tuple[str, Any]]:
        """Return top-level key-value pairs."""
        if isinstance(self._data, dict):
            return list(self._data.items())
        return []

    def update(self, data: Union[dict, "PyfficeJSON"]) -> "PyfficeJSON":
        """
        Update data with dictionary or PyfficeJSON object.
        
        Args:
            data: Dictionary or PyfficeJSON to merge
            
        Returns:
            Self for chaining
        """
        if isinstance(data, PyfficeJSON):
            data = data._data
            
        if isinstance(self._data, dict) and isinstance(data, dict):
            self._data.update(data)
        else:
            self._data = data
            
        return self

    def merge(self, other: "PyfficeJSON") -> "PyfficeJSON":
        """
        Deep merge another PyfficeJSON into this one.
        
        Args:
            other: PyfficeJSON to merge
            
        Returns:
            Self for chaining
        """
        self._data = self._deep_merge(self._data, other._data)
        return self

    def _deep_merge(self, base: Any, update: Any) -> Any:
        """Deep merge helper."""
        if isinstance(base, dict) and isinstance(update, dict):
            result = base.copy()
            for key, value in update.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        return update

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

    @staticmethod
    def from_dict(data: dict) -> "PyfficeJSON":
        """
        Create PyfficeJSON from dictionary.
        
        Args:
            data: Dictionary data
            
        Returns:
            New PyfficeJSON instance
        """
        obj = PyfficeJSON()
        obj._data = data
        return obj

    def clear(self) -> "PyfficeJSON":
        """Clear all data."""
        self._data = None
        return self

    @property
    def data(self) -> Any:
        """Access raw data."""
        return self._data
