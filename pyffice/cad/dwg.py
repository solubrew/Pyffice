"""DWG CAD drawing format support."""
from typing import Any, Optional
import io


def load(path: str) -> bytes:
    """Load DWG file contents."""
    with open(path, 'rb') as f:
        return f.read()


def read(path: str) -> bytes:
    """Read DWG file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to DWG file."""
    with open(path, 'wb') as f:
        f.write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to DWG file."""
    write(data, path)
