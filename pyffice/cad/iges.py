"""IGES CAD format support (Initial Graphics Exchange Specification)."""

from typing_extensions import Self
from typing import Any, Optional
import io

from kahndor.logma import Logma

from pyffice.document import PyfficeDocument
from pyffice.io_helpers import load_via_class, dump_via_class

logma = Logma(__name__)


class PyfficeIGES(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """IGES CAD file handler"""

    EXTENSIONS = {".iges", ".igs"}
    DEFAULT_LIMIT = 100 * 1024 * 1024  # 100MB

    def __init__(self, file_path: str = None, cfg=None) -> None:
        super().__init__(cfg)
        self.file_path = file_path
        # _content caches the raw IGES text after read(); _entities is
        # the parsed entity list (populated by parse_iges()).
        self._content: Optional[str] = None
        self._entities: list = []

    def read(self) -> str:
        """Load IGES file contents.

        Reads the file from disk and caches it on ``self._content``.
        Returns the raw text. Use :meth:`parse_iges` to populate the
        structured ``self._entities`` list.
        """
        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        self._content = text
        return text

    def write(self, data: str) -> None:
        """Write IGES data to ``self.file_path``.

        Updates ``self._content`` so subsequent :meth:`to_dict` calls
        see the current payload.
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(data)
        self._content = data

    def parse_iges(self) -> list:
        """Parse the cached IGES text into a list of entity dicts.

        IGES fixed-format puts each logical entity's primary record on
        one line of variable length (typically 73-80 columns). Section
        boundaries are signalled by sequence-number suffixes:
          - the digit-and-letter suffix at the END of the line
            (last 7 columns when padded to 80) holds the sequence
            number; the LAST digit/character of that suffix indicates
            the section: 'S' starts a new entity (single-record),
            'G' terminates the global section.
          - everything before the suffix is the entity data
            (type code + parameters), comma-separated.

        The parser detects these suffixes by matching the line's
        trailing non-space token: lines ending in ``,S<num>`` start a
        new entity; lines ending in ``,G<num>`` or just ``G`` close
        the current entity and end the global section. The leading
        integer code (before the first comma) becomes the entity type.

        Each returned entity is ``{"type": str, "raw": list[str]}``
        where ``raw`` is the list of section lines belonging to it.
        """
        import re as _re
        if self._content is None:
            self.read()
        # IGES fixed-format: data (padded to col 64) followed by either
        # spaces or a single space separator, then a section marker
        # letter (S for new entity, G for global terminator) and the
        # sequence number (right-aligned). The marker matches a trailing
        # pattern of ``S\\s*\\d+`` or ``G\\s*\\d+`` at the very end of the
        # line. Continuation lines (no terminal S/G) are appended to the
        # current entity's section.
        boundary_re = _re.compile(r"([SG])\s*\d+\s*$")
        entities: list[dict] = []
        current_lines: list[str] = []
        current_type: Optional[str] = None

        def _flush():
            nonlocal current_lines, current_type
            if current_lines:
                entities.append({
                    "type": current_type or "unknown",
                    "raw": list(current_lines),
                })
                current_lines = []
                current_type = None

        for raw_line in (self._content or "").splitlines():
            line = raw_line.rstrip()
            if not line:
                continue
            m = boundary_re.search(line)
            if m is None:
                # Continuation / parameter-expansion line.
                if current_lines:
                    current_lines.append(line)
                continue
            section_marker = m.group(1)
            # Boundary detected: flush any in-progress entity first, then
            # start the new one.
            _flush()
            # Determine the new entity's type code from the integer
            # prefix of the line (everything before the first comma).
            type_code = line.split(",", 1)[0].strip()
            if not type_code.isdigit():
                type_code = "unknown"
            current_type = type_code
            current_lines = [line]
            if section_marker == "G":
                # Global terminator: record the G line as its own 'G'
                # entity then flush.
                _flush()
                current_type = "G"
                current_lines = [line]
                _flush()
        _flush()
        self._entities = entities
        return entities

    def load_document(self, document=None) -> Self:
        """Restore PyfficeIGES state from a canonical envelope.

        Calls the base implementation first so :attr:`did`,
        :attr:`meta_data`, and :attr:`data.path` are populated.
        Then unpacks IGES-specific fields from ``data.content``:

        - ``file_path``: the path the IGES was/is loaded from
        - ``content``: the cached raw IGES text (if available)
        - ``entities``: parsed entity list (if available, otherwise empty)

        Args:
            document: A dict produced by :meth:`to_dict`, or ``None``.

        Returns:
            Self for chaining.
        """
        logma.debug(f"PyfficeIGES.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            self.file_path = content.get("file_path", self.file_path)
            self._content = content.get("content")
            ents = content.get("entities", []) or []
            self._entities = list(ents)
        return self

    def open_file(self, file_=None) -> Self:
        """Load IGES content from a JSON envelope file.

        Reads the file (must be in the canonical envelope produced by
        :meth:`to_dict`) and delegates to :meth:`load_document`. Returns
        self on failure (no exceptions raised).

        Args:
            file_: Path to a JSON envelope. ``None`` means use
                ``self.file_path``.

        Returns:
            Self for chaining.
        """
        import json as _json
        from os.path import exists
        if file_ is None:
            file_ = self.file_path
        if not file_ or not exists(file_):
            logma.warning(f"PyfficeIGES.open_file: no such path {file_!r}")
            return self
        try:
            with open(file_, "r") as f:
                doc = _json.load(f)
        except (OSError, ValueError) as e:
            logma.warning(f"PyfficeIGES.open_file failed for {file_!r}: {e}")
            return self
        logma.debug(f"PyfficeIGES.open_file loaded {file_!r}")
        return self.load_document(doc)

    def save(self, path=None, format_=None, encrypt=None) -> None:
        """Persist the canonical envelope to disk as JSON.

        Writes ``self.to_dict()`` (which serializes ``_content`` and
        ``_entities`` if present) to ``path``. Calls
        :meth:`super().save` first to bump version metadata.

        Args:
            path: Destination file path. ``None`` means use
                ``self.file_path``.
            format_: Ignored (always JSON for canonical envelopes).
            encrypt: Ignored.

        Returns:
            None.
        """
        logma.debug(f"PyfficeIGES.save called path={path!r}")
        super().save(path, format_, encrypt)
        if path is None:
            path = self.file_path
        if not path:
            logma.warning("PyfficeIGES.save: no path available")
            return
        import json as _json
        doc = self.to_dict()
        with open(path, "w") as f:
            _json.dump(doc, f, indent=2, default=str)
        return None

    def to_dict(self) -> Self:
        """Serialize PyfficeIGES state to a canonical envelope.

        Builds the doc dict with the IGES-specific payload under
        ``data.content``:

        - ``file_path``: the on-disk IGES path
        - ``content``: the cached raw IGES text (populated by
          :meth:`read`); ``None`` if read has not been called yet
        - ``entities``: the parsed entity list (populated by
          :meth:`parse_iges`); empty list if parse has not run

        The key order puts ``content`` first so the canonical ``content``
        slot is satisfied before any other dict keys (which prevents
        :meth:`PyfficeDocument._canonicalize` from mirroring a string
        into it).

        Returns:
            The canonical envelope dict.
        """
        logma.debug(f"PyfficeIGES.to_dict called")
        super().to_dict()  # populate canonical envelope on self
        # Ensure parse has run so the envelope carries the entity list
        if not self._entities and self._content:
            self.parse_iges()
        doc = {
            "did": self.did,
            "meta_data": {"schema_version": list(self.SERIALIZATION_VERSION)},
            "data": {
                "content": {
                    "file_path": self.file_path,
                    "content": self._content,
                    "entities": list(self._entities or []),
                },
                "document_type": "iges",
            },
        }
        return self._canonicalize(doc)


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
