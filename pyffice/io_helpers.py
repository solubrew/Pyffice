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

from typing import Any, Callable


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


__all__ = [
    "load_bytes",
    "write_bytes",
    "load_text",
    "write_text",
    "load_via_class",
    "dump_via_class",
    "read",
    "dump",
]
