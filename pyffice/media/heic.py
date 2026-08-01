"""
Pyffice HEIC/AVIF Image Handler
"""

from typing_extensions import Self
from pathlib import Path


class PyfficeHeic:
    EXTENSIONS = {".heic", ".heif", ".avif", ".avifs"}
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
