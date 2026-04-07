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
from pyffice.document import PyfficeDocumentManager
from pyffice.tags.tags import PyfficeTag

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeTag(object):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeTag").override(cfg)
        self.description = None
        self.label = None
        self.value = None
        self.doc_type = "tags"

    def load_tag(self, tag=None):
        """"""
        if tag is None:
            tag = self.config.dikt.get("tag", {})
        self.set_description(tag.get("description", None))
        self.set_label(tag.get("label", None))
        self.set_value(tag.get("value", None))
        return self

    def set_description(self, description):
        """"""
        self.description = description
        return self

    def set_label(self, label):
        """"""
        self.label = label
        return self

    def set_value(self, value):
        """"""
        self.value = value
        return self

    def to_dict(self):
        """"""
        doc = {
            "label": self.label,
            "description": self.description,
            "value": self.value,
        }
        return doc


class PyfficeTagsManager(PyfficeDocumentManager):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(
            condor.Instruct(pxcfg).select("PyfficeTagsManager")
        ).override(cfg)
        self.tags = []

    def add_tag(self, name, description="", group=None):
        """"""
        cfg = {"tag": {"name": name, "description": description, "group": group}}
        tag = PyfficeTag(cfg)
        tag.load_tag()
        self.tags.append(tag)
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
        super().load_document(document)
        self.set_tags(document.get("tags", []))
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = {"tags": self.tags}
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
