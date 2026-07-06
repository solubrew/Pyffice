"""
Pyffice TAR Handler - Read/Write TAR archives
"""
import tarfile
from pathlib import Path
from typing import List, Dict, Any, Optional


class PyfficeTar:
    EXTENSIONS = {'.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2', '.tar.xz', '.txz'}
    DEFAULT_LIMIT = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str, mode: str = 'r'):
        self.file_path = Path(file_path)
        self.mode = mode
    
    @staticmethod
    def size_limit(path: str) -> int:
        return PyfficeTar.DEFAULT_LIMIT
    
    @staticmethod
    def inline(path: str) -> bool:
        return Path(path).stat().st_size < PyfficeTar.DEFAULT_LIMIT
    
    def read(self) -> List[Dict[str, Any]]:
        """List contents of TAR file"""
        with tarfile.open(self.file_path, 'r:*') as tf:
            return [{'name': m.name, 'size': m.size, 'type': m.type} for m in tf.getmembers()]
    
    def extract(self, member: str, path: str = '.') -> None:
        """Extract a file from TAR"""
        with tarfile.open(self.file_path, 'r:*') as tf:
            tf.extract(member, path)
    
    def extract_all(self, path: str = '.') -> None:
        """Extract all files from TAR"""
        with tarfile.open(self.file_path, 'r:*') as tf:
            tf.extractall(path)
    
    def read_file(self, member: str) -> bytes:
        """Read a specific file from TAR"""
        with tarfile.open(self.file_path, 'r:*') as tf:
            return tf.extractfile(member).read()
    
    def write(self, file_path: str, arcname: Optional[str] = None) -> None:
        """Add a file to TAR"""
        with tarfile.open(self.file_path, 'a') as tf:
            tf.add(file_path, arcname or Path(file_path).name)
    
    def write_data(self, name: str, data: bytes) -> None:
        """Add data as file to TAR"""
        import io
        with tarfile.open(self.file_path, 'a') as tf:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    
    def create(archive_path: str, files: Dict[str, str], compression: str = 'gz') -> None:
        """Create TAR from dict of arcname -> file_path"""
        mode = f'w:{compression}' if compression else 'w'
        with tarfile.open(archive_path, mode) as tf:
            for arcname, file_path in files.items():
                tf.add(file_path, arcname)


# Module-level convenience functions
def read(tar_path: str) -> List[Dict[str, Any]]:
    """List contents of TAR file"""
    return PyfficeTar(tar_path).read()


def load(tar_path: str) -> List[Dict[str, Any]]:
    """List contents of TAR file"""
    return read(tar_path)


def write(tar_path: str, files: Dict[str, str], compression: str = 'gz') -> None:
    """Create TAR from dict of arcname -> file_path"""
    PyfficeTar.create(tar_path, files, compression)


def extract(tar_path: str, path: str = '.') -> None:
    """Extract TAR to directory"""
    PyfficeTar(tar_path).extract_all(path)


def extract_file(tar_path: str, member: str, path: str = '.') -> None:
    """Extract specific file from TAR"""
    PyfficeTar(tar_path).extract(member, path)


__all__ = ['PyfficeTar', 'read', 'write', 'load', 'extract', 'extract_file', 'create', 'compress']

# Aliases for test compatibility
read_tar = read
write_tar = write
extract_tar = extract
compress_tar = write  # compress is similar to write for tar
