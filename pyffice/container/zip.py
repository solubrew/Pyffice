"""
Pyffice ZIP Handler - Read/Write ZIP archives
"""
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional


class PyfficeZip:
    EXTENSIONS = {'.zip', '.zipx'}
    DEFAULT_LIMIT = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str, mode: str = 'r'):
        self.file_path = Path(file_path)
        self.mode = mode
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeZip.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeZip.DEFAULT_LIMIT
    
    def read(self) -> List[Dict[str, Any]]:
        """List contents of ZIP file"""
        with zipfile.ZipFile(self.file_path, 'r') as zf:
            return [{'name': n, 'size': zf.getinfo(n).file_size} for n in zf.namelist()]
    
    def extract(self, member: str, path: str = '.') -> None:
        """Extract a file from ZIP"""
        with zipfile.ZipFile(self.file_path, 'r') as zf:
            zf.extract(member, path)
    
    def extract_all(self, path: str = '.') -> None:
        """Extract all files from ZIP"""
        with zipfile.ZipFile(self.file_path, 'r') as zf:
            zf.extractall(path)
    
    def read_file(self, member: str) -> bytes:
        """Read a specific file from ZIP"""
        with zipfile.ZipFile(self.file_path, 'r') as zf:
            return zf.read(member)
    
    def write(self, file_path: str, arcname: Optional[str] = None) -> None:
        """Add a file to ZIP"""
        with zipfile.ZipFile(self.file_path, 'a') as zf:
            zf.write(file_path, arcname or Path(file_path).name)
    
    def write_data(self, name: str, data: bytes) -> None:
        """Add data as file to ZIP"""
        with zipfile.ZipFile(self.file_path, 'a') as zf:
            zf.writestr(name, data)
    
    @staticmethod
    def create(archive_path: str, files: Dict[str, str]) -> None:
        """Create ZIP from dict of arcname -> file_path"""
        with zipfile.ZipFile(archive_path, 'w') as zf:
            for arcname, file_path in files.items():
                zf.write(file_path, arcname)


# Module-level convenience functions
def read(zip_path: str) -> List[Dict[str, Any]]:
    """List contents of ZIP file"""
    return PyfficeZip(zip_path).read()


def load(zip_path: str) -> List[Dict[str, Any]]:
    """List contents of ZIP file"""
    return read(zip_path)


def write(zip_path: str, files: Dict[str, str]) -> None:
    """Create ZIP from dict of arcname -> file_path"""
    PyfficeZip.create(zip_path, files)


def extract(zip_path: str, path: str = '.') -> None:
    """Extract ZIP to directory"""
    PyfficeZip(zip_path).extract_all(path)


def extract_file(zip_path: str, member: str, path: str = '.') -> None:
    """Extract specific file from ZIP"""
    PyfficeZip(zip_path).extract(member, path)


def compress(source_dir: str, archive_path: str) -> None:
    """Compress a directory into a ZIP file"""
    import os
    files = {}
    for root, dirs, filenames in os.walk(source_dir):
        for fname in filenames:
            fpath = os.path.join(root, fname)
            arcname = os.path.relpath(fpath, source_dir)
            files[arcname] = fpath
    PyfficeZip.create(archive_path, files)


def create(archive_path: str, files: Dict[str, str]) -> None:
    """Create ZIP from dict of arcname -> file_path (module-level alias)"""
    PyfficeZip.create(archive_path, files)


__all__ = ['PyfficeZip', 'read', 'write', 'load', 'extract', 'extract_file', 'create', 'compress']
