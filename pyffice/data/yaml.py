"""
Pyffice YAML Data Handler
"""

import yaml
from pathlib import Path
from typing import Any, Dict, List


def load(filepath: str) -> Any:
    """Load YAML file and return data."""
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def read(filepath: str) -> Any:
    """Alias for load."""
    return load(filepath)


def dump(filepath: str, data: Any, default_flow_style: bool = False) -> None:
    """Dump data to YAML file."""
    with open(filepath, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=default_flow_style, sort_keys=False)


def write(filepath: str, data: Any) -> None:
    """Alias for dump."""
    dump(filepath, data)


def append(filepath: str, data: Any) -> None:
    """Append data to YAML file (appends to list or merges dict)."""
    existing = []
    path = Path(filepath)
    if path.exists() and path.stat().st_size > 0:
        existing = load(filepath)
        if not isinstance(existing, list):
            existing = [existing]
    
    if isinstance(existing, list):
        if isinstance(data, list):
            existing.extend(data)
        else:
            existing.append(data)
    else:
        existing = [existing, data] if existing else data
    
    dump(filepath, existing)


def merge(filepath: str, data: Dict) -> None:
    """Merge data into existing YAML file."""
    existing = {}
    path = Path(filepath)
    if path.exists() and path.stat().st_size > 0:
        existing = load(filepath)
        if not isinstance(existing, dict):
            existing = {"data": existing}
    
    existing.update(data)
    dump(filepath, existing)
