# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
            A BOM is a workflow because in its ultimate form the needs of that BOM are placed on a timeline of events.
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

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "_data_", "bom.yaml")


class PyfficeBOM(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).override("PyfficeBOM")
        super().__init__(self)
        self.config.override(cfg)

    def add_part(self, part):
        """"""
        super().add_document(part)

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeSoftwareBOM(PyfficeBOM):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).override("PyfficeSoftwareBOM")
        super().__init__(self)
        self.config.override(cfg)

    def add_part(self, part):
        """"""
        super().add_part(part)

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
