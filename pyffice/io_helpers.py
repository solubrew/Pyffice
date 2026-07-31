# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid: pyffice-io-helpers-001
    name: pyffice/io_helpers.py
    description: >
        Shared module-level I/O helpers used by the format-specific
        CAD / ebook / media modules (azw, blend, dwg, dxf, fbx,
        gltf, iges, mobi, pptx, step, media_audio, media_video).

        The 14 format modules each had identical ``load`` / ``read``
        / ``write`` / ``dump`` functions. Most were straight
        binary file copies; a few wrapped a class. This module
        collapses both patterns into two reusable helpers that the
        format modules import.

        - :func:`load_bytes` / :func:`read_bytes` / :func:`write_bytes`
          / :func:`dump_bytes`: byte-level file I/O. ``read`` is an
          alias of ``load`` and ``dump`` is an alias of ``write``
          (matching the previous per-module signature).
        - :func:`load_via_class` / :func:`dump_via_class`: dispatch
          to a format class that has ``read()`` / ``write(data)``
          methods. ``read`` is an alias of ``load`` and ``dump`` is
          an alias of ``write``.

        Format modules can now write:
            from pyffice.io_helpers import load_bytes, write_bytes
            def load(path): return load_bytes(path)
            def write(data, path): write_bytes(data, path)

        instead of defining four functions per file.
    version: 0.1.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""

# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, List, Dict, Optional


def load_bytes(path: str) -> bytes:
    """Read the entire contents of ``path`` as bytes."""
    with open(path, "rb") as f:
        return f.read()


def write_bytes(data: bytes, path: str) -> None:
    """Write ``data`` to ``path`` as bytes."""
    with open(path, "wb") as f:
        f.write(data)


def load_text(path: str, encoding: str = "utf-8", errors: str = "ignore") -> str:
    """Read the entire contents of ``path`` as text."""
    with open(path, "r", encoding=encoding, errors=errors) as f:
        return f.read()


def write_text(
    data: str,
    path: str,
    encoding: str = "utf-8",
    errors: str = "strict",
) -> None:
    """Write ``data`` to ``path`` as text."""
    with open(path, "w", encoding=encoding, errors=errors) as f:
        f.write(data)


def load_via_class(cls: type, path: str) -> Any:
    """Construct ``cls(path)`` and call its ``read()`` method.

    Used by format modules whose class has a custom ``read()`` that
    parses the file (e.g. STEP / DXF / IGES). Returns whatever the
    class's ``read()`` returns.
    """
    return cls(path).read()


def dump_via_class(cls: type, data: Any, path: str) -> None:
    """Construct ``cls(path)`` and call its ``write(data)`` method.

    Used by format modules whose class has a custom ``write()``
    that serializes the data (e.g. STEP / DXF / IGES).
    """
    cls(path).write(data)


# Convenient aliases so callers can use the original names
read = load_bytes
dump = write_bytes


class ArchiveHandler:
    """Base class for archive file handlers (ZIP, TAR, etc.).

    Subclasses override the private ``_open_read``, ``_list_members``,
    ``_extract``, ``_extractall``, ``_read_member``, ``_write_member``,
    ``_write_data``, and ``_create`` hooks with the archive-specific
    implementation. The public ``read`` / ``extract`` / ``extract_all``
    / ``read_file`` / ``write`` / ``write_data`` / ``create`` methods
    here provide the shared structure and the ``size_limit`` /
    ``inline`` static helpers.

    Consolidates what was duplicated across ``zip.py``, ``tar.py``,
    ``rar.py``, ``sevenzip.py``, etc. Each subclass only implements
    the format-specific hooks instead of re-implementing the same
    control flow.
    """

    #: Subclasses override this with their file extension set.
    EXTENSIONS: set[str] = set()
    #: Subclasses override this with their default size limit.
    DEFAULT_LIMIT: int = 256 * 1024 * 1024  # 256MB

    def __init__(self, file_path: str, mode: str = "r") -> None:
        """Initialize the archive handler.

        Args:
            file_path: Path to the archive file.
            mode: Open mode (read/write/append).
        """
        self.file_path = Path(file_path)
        self.mode = mode

    @classmethod
    def size_limit(cls, path: str) -> int:
        """Return the size limit for the archive.

        Args:
            path: Parameter (path to the archive).

        Returns:
            The handler's DEFAULT_LIMIT.
        """
        return cls.DEFAULT_LIMIT

    @classmethod
    def inline(cls, path: str) -> bool:
        """Return whether the archive is small enough to load inline.

        Args:
            path: Parameter (path to the archive).

        Returns:
            ``True`` if the file size is below ``DEFAULT_LIMIT``.
        """
        try:
            return Path(path).stat().st_size < cls.DEFAULT_LIMIT
        except OSError:
            return False

    def read(self) -> List[Dict[str, Any]]:
        """List contents of the archive.

        Returns:
            List of member metadata dicts (``name``, ``size``, ...).
        """
        with self._open_read() as handle:
            return self._list_members(handle)

    def extract(self, member: str, path: str = ".") -> None:
        """Extract a single member to ``path``.

        Args:
            member: Name of the member to extract.
            path: Destination directory.
        """
        with self._open_read() as handle:
            self._extract(handle, member, path)

    def extract_all(self, path: str = ".") -> None:
        """Extract all members to ``path``.

        Args:
            path: Destination directory.
        """
        with self._open_read() as handle:
            self._extractall(handle, path)

    def read_file(self, member: str) -> bytes:
        """Read the bytes of a single member.

        Args:
            member: Name of the member to read.

        Returns:
            The member's bytes.
        """
        with self._open_read() as handle:
            return self._read_member(handle, member)

    def write(
        self, file_path: str, arcname: Optional[str] = None
    ) -> None:
        """Add a file to the archive.

        Args:
            file_path: Path of the file to add.
            arcname: Name to use inside the archive. Defaults to
                the file's basename.
        """
        with self._open_read(mode="a") as handle:
            self._write_member(handle, file_path, arcname)

    def write_data(self, name: str, data: bytes) -> None:
        """Add in-memory bytes as a member named ``name``.

        Args:
            name: Archive member name.
            data: Bytes to write.
        """
        with self._open_read(mode="a") as handle:
            self._write_data(handle, name, data)

    @classmethod
    def create(cls, archive_path: str, files: Dict[str, str], **kwargs) -> None:
        """Create an archive from a dict of arcname -> file_path.

        Args:
            archive_path: Destination archive path.
            files: Mapping of arcname (in archive) to file_path (on disk).
            **kwargs: Format-specific options (e.g. compression).
        """
        cls._create(archive_path, files, **kwargs)

    # ------------------------------------------------------------------
    # Hooks subclasses override with format-specific implementations.
    # ------------------------------------------------------------------
    def _open_read(self, mode: str = "r") -> Any:  # pragma: no cover
        """Return an open archive handle. Override in subclass."""
        raise NotImplementedError

    def _list_members(self, handle: Any) -> List[Dict[str, Any]]:  # pragma: no cover
        """Return member metadata. Override in subclass."""
        raise NotImplementedError

    def _extract(self, handle: Any, member: str, path: str) -> None:  # pragma: no cover
        """Extract a single member. Override in subclass."""
        raise NotImplementedError

    def _extractall(self, handle: Any, path: str) -> None:  # pragma: no cover
        """Extract all members. Override in subclass."""
        raise NotImplementedError

    def _read_member(self, handle: Any, member: str) -> bytes:  # pragma: no cover
        """Read one member's bytes. Override in subclass."""
        raise NotImplementedError

    def _write_member(
        self, handle: Any, file_path: str, arcname: Optional[str]
    ) -> None:  # pragma: no cover
        """Write a file into the archive. Override in subclass."""
        raise NotImplementedError

    def _write_data(self, handle: Any, name: str, data: bytes) -> None:  # pragma: no cover
        """Write in-memory bytes as a member. Override in subclass."""
        raise NotImplementedError

    @classmethod
    def _create(
        cls, archive_path: str, files: Dict[str, str], **kwargs
    ) -> None:  # pragma: no cover
        """Create a new archive from a files mapping. Override in subclass."""
        raise NotImplementedError


__all__ = [
    "load_bytes",
    "write_bytes",
    "load_text",
    "write_text",
    "load_via_class",
    "dump_via_class",
    "read",
    "dump",
    "ArchiveHandler",
]
