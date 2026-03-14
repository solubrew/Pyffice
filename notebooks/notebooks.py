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
from condor import condor
from ogma.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.text.text import PyfficeText

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "notebooks.yaml")


class PyfficeNotebook(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).override("PyfficeNotebook")).override(cfg)
        self.cells = None
        self.notebook = None

    def add_cell(self, cell):
        """"""
        self.cells.append(cell)
        return self

    def clear_cell(self, dex):
        """"""
        self.cells[dex]["outputs"] = []
        return self

    def clear_cells(self):
        """"""
        for cell in self.cells:
            cell["outputs"] = []
        return self

    def del_cell(self, dex):
        """"""
        self.cells.pop(dex)
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_notebook(document.get("notebook", None))
        self.set_cells(document.get("notebook", None))
        return self

    def set_cells(self, cells):
        """"""
        if cells != self.cells:
            self.add_change("cells", self.cells, cells)
            self.cells = cells
        return self

    def set_cell_source(self, text, position=0):
        """"""
        cfg = {"text": text}
        text = PyfficeText(cfg)
        self.cells[position]["source"] = text
        return self

    def set_notebook(self, notebook=None):
        """"""
        if notebook is None:
            notebook = {
                "cells": [],
            }
        if notebook != self.notebook:
            self.add_change("notebook", self.notebook, notebook)
            self.notebook = notebook
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = {"notebook": self.notebook}
        doc["document"]["notebook"]["cells"] = [x.to_dict() for x in self.cells]
        return doc

    def to_html(self):
        """"""
        return self.to_html()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
