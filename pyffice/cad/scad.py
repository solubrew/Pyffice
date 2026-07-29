"""OpenSCAD script format support."""
from typing import Any, Optional
import io

from pyffice.document import PyfficeDocument


class PyfficeSCAD(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """OpenSCAD script document."""
    
    def __init__(self, path: Optional[str] = None, content: Optional[str] = None):
        super().__init__(path=path, content=content)
        self.doc_type = "scad"
    
    def load(self, path: str) -> str:
        """Load OpenSCAD script contents."""
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        self.content = content
        return content
    
    def read(self, path: str) -> str:
        """Read OpenSCAD script contents."""
        return self.load(path)
    
    def write(self, data: str, path: str) -> None:
        """Write data to OpenSCAD file."""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)
    
    def dump(self, data: str, path: str) -> None:
        """Dump data to OpenSCAD file."""
        self.write(data, path)
