"""
Pyffice FBX Handler
"""
from pathlib import Path

class PyfficeFbx:
    EXTENSIONS = {'.fbx'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeFbx.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeFbx.DEFAULT_LIMIT
