"""
Pyffice JSON Module - Read/Write JSON files
"""

import json
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class PyfficeJSON:
    """Handle JSON file operations"""
    
    SUPPORTED_EXTENSIONS = ['.json', '.jsonl']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self, encoding: Optional[str] = None) -> Union[Dict, List, Any]:
        """Read JSON file"""
        with open(self.file_path, 'r', encoding=encoding or self.encoding) as f:
            return json.load(f)
    
    def read_raw(self) -> str:
        """Read raw JSON string"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return f.read()
    
    def write(self, data: Any, indent: int = 2, sort_keys: bool = False):
        """Write data to JSON file"""
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            json.dump(data, f, indent=indent, sort_keys=sort_keys)
    
    def write_raw(self, data: str):
        """Write raw JSON string"""
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            f.write(data)


class PyfficeJSONL:
    """Handle JSON Lines file operations"""
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = Path(file_path)
        self.encoding = encoding
    
    def read(self) -> List[Dict]:
        """Read JSONL file"""
        lines = []
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(json.loads(line))
        return lines
    
    def write(self, data: List[Dict]):
        """Write list of dicts to JSONL"""
        with open(self.file_path, 'w', encoding=self.encoding) as f:
            for item in data:
                f.write(json.dumps(item) + '\n')


def read_json(file_path: str, **kwargs) -> Any:
    """Convenience function to read JSON"""
    return PyfficeJSON(file_path).read(**kwargs)


def write_json(file_path: str, data: Any, **kwargs):
    """Convenience function to write JSON"""
    PyfficeJSON(file_path).write(data, **kwargs)


def read_jsonl(file_path: str) -> List[Dict]:
    """Convenience function to read JSONL"""
    return PyfficeJSONL(file_path).read()


def write_jsonl(file_path: str, data: List[Dict]):
    """Convenience function to write JSONL"""
    PyfficeJSONL(file_path).write(data)
