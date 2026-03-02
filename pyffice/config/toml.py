"""
Pyffice TOML Module - Read/Write TOML files
"""

import sys
from typing import Any, Dict
from pathlib import Path

# Use tomllib (built-in Python 3.11+) or fall back to tomli/toml
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        import toml as tomllib


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
        with open(self.file_path, 'rb') as f:
            return tomllib.load(f)
    
    def read_raw(self) -> str:
        """Read raw TOML string"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return f.read()
    
    def write(self, data: Dict[str, Any]):
        """Write data to TOML file"""
        # For now, use simple string formatting
        lines = []
        def _format_value(v, indent=0):
            if isinstance(v, dict):
                lines.append('{' + ', '.join(f'"{k}": {_format_value(val)}' for k, val in v.items()) + '}')
            elif isinstance(v, list):
                lines.append('[' + ', '.join(str(x) for x in v) + ']')
            elif isinstance(v, str):
                lines.append(f'"{v}"')
            else:
                lines.append(str(v))
            return lines[-1]
        
        for section, values in data.items():
            lines.append(f"[{section}]")
            if isinstance(values, dict):
                for key, value in values.items():
                    if isinstance(value, str):
                        lines.append(f'{key} = "{value}"')
                    else:
                        lines.append(f'{key} = {value}')
            lines.append("")
        
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            f.write('\n'.join(lines))
    
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


# Alias for compatibility
load = read_toml
read = read_toml
write = write_toml
__all__ = ['PyfficeTOML', 'read_toml', 'write_toml', 'load', 'read', 'write']
