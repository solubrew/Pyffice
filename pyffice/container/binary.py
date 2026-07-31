"""Pyffice Binary Container Module"""
import base64
from pathlib import Path
from typing import Any, Optional


# Per-type size limits (bytes)
DEFAULT_LIMITS = {
    # Office
    'xlsx': 256 * 1024 * 1024,
    'docx': 256 * 1024 * 1024,
    'pptx': 256 * 1024 * 1024,
    'pdf': 256 * 1024 * 1024,
    # Media
    'mp4': 256 * 1024 * 1024,
    'mp3': 256 * 1024 * 1024,
    'wav': 256 * 1024 * 1024,
    'avi': 256 * 1024 * 1024,
    'mkv': 256 * 1024 * 1024,
    'flac': 256 * 1024 * 1024,
    # Images
    'png': 256 * 1024 * 1024,
    'jpg': 256 * 1024 * 1024,
    'jpeg': 256 * 1024 * 1024,
    'gif': 256 * 1024 * 1024,
    'webp': 256 * 1024 * 1024,
    'bmp': 256 * 1024 * 1024,
    # Data
    'csv': 256 * 1024 * 1024,
    'json': 256 * 1024 * 1024,
    'xml': 256 * 1024 * 1024,
    'yaml': 256 * 1024 * 1024,
    'yml': 256 * 1024 * 1024,
    # Config
    'ini': 256 * 1024 * 1024,
    'toml': 256 * 1024 * 1024,
    'env': 256 * 1024 * 1024,
    # CAD
    'obj': 256 * 1024 * 1024,
    'stl': 256 * 1024 * 1024,
    'scad': 256 * 1024 * 1024,
    'dxf': 256 * 1024 * 1024,
    # Web
    'html': 256 * 1024 * 1024,
    'htm': 256 * 1024 * 1024,
    # Archive
    'zip': 256 * 1024 * 1024,
    'tar': 256 * 1024 * 1024,
    'gz': 256 * 1024 * 1024,
    # Default fallback
    'default': 256 * 1024 * 1024,
}

# Module-level limits storage
_limits_storage = dict(DEFAULT_LIMITS)


def get_limit_for_type(ext: str) -> int:
    """Get size limit for a file extension."""
    ext = ext.lower().lstrip('.')
    return _limits_storage.get(ext, _limits_storage['default'])


def set_limit_for_type(ext: str, limit: int) -> None:
    """Set size limit for a file extension."""
    ext = ext.lower().lstrip('.')
    _limits_storage[ext] = limit


class PyfficeBinaryContainer:
    """Container that stores documents either as inline base64 or as file paths."""
    
    def __init__(self, mode: str = 'auto', custom_limits: Optional[dict] = None):
        """
        mode: 'auto' (auto-detect), 'inline' (always embed), 'path' (always reference)
        custom_limits: dict of ext -> bytes
        """
        self.mode = mode
        self.limits = {**DEFAULT_LIMITS, **(custom_limits or {})}
        self._documents: dict = {}
    
    def get_limit(self, ext: str) -> int:
        """Return the limit.
        
        Args:
            ext: Parameter.
        
        Returns:
            Self for chaining.
        """
        ext = ext.lower().lstrip('.')
        return self.limits.get(ext, self.limits['default'])
    
    def set_limit(self, ext: str, limit: int) -> None:
        """Set the limit.
        
        Args:
            ext: Parameter.
            limit: Parameter.
        
        Returns:
            Self for chaining.
        """
        ext = ext.lower().lstrip('.')
        self.limits[ext] = limit
    
    def add(self, name: str, file_path: str) -> bool:
        """Add a document to the container."""
        path = Path(file_path)
        if not path.exists():
            return False
        
        ext = path.suffix.lower().lstrip('.')
        limit = self.get_limit(ext)
        size = path.stat().st_size
        
        if size > limit:
            raise ValueError(f"{ext} exceeds {limit} byte limit")
        
        if self.mode == 'path':
            self._documents[name] = {'mode': 'path', 'path': str(path), 'ext': ext, 'size': size}
        elif self.mode == 'inline':
            with open(path, 'rb') as f:
                data = base64.b64encode(f.read()).decode('utf-8')
            self._documents[name] = {'mode': 'inline', 'data': data, 'ext': ext, 'size': size}
        else:  # auto
            if size < 10 * 1024 * 1024:  # < 10MB inline
                with open(path, 'rb') as f:
                    data = base64.b64encode(f.read()).decode('utf-8')
                self._documents[name] = {'mode': 'inline', 'data': data, 'ext': ext, 'size': size}
            else:
                self._documents[name] = {'mode': 'path', 'path': str(path), 'ext': ext, 'size': size}
        
        return True
    
    def get(self, name: str) -> Optional[bytes]:
        """Retrieve document content as bytes."""
        doc = self._documents.get(name)
        if not doc:
            return None
        
        if doc['mode'] == 'inline':
            return base64.b64decode(doc['data'])
        else:
            with open(doc['path'], 'rb') as f:
                return f.read()
    
    def list(self) -> list[str]:
        """List.
        
        Returns:
            Self for chaining.
        """
        return list(self._documents.keys())
    
    def info(self, name: str) -> Optional[dict]:
        """Info.
        
        Args:
            name: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._documents.get(name)
    
    def remove(self, name: str) -> bool:
        """Remove.
        
        Args:
            name: Parameter.
        
        Returns:
            Self for chaining.
        """
        if name in self._documents:
            del self._documents[name]
            return True
        return False
    
    def __len__(self) -> int:
        return len(self._documents)
