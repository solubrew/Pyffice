"""Blender (.blend) 3D model format support."""
from typing import Any, Optional
import io


def load(path: str) -> bytes:
    """Load Blender file contents."""
    with open(path, 'rb') as f:
        return f.read()


def read(path: str) -> bytes:
    """Read Blender file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to Blender file."""
    with open(path, 'wb') as f:
        f.write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to Blender file."""
    write(data, path)
