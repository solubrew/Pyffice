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
from pyffice.document import PyfficeDocumentManager
from pyffice.tags.tags import PyfficeTag
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeTagsManager(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeTagsManager")).override(cfg)
        self.tags = []

    def add_tag(self, name, description="", group=None) -> Self:
        """Attach a tag to this document.
        
        Args:
            name: Parameter.
            description: Parameter.
            group: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"tag": {"name": name, "description": description, "group": group}}
        tag = PyfficeTag(cfg)
        tag.load_tag()
        self.tags.append(tag)
        return self

    def load_document(self, document=None) -> Self:
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
        super().load_document(document)
        self.set_tags(document.get("tags", []))
        return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
