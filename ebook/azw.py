"""
Pyffice AZW Handler
"""
from pathlib import Path

class PyfficeAzw:
    EXTENSIONS = {'.azw', '.azw3', '.azw4'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeAzw.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeAzw.DEFAULT_LIMIT
