"""
glTF 3D model format support.
"""
from typing import Any, Optional, Dict, List
import json

from pyffice.document import PyfficeDocument


class PyfficeGLTF(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """glTF 3D model handler"""
    
    EXTENSIONS = {'.gltf', '.glb'}
    DEFAULT_LIMIT = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str = None, cfg=None):
        super().__init__(cfg)
        self.file_path = file_path
    
    def read(self) -> Dict[str, Any]:
        """Load glTF model."""
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def write(self, data: Dict[str, Any]) -> None:
        """Write glTF model."""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self) -> Dict[str, Any]:
        """Alias for read()"""
        return self.read()


# Module-level convenience functions
def load(path: str) -> Dict[str, Any]:
    """Load glTF model."""
    return PyfficeGLTF(path).read()


def read(path: str) -> Dict[str, Any]:
    """Read glTF model."""
    return load(path)


def write(data: Dict[str, Any], path: str) -> None:
    """Write glTF model."""
    PyfficeGLTF(path).write(data)


def dump(data: Dict[str, Any], path: str) -> None:
    """Dump glTF model."""
    write(data, path)


__all__ = ['PyfficeGLTF', 'load', 'read', 'write', 'dump']
