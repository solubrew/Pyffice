"""
Pyffice YAML Module - Read/Write YAML files
"""

import yaml
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class PyfficeYAML:
    """Handle YAML file operations"""
    
    SUPPORTED_EXTENSIONS = ['.yaml', '.yml']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self) -> Any:
        """Read YAML file"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return yaml.safe_load(f)
    
    def read_raw(self) -> str:
        """Read raw YAML string"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return f.read()
    
    def write(self, data: Any, default_flow_style: bool = False):
        """Write data to YAML file"""
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            yaml.safe_dump(data, f, default_flow_style=default_flow_style, sort_keys=False)
    
    def write_raw(self, data: str):
        """Write raw YAML string"""
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            f.write(data)


def read_yaml(file_path: str) -> Any:
    """Convenience function to read YAML"""
    return PyfficeYAML(file_path).read()


def write_yaml(file_path: str, data: Any, **kwargs):
    """Convenience function to write YAML"""
    PyfficeYAML(file_path).write(data, **kwargs)
