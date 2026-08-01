"""
Pyffice ZIP Handler - Read/Write ZIP archives
"""
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional

from kahndor.logma import Logma
from pyffice.io_helpers import ArchiveHandler

logma = Logma(__name__)
logma.off()


class PyfficeZip(ArchiveHandler):
    EXTENSIONS = {'.zip', '.zipx'}
    DEFAULT_LIMIT = 256 * 1024 * 1024  # 256MB

    def _open_read(self, mode: str = 'r') -> Any:
        """Open the underlying ZIP file for reading."""
        logma.debug(f"PyfficeZip._open_read called")
        return zipfile.ZipFile(self.file_path, mode)

    def _list_members(self, handle: Any) -> List[Dict[str, Any]]:
        """Return metadata for each ZIP member."""
        return [
            {'name': n, 'size': handle.getinfo(n).file_size}
            for n in handle.namelist()
        ]

    def _extract(self, handle: Any, member: str, path: str) -> None:
        """Extract a single ZIP member to ``path``."""
        handle.extract(member, path)

    def _extractall(self, handle: Any, path: str) -> None:
        """Extract all ZIP members to ``path``."""
        handle.extractall(path)

    def _read_member(self, handle: Any, member: str) -> bytes:
        """Read a single ZIP member's bytes."""
        return handle.read(member)

    def _write_member(self, handle: Any, file_path: str, arcname: Optional[str]) -> None:
        """Write a file to the ZIP archive."""
        handle.write(file_path, arcname or Path(file_path).name)

    def _write_data(self, handle: Any, name: str, data: bytes) -> None:
        """Write in-memory bytes as a ZIP member named ``name``."""
        handle.writestr(name, data)

    @classmethod
    def _create(cls, archive_path: str, files: Dict[str, str], **kwargs) -> None:
        """Create ZIP from dict of arcname -> file_path."""
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


def create(archive_path: str, files) -> None:
    """Module-level alias for ``PyfficeZip.create``.

    Args:
        archive_path: Destination ZIP path.
        files: Mapping of arcname -> file_path.
    """
    PyfficeZip.create(archive_path, files)


__all__ = ['PyfficeZip', 'read', 'write', 'load', 'extract', 'extract_file', 'create', 'compress']
