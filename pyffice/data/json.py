"""
Pyffice JSON Data Handler
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Union


def read(filepath: str, encoding: str = "utf-8") -> Union[Dict, List]:
    """Read JSON file and return data."""
    with open(filepath, "r", encoding=encoding) as f:
        return json.load(f)


def write(filepath: str, data: Any, indent: int = 2, encoding: str = "utf-8") -> None:
    """Write data to JSON file."""
    with open(filepath, "w", encoding=encoding) as f:
        json.dump(data, f, indent=indent)


def append(filepath: str, data: Any, encoding: str = "utf-8") -> None:
    """Append data to JSON file (list or object)."""
    existing = []
    path = Path(filepath)
    if path.exists() and path.stat().st_size > 0:
        existing = read(filepath, encoding)
    
    if isinstance(existing, list):
        if isinstance(data, list):
            existing.extend(data)
        else:
            existing.append(data)
    elif isinstance(existing, dict) and isinstance(data, dict):
        existing.update(data)
    else:
        existing = [existing, data] if existing else data
    
    write(filepath, existing, encoding=encoding)


def merge(filepath: str, data: Dict, encoding: str = "utf-8") -> None:
    """Merge data into existing JSON object."""
    existing = {}
    path = Path(filepath)
    if path.exists() and path.stat().st_size > 0:
        existing = read(filepath, encoding)
        if not isinstance(existing, dict):
            existing = {"data": existing}
    
    existing.update(data)
    write(filepath, existing, encoding=encoding)
