"""
Pyffice HEIC/AVIF Image Handler
"""

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
