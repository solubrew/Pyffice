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
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.items.text import PyfficeText

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "notebooks.yaml")


class PyfficeNotebook(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).override("PyfficeNotebook")).override(cfg)
        self.cells = []
        self.notebook = None

    def add_cell(self, cell) -> "PyfficeNotebook":
        """Add a cell.
        
        Args:
            cell: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.cells.append(cell)
        return self

    def clear_cell(self, dex) -> "PyfficeNotebook":
        """Clear cell.
        
        Args:
            dex: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.cells[dex]["outputs"] = []
        return self

    def clear_cells(self) -> "PyfficeNotebook":
        """Clear cells.
        
        Returns:
            Self for chaining.
        """
        for cell in self.cells:
            cell["outputs"] = []
        return self

    def del_cell(self, dex) -> "PyfficeNotebook":
        """Remove the cell.
        
        Args:
            dex: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.cells.pop(dex)
        return self

    def load_document(self, document=None) -> "PyfficeNotebook":
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_notebook(document.get("notebook", None))
        self.set_cells(document.get("notebook", None))
        return self

    def set_cells(self, cells) -> "PyfficeNotebook":
        """Set the cells.
        
        Args:
            cells: Parameter.
        
        Returns:
            Self for chaining.
        """
        if cells != self.cells:
            self.add_change("cells", self.cells, cells)
            self.cells = cells
        return self

    def set_cell_source(self, text, position=0) -> "PyfficeNotebook":
        """Set the cell source.
        
        Args:
            text: Parameter.
            position: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"text": text}
        text = PyfficeText(cfg)
        self.cells[position]["source"] = text
        return self

    def set_notebook(self, notebook=None) -> "PyfficeNotebook":
        """Set the notebook.
        
        Args:
            notebook: Parameter.
        
        Returns:
            Self for chaining.
        """
        if notebook is None:
            notebook = {
                "cells": [],
            }
        if notebook != self.notebook:
            self.add_change("notebook", self.notebook, notebook)
            self.notebook = notebook
        return self

    def set_pinned(self, pinned) -> "PyfficeNotebook":
        """Set pinned state."""
        self.pinned = pinned
        return self
    def to_html(self) -> Any:
        """Convert this document to html.
        
        Returns:
            Self for chaining.
        """
        return self.to_html()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
