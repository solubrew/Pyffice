"""
Pyffice IGES Handler
"""
from pathlib import Path

class PyfficeIges:
    EXTENSIONS = {'.iges', '.igs'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeIges.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeIges.DEFAULT_LIMIT
