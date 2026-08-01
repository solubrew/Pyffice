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
from pyffice.document import PyfficeDocument
from pyffice.tags.references import PyfficeReference
from typing import Any
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "bibliographies.yaml")


class PyfficeBibliography(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeBibliography")).override(cfg)
        self.references = None
        self.style = None

    def add_reference(self, cfg=None) -> Self:
        """Add a reference.
        
        Args:
            cfg: Parameter.
        
        Returns:
            Self for chaining.
        """
        reference = PyfficeReference(cfg)
        self.add_change("references", self.references, reference, "add")
        self.references.append(reference)
        return self

    def del_reference(self, index) -> Self:
        """Remove a reference from this document.
        
        Args:
            index: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("references", self.references, index, "del")
        del self.references[index]
        return self

    def del_references(self) -> Self:
        """Remove the references.
        
        Returns:
            Self for chaining.
        """
        self.add_change("references", self.references, [], "del")
        self.references = None
        return self

    def get_reference(self, index) -> Any:
        """Return the reference.
        
        Args:
            index: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self.references[index]

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
            if document is None:
                document = {}
        super().load_document(document)
        self.set_style(document.get("style", None))
        self.set_references(document.get("references", None))
        return self

    def set_references(self, references) -> Self:
        """Set the references.
        
        Args:
            references: Parameter.
        
        Returns:
            Self for chaining.
        """
        if references != self.references:
            self.add_change("references", self.references, references, "set")
        self.references = references if references is not None else []
        return self

    def set_style(self, style) -> Self:
        """Set the style.

        Args:
            style: Parameter.

        Returns:
            Self for chaining.
        """
        return self._set_with_change("style", style)

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
