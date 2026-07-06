"""ODT (OpenDocument Text) format support."""
from typing import Any, Optional
import zipfile
import io


def load(path: str) -> bytes:
    """Load ODT file contents."""
    with open(path, 'rb') as f:
        return f.read()


def read(path: str) -> bytes:
    """Read ODT file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to ODT file."""
    with open(path, 'wb') as f:
        f.write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to ODT file."""
    write(data, path)
