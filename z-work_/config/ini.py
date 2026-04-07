"""
Pyffice INI Module - Read/Write INI/CFG files
"""

import configparser
from typing import Dict, Any, Optional
from pathlib import Path


class PyfficeINI:
    """Handle INI/CFG file operations"""
    
    SUPPORTED_EXTENSIONS = ['.ini', '.cfg', '.conf']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._validate()
        self._parser = configparser.ConfigParser()
    
    def _validate(self):
        if self.file_path.exists() and self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self) -> Dict[str, Dict[str, str]]:
        """Read INI file as nested dict"""
        self._parser.read(self.file_path, encoding=self.encoding)
        return {section: dict(self._parser[section]) for section in self._parser.sections()}
    
    def read_raw(self) -> str:
        """Read raw INI string"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return f.read()
    
    def write(self, data: Dict[str, Dict[str, str]]):
        """Write nested dict to INI file"""
        for section, values in data.items():
            self._parser.add_section(section)
            for key, value in values.items():
                self._parser.set(section, key, str(value))
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            self._parser.write(f)
    
    def get(self, section: str, key: str, fallback: Optional[str] = None) -> Optional[str]:
        """Get value from section/key"""
        self._parser.read(self.file_path, encoding=self.encoding)
        try:
            return self._parser.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def set(self, section: str, key: str, value: str):
        """Set value for section/key"""
        self._parser.read(self.file_path, encoding=self.encoding)
        if not self._parser.has_section(section):
            self._parser.add_section(section)
        self._parser.set(section, key, value)
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            self._parser.write(f)


def read_ini(file_path: str) -> Dict[str, Dict[str, str]]:
    """Convenience function to read INI"""
    return PyfficeINI(file_path).read()


def write_ini(file_path: str, data: Dict[str, Dict[str, str]]):
    """Convenience function to write INI"""
    PyfficeINI(file_path).write(data)


# Alias for compatibility
load = read_ini
read = read_ini
write = write_ini
__all__ = ['PyfficeINI', 'read_ini', 'write_ini', 'load', 'read', 'write']
