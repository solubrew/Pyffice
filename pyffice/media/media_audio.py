"""Audio file format support."""
from typing import Any, Optional
import io


def load(path: str) -> bytes:
    """Load audio file contents."""
    with open(path, 'rb') as f:
        return f.read()


def read(path: str) -> bytes:
    """Read audio file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to audio file."""
    with open(path, 'wb') as f:
        f.write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to audio file."""
    write(data, path)
