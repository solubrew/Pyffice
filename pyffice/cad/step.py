"""
Pyffice STEP Handler
"""
from pathlib import Path

class PyfficeStep:
    EXTENSIONS = {'.step', '.stp'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeStep.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeStep.DEFAULT_LIMIT
