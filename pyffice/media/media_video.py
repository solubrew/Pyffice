"""Video file format support.

Thin wrappers around :mod:`pyffice.io_helpers` byte I/O.
"""
from typing import Any, Optional
import io

from pyffice.io_helpers import load_bytes, write_bytes


def load(path: str) -> bytes:
    """Load video file contents."""
    return load_bytes(path)


def read(path: str) -> bytes:
    """Read video file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to video file."""
    write_bytes(data, path)


def dump(data: bytes, path: str) -> None:
    """Dump data to video file."""
    write(data, path)
