"""
Pyffice MOBI Handler
"""
from pathlib import Path

class PyfficeMobi:
    EXTENSIONS = {'.mobi', '.pdb'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeMobi.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeMobi.DEFAULT_LIMIT
