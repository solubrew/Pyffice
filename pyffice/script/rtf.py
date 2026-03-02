"""
Pyffice RTF Handler
"""
from pathlib import Path

class PyfficeRtf:
    EXTENSIONS = {'.rtf'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeRtf.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeRtf.DEFAULT_LIMIT
