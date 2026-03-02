"""
Pyffice 7-Zip Handler
"""
from pathlib import Path

class PyfficeSevenZip:
    EXTENSIONS = {'.7z', '.7zip'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeSevenZip.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeSevenZip.DEFAULT_LIMIT
