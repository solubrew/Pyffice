"""IGES CAD format support (Initial Graphics Exchange Specification)."""

from typing import Any, Optional
import io

from pyffice.document import PyfficeDocument
from pyffice.io_helpers import load_via_class, dump_via_class


class PyfficeIGES(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """IGES CAD file handler"""

    EXTENSIONS = {".iges", ".igs"}
    DEFAULT_LIMIT = 100 * 1024 * 1024  # 100MB

    def __init__(self, file_path: str = None, cfg=None) -> None:
        super().__init__(cfg)
        self.file_path = file_path

    def read(self) -> str:
        """Load IGES file contents."""
        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def write(self, data: str) -> None:
        """Write data to IGES file."""
        with open(self.file_path, "w", encoding="utf-8") as f:
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


def load(path: str) -> str:
    """Load IGES file contents."""
    return load_via_class(PyfficeIGES, path)


def read(path: str) -> str:
    """Read IGES file contents."""
    return load(path)


def write(data: str, path: str) -> None:
    """Write data to IGES file."""
    dump_via_class(PyfficeIGES, data, path)


def dump(data: str, path: str) -> None:
    """Dump data to IGES file."""
    write(data, path)
