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
from pyffice.items.text import PyfficeText

# ====================================================================================================================||
HERE = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
PXCFG = join(HERE, "_data_", ".yaml")


class PyfficeTextDocument(PyfficeDocument):
    """Text document with full formatting support."""

    def __init__(self):
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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
