"""
Pyffice EPUB Handler
"""
from pathlib import Path

class PyfficeEpub:
    EXTENSIONS = {'.epub'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeEpub.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeEpub.DEFAULT_LIMIT
