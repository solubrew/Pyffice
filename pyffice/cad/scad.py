"""OpenSCAD script format support."""
from typing import Any, Optional
import io


def load(path: str) -> str:
    """Load OpenSCAD script contents."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def read(path: str) -> str:
    """Read OpenSCAD script contents."""
    return load(path)


def write(data: str, path: str) -> None:
    """Write data to OpenSCAD file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def dump(data: str, path: str) -> None:
    """Dump data to OpenSCAD file."""
    write(data, path)
