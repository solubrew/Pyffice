"""
Blender (.blend) 3D model format support.
"""
from typing import Any, Optional
import io

from pyffice.document import PyfficeDocument
from pyffice.io_helpers import load_via_class, dump_via_class


class PyfficeBLEND(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """Blender .blend file handler"""

    EXTENSIONS = {'.blend'}
    DEFAULT_LIMIT = 512 * 1024 * 1024  # 512MB

    def __init__(self, file_path: str = None, cfg=None) -> None:
        super().__init__(cfg)
        if file_path:
            self.file_path = file_path

    def read(self) -> bytes:
        """Load Blender file contents."""
        with open(self.file_path, 'rb') as f:
            return f.read()

    def write(self, data: bytes) -> None:
        """Write data to Blender file."""
        with open(self.file_path, 'wb') as f:
            f.write(data)


# Module-level convenience functions
def load(path: str) -> bytes:
    """Load Blender file contents."""
    return load_via_class(PyfficeBLEND, path)


def read(path: str) -> bytes:
    """Read Blender file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to Blender file."""
    dump_via_class(PyfficeBLEND, data, path)


def dump(data: bytes, path: str) -> None:
    """Dump data to Blender file."""
    write(data, path)


__all__ = ['PyfficeBLEND', 'load', 'read', 'write', 'dump']
