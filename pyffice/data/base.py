"""Pyffice Data Base Module

Provides shared functionality for data format handlers (JSON, YAML, TOML, etc.).
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class PyfficeDataBase(ABC):
    """Abstract base class for data format handlers.
    
    Provides common functionality like dot-notation access, deep merging,
    and dict conversion that all data format handlers share.
    """

    def __init__(self):
        """Initialize base data handler."""
        self._data: Any = None

    @property
    @abstractmethod
    def data(self) -> Any:
        """Get raw data. Must be implemented by subclass."""
        raise NotImplementedError("Subclass must implement data property")

    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key with dot notation support.
        
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

    def set(self, key: str, value: Any) -> "PyfficeDataBase":
        """Set value by key with dot notation support.
        
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

    def merge(self, other: "PyfficeDataBase") -> "PyfficeDataBase":
        """Deep merge another data handler into this one.
        
        Args:
            other: Data handler to merge
            
        Returns:
            Self for chaining
        """
        other_data = other._data if hasattr(other, '_data') else other
        self._data = self._deep_merge(self._data, other_data)
        return self

    def _deep_merge(self, base: Any, update: Any) -> Any:
        """Deep merge helper.
        
        Args:
            base: Base dictionary
            update: Dictionary to merge in
            
        Returns:
            Merged dictionary
        """
        if isinstance(base, dict) and isinstance(update, dict):
            result = base.copy()
            for key, value in update.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        return update

    def keys(self) -> list[str]:
        """Return top-level keys.
        
        Returns:
            List of keys at top level
        """
        if isinstance(self._data, dict):
            return list(self._data.keys())
        return []

    def values(self) -> list[Any]:
        """Return top-level values.
        
        Returns:
            List of values at top level
        """
        if isinstance(self._data, dict):
            return list(self._data.values())
        return []

    def items(self) -> list[tuple[str, Any]]:
        """Return top-level key-value pairs.
        
        Returns:
            List of (key, value) tuples at top level
        """
        if isinstance(self._data, dict):
            return list(self._data.items())
        return []

    def update(self, data: dict) -> "PyfficeDataBase":
        """Update data with dictionary.
        
        Args:
            data: Dictionary to merge
            
        Returns:
            Self for chaining
        """
        if isinstance(self._data, dict) and isinstance(data, dict):
            self._data.update(data)
        else:
            self._data = data
        return self

    def clear(self) -> "PyfficeDataBase":
        """Clear all data.
        
        Returns:
            Self for chaining
        """
        self._data = None
        return self

    @staticmethod
    @abstractmethod
    def from_dict(data: dict) -> "PyfficeDataBase":
        """Create instance from dictionary.

        Args:
            data: Dictionary data

        Returns:
            New instance (must be implemented by subclass)
        """
        raise NotImplementedError("Subclass must implement from_dict")


# Backwards-compatible alias. The data/format modules (json.py,
# csv.py, yaml.py, xml.py) were originally written against a
# `PyfficeDataMixin` name that doesn't exist on this codebase.
# Aliasing it to `PyfficeDataBase` is the minimal-impact fix; new
# code should prefer `PyfficeDataBase`.
PyfficeDataMixin = PyfficeDataBase
