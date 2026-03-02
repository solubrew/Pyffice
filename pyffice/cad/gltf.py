"""
Pyffice GLTF Handler
"""
from pathlib import Path

class PyfficeGltf:
    EXTENSIONS = {'.gltf', '.glb'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeGltf.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeGltf.DEFAULT_LIMIT
