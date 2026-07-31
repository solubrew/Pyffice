"""
Pyffice HEIC/AVIF Image Handler
"""
from pathlib import Path

class PyfficeHeic:
    EXTENSIONS = {'.heic', '.heif', '.avif', '.avifs'}
    DEFAULT_LIMIT = 256 * 1024 * 1024
    
    @staticmethod
    def size_limit(path: str) -> int:
        """Size limit.
        
        Args:
            path: Parameter.
        
        Returns:
            Self for chaining.
        """
        return PyfficeHeic.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        """Inline.
        
        Args:
            path: Parameter.
        
        Returns:
            Self for chaining.
        """
        return Path(path).stat().st_size < PyfficeHeic.DEFAULT_LIMIT
