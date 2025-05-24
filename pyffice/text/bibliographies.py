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
from pyffice.document import PyfficeDocument
from pyffice.tags.references import PyfficeReference

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "bibliographies.yaml")


class PyfficeBibliography(PyfficeDocument):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeBibliography")).override(cfg)
        self.references = None
        self.style = None

    def add_reference(self, cfg=None):
        """"""
        reference = PyfficeReference(cfg)
        self.add_change("references", self.references, reference, "add")
        self.references.append(reference)
        return self

    def del_reference(self, index):
        """"""
        self.add_change("references", self.references, index, "del")
        del self.references[index]
        return self

    def del_references(self):
        """"""
        self.add_change("references", self.references, [], "del")
        self.references = None
        return self

    def get_reference(self, index):
        """"""
        return self.references[index]

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_style(document.get("style", None))
        self.set_references(document.get("references", None))
        return self

    def set_references(self, references):
        """"""
        if references != self.references:
            self.add_change("references", self.references, references, "set")
        self.references = references if references is not None else []
        return self

    def set_style(self, style):
        """"""
        if style != self.style:
            self.add_change("style", self.style, style, "set")
        self.style = style
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"]["style"] = self.style.to_dict() if self.style is not None else None
        doc["document"]["references"] = (
            [ref.to_dict() for ref in self.references] if self.references is not None else None
        )
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
