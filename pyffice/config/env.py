"""
Pyffice ENV Module - Read/Write ENV files
"""

import os
from typing import Dict, Optional
from pathlib import Path


class PyfficeENV:
    """Handle ENV file operations"""
    
    SUPPORTED_EXTENSIONS = ['.env']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self) -> Dict[str, str]:
        """Read ENV file as dict"""
        env_vars = {}
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        env_vars[key] = value
        return env_vars
    
    def read_raw(self) -> str:
        """Read raw ENV string"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return f.read()
    
    def write(self, data: Dict[str, str], comments: Optional[list] = None):
        """Write dict to ENV file"""
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            if comments:
                for comment in comments:
                    f.write(f"# {comment}\n")
            for key, value in data.items():
                f.write(f"{key}={value}\n")
    
    def write_raw(self, data: str):
        """Write raw ENV string"""
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            f.write(data)
    
    def load_to_env(self):
        """Load ENV vars into os.environ"""
        env_vars = self.read()
        os.environ.update(env_vars)


def read_env(file_path: str) -> Dict[str, str]:
    """Convenience function to read ENV"""
    return PyfficeENV(file_path).read()


def write_env(file_path: str, data: Dict[str, str], **kwargs):
    """Convenience function to write ENV"""
    PyfficeENV(file_path).write(data, **kwargs)
