"""
Pyffice TAR Handler - Read/Write TAR archives
"""
import io
import tarfile
from pathlib import Path
from typing import List, Dict, Any, Optional

from pyffice.io_helpers import ArchiveHandler

from kahndor.logma import Logma

logma = Logma(__name__)
logma.off()


class PyfficeTar(ArchiveHandler):
    EXTENSIONS = {'.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2', '.tar.xz', '.txz'}
    DEFAULT_LIMIT = 256 * 1024 * 1024  # 256MB

    def _open_read(self, mode: str = 'r') -> Any:
        """Open the underlying TAR file. Read-mode auto-detects compression."""
        logma.debug(f"PyfficeTar._open_read called")
        return tarfile.open(self.file_path, 'r:*' if mode == 'r' else mode)

    def _list_members(self, handle: Any) -> List[Dict[str, Any]]:
        """Return metadata for each TAR member."""
        return [
            {'name': m.name, 'size': m.size, 'type': m.type}
            for m in handle.getmembers()
        ]

    def _extract(self, handle: Any, member: str, path: str) -> None:
        """Extract a single TAR member to ``path``."""
        handle.extract(member, path)

    def _extractall(self, handle: Any, path: str) -> None:
        """Extract all TAR members to ``path``."""
        handle.extractall(path)

    def _read_member(self, handle: Any, member: str) -> bytes:
        """Read a single TAR member's bytes."""
        extracted = handle.extractfile(member)
        return extracted.read() if extracted else b""

    def _write_member(self, handle: Any, file_path: str, arcname: Optional[str]) -> None:
        """Write a file into the TAR archive."""
        handle.add(file_path, arcname or Path(file_path).name)

    def _write_data(self, handle: Any, name: str, data: bytes) -> None:
        """Write in-memory bytes as a TAR member named ``name``."""
        info = tarfile.TarInfo(name)
        info.size = len(data)
        handle.addfile(info, io.BytesIO(data))

    @classmethod
    def _create(cls, archive_path: str, files: Dict[str, str], **kwargs) -> None:
        """Create TAR from dict of arcname -> file_path.

        Args:
            archive_path: Destination TAR path.
            files: Mapping of arcname -> file_path.
            **kwargs: Accepts ``compression`` (e.g. ``'gz'``).
        """
        compression = kwargs.get("compression", "gz")
        mode = f"w:{compression}" if compression else "w"
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
