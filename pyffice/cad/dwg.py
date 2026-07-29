"""
DWG CAD drawing format support.
"""
from typing import Any, Optional
import io

from pyffice.document import PyfficeDocument


class PyfficeDWG(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """DWG CAD drawing handler"""
    
    EXTENSIONS = {'.dwg'}
    DEFAULT_LIMIT = 100 * 1024 * 1024  # 100MB
    
    def __init__(self, file_path: str = None, cfg=None):
        super().__init__(cfg)
        self.file_path = file_path
    
    def read(self) -> bytes:
        """Load DWG file contents."""
        with open(self.file_path, 'rb') as f:
            return f.read()
    
    def write(self, data: bytes) -> None:
        """Write data to DWG file."""
        with open(self.file_path, 'wb') as f:
            f.write(data)
    
    def load(self) -> bytes:
        """Alias for read()"""
        return self.read()


# Module-level convenience functions
def load(path: str) -> bytes:
    """Load DWG file contents."""
    return PyfficeDWG(path).read()


def read(path: str) -> bytes:
    """Read DWG file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to DWG file."""
    PyfficeDWG(path).write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to DWG file."""
    write(data, path)


__all__ = ['PyfficeDWG', 'load', 'read', 'write', 'dump']
