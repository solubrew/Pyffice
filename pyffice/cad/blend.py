"""
Pyffice Blender Handler
"""
from pathlib import Path

class PyfficeBlend:
    EXTENSIONS = {'.blend'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeBlend.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeBlend.DEFAULT_LIMIT
