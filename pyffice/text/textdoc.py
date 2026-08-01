#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

from typing_extensions import Self
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

# ======================================3rd Party Library Modules=====================================================||


# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument
from pyffice.items.text import PyfficeText, PyfficeParagraph, PyfficeFont

# ====================================================================================================================||
HERE = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
PXCFG = join(HERE, "_data_", ".yaml")


class PyfficeTextDocument(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """Text document with full formatting support."""

    def __init__(self, cfg=None) -> None:
        """Initialize the text document following the PyfficeScript template.

        Calls super().__init__(cfg) FIRST so the base attributes
        (config, did, name, description, content, etc.) are populated
        before the class-specific state. Only then initializes
        self.text and self.metadata.

        Args:
            cfg: Optional config dict.
        """
        super().__init__(cfg)
        logma.debug(f"PyfficeTextDocument.__init__ called")
        self.text = PyfficeText()
        self.metadata: Dict[str, Any] = {}

    def add_heading(
        self,
        text: str,
        level: int = 1,
    ) -> PyfficeParagraph:
        """Add a heading paragraph."""
        sizes = {1: 24.0, 2: 20.0, 3: 16.0, 4: 14.0, 5: 12.0, 6: 11.0}
        font = PyfficeFont(size=sizes.get(level, 14.0), bold=True)
        return self.text.add_paragraph(text, font=font)

    def add_paragraph(
        self,
        text: str,
        style: Optional[str] = None,
    ) -> PyfficeParagraph:
        """Add a regular paragraph."""
        para = self.text.add_paragraph(text)
        para.style = style
        return para

    def add_bullet(
        self,
        text: str,
        level: int = 0,
    ) -> PyfficeParagraph:
        """Add a bullet point."""
        para = self.text.add_paragraph(text)
        para.numbering = {"type": "bullet", "level": level}
        return para

    def add_numbered(
        self,
        text: str,
        number: int,
        level: int = 0,
    ) -> PyfficeParagraph:
        """Add a numbered item."""
        para = self.text.add_paragraph(text)
        para.numbering = {"type": "number", "number": number, "level": level}
        return para

    def __str__(self) -> str:
        """Return plain text representation."""
        return self.text.text

    def load_document(self, document=None) -> Self:
        """Load a TextDocument envelope previously produced by to_dict.

        Calls the canonical base implementation (which sets did,
        content, paths, schema_version, etc.), then restores the
        class-specific state (PyfficeText tree + metadata) from the
        envelope's data.content slot.

        Args:
            document: Dict produced by to_dict() (or a JSON string).

        Returns:
            Self for chaining.
        """
        logma.debug(f"PyfficeTextDocument.load_document called for {document.get('did', '?') if isinstance(document, dict) else '?'}")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if not isinstance(content, dict):
            content = {}
        self.metadata = content.get("metadata", {}) or {}
        text_data = content.get("text", {}) or {}
        if isinstance(text_data, dict) and text_data:
            # PyfficeText.load_unit accepts a dict shape directly.
            self.text.load_unit(text_data)
        return self

    def open_file(self, file_=None) -> Self:
        """Open a .json TextDocument and load it.

        Reads the JSON envelope from disk and delegates to
        load_document. Returns self even on read failure (logs a
        warning).

        Args:
            file_: Path to a JSON file. None means use self.file_path.

        Returns:
            Self for chaining.
        """
        import json as _json
        from os.path import exists
        if file_ is None:
            file_ = self.file_path
        if not file_ or not exists(file_):
            logma.warning(f"PyfficeTextDocument.open_file: no such path {file_!r}")
            return self
        try:
            with open(file_, "r") as f:
                doc = _json.load(f)
        except (OSError, ValueError) as e:
            logma.warning(f"PyfficeTextDocument.open_file failed for {file_!r}: {e}")
            return self
        logma.debug(f"PyfficeTextDocument.open_file loaded {file_!r}")
        return self.load_document(doc)

    def save(self, path=None, format_=None, encrypt=None) -> None:
        """Save this document to a JSON envelope on disk.

        Calls super().save() first to bump version / change tracking,
        then writes the canonical envelope (to_dict output) as JSON.

        Args:
            path: Destination file path. None means use self.file_path.
            format_: Unused (always JSON for TextDocument).
            encrypt: Unused.
        """
        logma.debug(f"PyfficeTextDocument.save called path={path!r}")
        super().save(path, format_, encrypt)
        if path is None:
            path = self.file_path
        if not path:
            logma.warning("PyfficeTextDocument.save: no path available")
            return
        import json as _json
        doc = self.to_dict()
        with open(path, "w") as f:
            _json.dump(doc, f, indent=2, default=str)
        return None

    def to_dict(self) -> Self:
        """Convert to canonical envelope (matching PyfficeScript template).

        Builds the doc envelope with class-specific payload under
        data.content (the canonical slot). data.content holds:
          - text: dict from PyfficeText.to_dict()
          - metadata: dict (text document metadata: title, author, etc.)
          - document_type: "text_document"

        Returns:
            self._canonicalize(doc) — the canonical envelope as a dict.
        """
        logma.debug("PyfficeTextDocument.to_dict called")
        super().to_dict()  # populate canonical envelope on self
        text_dict = {}
        try:
            text_dict = self.text.to_dict()
        except Exception:
            text_dict = {}
        doc = {
            "did": self.did,
            "meta_data": {"schema_version": list(self.SERIALIZATION_VERSION)},
            "data": {
                "content": {
                    "text": text_dict,
                    "metadata": getattr(self, "metadata", {}) or {},
                },
                "document_type": "text_document",
            },
        }
        return self._canonicalize(doc)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
