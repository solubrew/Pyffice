"""
Pyffice ZIP Handler
"""
from pathlib import Path

class PyfficeZip:
    EXTENSIONS = {'.zip', '.zipx'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeZip.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeZip.DEFAULT_LIMIT
