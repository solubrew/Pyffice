"""MOBI ebook format support.

Thin wrappers around :mod:`pyffice.io_helpers` byte I/O. See
:mod:`pyffice.ebook.azw` for the rationale on keeping the
per-format module API.
"""
from typing import Any, Optional
import io

from pyffice.io_helpers import load_bytes, write_bytes


def load(path: str) -> bytes:
    """Load MOBI ebook contents."""
    return load_bytes(path)


def read(path: str) -> bytes:
    """Read MOBI ebook contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to MOBI file."""
    write_bytes(data, path)


def dump(data: bytes, path: str) -> None:
    """Dump data to MOBI file."""
    write(data, path)
