"""MOBI ebook format support."""
from typing import Any, Optional
import io


def load(path: str) -> bytes:
    """Load MOBI ebook contents."""
    with open(path, 'rb') as f:
        return f.read()


def read(path: str) -> bytes:
    """Read MOBI ebook contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to MOBI file."""
    with open(path, 'wb') as f:
        f.write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to MOBI file."""
    write(data, path)
