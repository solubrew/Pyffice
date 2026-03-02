"""
Pyffice TOML Config Handler
"""

try:
    import tomllib
except ImportError:
    import tomli as tomllib
try:
    import tomli_w
except ImportError:
    import tomlkit as tomli_w

from pathlib import Path
from typing import Any, Dict


def load(filepath: str) -> Dict[str, Any]:
    """Load TOML file and return dictionary."""
    with open(filepath, "rb") as f:
        return tomllib.load(f)


def read(filepath: str) -> Dict[str, Any]:
    """Alias for load."""
    return load(filepath)


def dump(filepath: str, data: Dict[str, Any]) -> None:
    """Dump dictionary to TOML file."""
    with open(filepath, "wb") as f:
        tomli_w.dump(data, f)


def write(filepath: str, data: Dict[str, Any]) -> None:
    """Alias for dump."""
    dump(filepath, data)


def merge(filepath: str, data: Dict[str, Any]) -> None:
    """Merge data into existing TOML file."""
    existing = {}
    path = Path(filepath)
    if path.exists() and path.stat().st_size > 0:
        existing = load(filepath)
    
    existing.update(data)
    dump(filepath, existing)
