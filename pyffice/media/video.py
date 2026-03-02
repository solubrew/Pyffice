"""Video file format support."""
from typing import Any, Optional
import io


def load(path: str) -> bytes:
    """Load video file contents."""
    with open(path, 'rb') as f:
        return f.read()


def read(path: str) -> bytes:
    """Read video file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to video file."""
    with open(path, 'wb') as f:
        f.write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to video file."""
    write(data, path)
