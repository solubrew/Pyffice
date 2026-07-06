"""
DXF CAD drawing format support.
"""
from typing import Any, Optional, List, Dict
import io

from pyffice.document import PyfficeDocument


class PyfficeDXF(PyfficeDocument):
    """DXF CAD drawing handler"""
    
    EXTENSIONS = {'.dxf'}
    DEFAULT_LIMIT = 100 * 1024 * 1024  # 100MB
    
    def __init__(self, file_path: str = None, cfg=None):
        super().__init__(cfg)
        self.file_path = file_path
    
    def read(self) -> str:
        """Load DXF file contents."""
        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def write(self, data: str) -> None:
        """Write data to DXF file."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(data)
    
    def load(self) -> str:
        """Alias for read()"""
        return self.read()


# Module-level convenience functions
def load(path: str) -> str:
    """Load DXF file contents."""
    return PyfficeDXF(path).read()


def read(path: str) -> str:
    """Read DXF file contents."""
    return load(path)


def write(data: str, path: str) -> None:
    """Write data to DXF file."""
    PyfficeDXF(path).write(data)


def dump(data: str, path: str) -> None:
    """Dump data to DXF file."""
    write(data, path)


__all__ = ['PyfficeDXF', 'load', 'read', 'write', 'dump']
