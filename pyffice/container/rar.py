"""
Pyffice RAR Handler
"""
from pathlib import Path

class PyfficeRar:
    EXTENSIONS = {'.rar', '.rar5'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeRar.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeRar.DEFAULT_LIMIT
