"""
DWG CAD drawing format support.
"""

from typing_extensions import Self
from typing import Any, Optional
import io

from pyffice.document import PyfficeDocument
from pyffice.io_helpers import load_via_class, dump_via_class


class PyfficeDWG(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """DWG CAD drawing handler"""

    EXTENSIONS = {".dwg"}
    DEFAULT_LIMIT = 100 * 1024 * 1024  # 100MB

    def __init__(self, file_path: str = None, cfg=None) -> None:
        super().__init__(cfg)
        self.file_path = file_path

    def read(self) -> bytes:
        """Load DWG file contents."""
        with open(self.file_path, "rb") as f:
            return f.read()

    def write(self, data: bytes) -> None:
        """Write data to DWG file."""
        with open(self.file_path, "wb") as f:
            f.write(data)

    def load_document(self, document=None) -> Self:
        """"""
        super().load_document(document)
        # TODO implement method
        return self

    def open_file(self, file_=None):
        """"""
        super().open_file(file_)
        # TODO implement method
        return self

    def save(self, path=None, format_=None, encrypt=None):
        """"""
        super().save(path, format_, encrypt)
        # TODO implement method
        return self

    def to_dict(self):
        # TODO implement method
        super().to_dict()
        return self


# Module-level convenience functions
def load(path: str) -> bytes:
    """Load DWG file contents."""
    return load_via_class(PyfficeDWG, path)


def read(path: str) -> bytes:
    """Read DWG file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to DWG file."""
    dump_via_class(PyfficeDWG, data, path)


def dump(data: bytes, path: str) -> None:
    """Dump data to DWG file."""
    write(data, path)


__all__ = ["PyfficeDWG", "load", "read", "write", "dump"]
