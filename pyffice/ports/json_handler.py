"""JSON file handler for the ports layer.

Migrated from pyffice/data/json.py (T-NEW-069). The data/ directory
was deprecated because every file in it had zero callers; the JSON
functionality moves here where it belongs alongside the other file
format handlers.

The original data/json.py inherited from PyfficeDataMixin (a
typo-alias for PyfficeDataBase in data/base.py). After migrating,
the inheritance is dropped because:
- PyfficeDataBase is an ABC with @abstractmethod methods
- The concrete methods (get, set, merge, etc.) duplicated ours
- The base class is also being deleted (zero callers)

The two methods that PyfficeDataMixin actually contributed
(`get` and `set`) are reimplemented here as plain helpers. All
file-level functions are preserved verbatim.
"""

import json
from pathlib import Path
from typing import Any, Optional

from kahndor.logma import Logma

logma = Logma(__name__)
logma.off()


def read(filepath: str) -> dict:
    """Read a JSON file and return the parsed dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def parse(json_string: str) -> Any:
    """Parse a JSON string into a Python object."""
    return json.loads(json_string)


def write(filepath: str, data: Any, indent: int = 2) -> None:
    """Write a Python object to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def to_string(data: Any, indent: int = 2) -> str:
    """Convert a Python object to a JSON string."""
    return json.dumps(data, indent=indent, ensure_ascii=False)


def create(initial: Any = None) -> "PyfficeJSON":
    """Create a new PyfficeJSON instance, optionally seeded with data."""
    obj = PyfficeJSON()
    if initial is not None:
        obj._data = initial
    return obj


def add_child(parent: dict, key: str, value: Any) -> dict:
    """Add a child key-value pair to a parent dict (mutates parent)."""
    parent[key] = value
    return parent


class PyfficeJSON:
    """Handler for JSON file operations."""

    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize PyfficeJSON handler.

        Args:
            file_path: Optional path to JSON file
        """
        logma.debug(f"PyfficeJSON.__init__ called")
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

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by dotted key (e.g. 'user.profile.name').

        Replaces the PyfficeDataMixin.get() method that was dropped
        when the data/ base class was deleted.
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
        """Set a value by dotted key (e.g. 'user.profile.name').

        Replaces the PyfficeDataMixin.set() method that was dropped.
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
