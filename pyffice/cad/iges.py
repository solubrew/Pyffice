"""IGES CAD format support (Initial Graphics Exchange Specification)."""
from typing import Any, Optional
import io


def load(path: str) -> str:
    """Load IGES file contents."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def read(path: str) -> str:
    """Read IGES file contents."""
    return load(path)


def write(data: str, path: str) -> None:
    """Write data to IGES file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def dump(data: str, path: str) -> None:
    """Dump data to IGES file."""
    write(data, path)
