"""
Pyffice GLTF Handler
"""
import json
from pathlib import Path
from typing import Dict, Any

class PyfficeGltf:
    EXTENSIONS = {'.gltf', '.glb'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeGltf.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeGltf.DEFAULT_LIMIT
    
    @staticmethod
    def read(filepath: str) -> Dict[str, Any]:
        """Read GLTF file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def write(filepath: str, data: Dict[str, Any]) -> None:
        """Write GLTF file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
