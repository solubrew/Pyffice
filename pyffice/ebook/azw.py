"""Amazon Kindle (AZW) ebook format support."""
from typing import Any, Optional
import io


def load(path: str) -> bytes:
    """Load AZW ebook contents."""
    with open(path, 'rb') as f:
        return f.read()


def read(path: str) -> bytes:
    """Read AZW ebook contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to AZW file."""
    with open(path, 'wb') as f:
        f.write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to AZW file."""
    write(data, path)
