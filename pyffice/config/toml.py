"""
Pyffice TOML Module - Read/Write TOML files
"""

import toml
from typing import Any, Dict
from pathlib import Path


class PyfficeTOML:
    """Handle TOML file operations"""
    
    SUPPORTED_EXTENSIONS = ['.toml']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self) -> Dict[str, Any]:
        """Read TOML file"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return toml.load(f)
    
    def read_raw(self) -> str:
        """Read raw TOML string"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return f.read()
    
    def write(self, data: Dict[str, Any]):
        """Write data to TOML file"""
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            toml.dump(data, f)
    
    def write_raw(self, data: str):
        """Write raw TOML string"""
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            f.write(data)


def read_toml(file_path: str) -> Dict[str, Any]:
    """Convenience function to read TOML"""
    return PyfficeTOML(file_path).read()


def write_toml(file_path: str, data: Dict[str, Any]):
    """Convenience function to write TOML"""
    PyfficeTOML(file_path).write(data)
