"""
FBX 3D model format support (Filmbox).
"""
from typing import Any, Optional
import io

from pyffice.document import PyfficeDocument


class PyfficeFBX(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """FBX 3D model handler"""
    
    EXTENSIONS = {'.fbx'}
    DEFAULT_LIMIT = 512 * 1024 * 1024  # 512MB
    
    def __init__(self, file_path: str = None, cfg=None):
        super().__init__(cfg)
        self.file_path = file_path
    
    def read(self) -> bytes:
        """Load FBX file contents."""
        with open(self.file_path, 'rb') as f:
            return f.read()
    
    def write(self, data: bytes) -> None:
        """Write data to FBX file."""
        with open(self.file_path, 'wb') as f:
            f.write(data)
    
    def load(self) -> bytes:
        """Alias for read()"""
        return self.read()


# Module-level convenience functions
def load(path: str) -> bytes:
    """Load FBX file contents."""
    return PyfficeFBX(path).read()


def read(path: str) -> bytes:
    """Read FBX file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to FBX file."""
    PyfficeFBX(path).write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to FBX file."""
    write(data, path)


__all__ = ['PyfficeFBX', 'load', 'read', 'write', 'dump']
