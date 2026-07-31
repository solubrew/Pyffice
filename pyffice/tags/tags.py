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

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "_data_", "tags.yaml")


class PyfficeTag(object):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeTag").override(cfg)
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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
