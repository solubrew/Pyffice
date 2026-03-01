"""
Pyffice Raw Image Handler
"""
from pathlib import Path

class PyfficeRaw:
    EXTENSIONS = {'.cr2', '.nef', '.arw', '.dng', '.orf', '.rw2', '.pef', '.srw', '.raf', '.3fr', '.mef', '.nrw'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeRaw.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeRaw.DEFAULT_LIMIT
