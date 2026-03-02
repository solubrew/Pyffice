"""PPTX (PowerPoint) presentation format support."""
from typing import Any, Optional
import zipfile
import io


def load(path: str) -> bytes:
    """Load PPTX file contents."""
    with open(path, 'rb') as f:
        return f.read()


def read(path: str) -> bytes:
    """Read PPTX file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to PPTX file."""
    with open(path, 'wb') as f:
        f.write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to PPTX file."""
    write(data, path)
