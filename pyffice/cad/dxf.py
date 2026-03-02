"""DXF CAD drawing format support."""
from typing import Any, Optional, List, Dict
import io


def load(path: str) -> str:
    """Load DXF file contents."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def read(path: str) -> str:
    """Read DXF file contents."""
    return load(path)


def write(data: str, path: str) -> None:
    """Write data to DXF file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def dump(data: str, path: str) -> None:
    """Dump data to DXF file."""
    write(data, path)
