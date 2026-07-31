"""Amazon Kindle (AZW) ebook format support.

The load/read/write/dump helpers are thin wrappers around the
shared :mod:`pyffice.io_helpers` byte I/O. They're kept here so
callers can continue to import ``from pyffice.ebook.azw import
load`` etc. (the per-format module API is part of pyffice's
public surface).
"""
from typing import Any, Optional
import io

from pyffice.io_helpers import load_bytes, write_bytes


def load(path: str) -> bytes:
    """Load AZW ebook contents."""
    return load_bytes(path)


def read(path: str) -> bytes:
    """Read AZW ebook contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to AZW file."""
    write_bytes(data, path)


def dump(data: bytes, path: str) -> None:
    """Dump data to AZW file."""
    write(data, path)
