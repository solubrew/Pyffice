"""glTF 3D model format support."""
from typing import Any, Optional, Dict, List
import json


def load(path: str) -> Dict[str, Any]:
    """Load glTF model."""
    with open(path, 'r') as f:
        return json.load(f)


def read(path: str) -> Dict[str, Any]:
    """Read glTF model."""
    return load(path)


def write(data: Dict[str, Any], path: str) -> None:
    """Write glTF model."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def dump(data: Dict[str, Any], path: str) -> None:
    """Dump glTF model."""
    write(data, path)
