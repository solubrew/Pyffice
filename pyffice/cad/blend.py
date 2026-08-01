"""
Blender (.blend) 3D model format support.
"""

from typing_extensions import Self
from typing import Any, Optional
import io

from pyffice.document import PyfficeDocument
from pyffice.io_helpers import load_via_class, dump_via_class


class PyfficeBLEND(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """Blender .blend file handler"""

    EXTENSIONS = {".blend"}
    DEFAULT_LIMIT = 512 * 1024 * 1024  # 512MB

    def __init__(self, file_path: str = None, cfg=None) -> None:
        super().__init__(cfg)
        if file_path:
            self.file_path = file_path

    def read(self) -> bytes:
        """Load Blender file contents."""
        with open(self.file_path, "rb") as f:
            return f.read()

    def write(self, data: bytes) -> None:
        """Write data to Blender file."""
        with open(self.file_path, "wb") as f:
            f.write(data)

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "file_path" in content:
                setattr(self, "file_path", content["file_path"])
        return self

    def open_file(self, file_=None):
        import json as _json
        from os.path import exists
        if file_ is None:
            file_ = self.file_path
        if not file_ or not exists(file_):
            logma.warning(f"{self.__class__.__name__}.open_file: no such path {file_!r}")
            return self
        try:
            with open(file_, "r") as f:
                doc = _json.load(f)
        except (OSError, ValueError) as e:
            logma.warning(f"{self.__class__.__name__}.open_file failed for {file_!r}: {e}")
            return self
        return self.load_document(doc)

    def save(self, path=None, format_=None, encrypt=None):
        logma.debug(f"{self.__class__.__name__}.save called path={path!r}")
        super().save(path, format_, encrypt)
        if path is None:
            path = self.file_path
        if not path:
            logma.warning(f"{self.__class__.__name__}.save: no path available")
            return
        import json as _json
        doc = self.to_dict()
        with open(path, "w") as f:
            _json.dump(doc, f, indent=2, default=str)
        return

    def to_dict(self):
        # TODO implement method
        super().to_dict()
        return self


# Module-level convenience functions
def load(path: str) -> bytes:
    """Load Blender file contents."""
    return load_via_class(PyfficeBLEND, path)


def read(path: str) -> bytes:
    """Read Blender file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to Blender file."""
    dump_via_class(PyfficeBLEND, data, path)


def dump(data: bytes, path: str) -> None:
    """Dump data to Blender file."""
    write(data, path)


__all__ = ["PyfficeBLEND", "load", "read", "write", "dump"]
