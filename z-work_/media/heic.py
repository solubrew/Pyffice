"""
Pyffice HEIC/AVIF Image Handler
"""
from pathlib import Path

class PyfficeHeic:
    EXTENSIONS = {'.heic', '.heif', '.avif', '.avifs'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeHeic.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeHeic.DEFAULT_LIMIT
