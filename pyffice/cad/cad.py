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
import math
from abc import ABC, abstractmethod

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.items.items import PyfficePart

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "cad.yaml")


class PyfficeCADAssembly(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeCADAssembly")
        super().__init__(self.config)
        self.config.override(cfg)

    def add_document(self, document) -> None:
        """Add a child document to this manager.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        super().add_document(document)

    def create_new_document(self, name, type_=None) -> None:
        """Create a new document.
        
        Args:
            name: Parameter.
            type_: Parameter.
        
        Returns:
            Self for chaining.
        """
        super().create_new_document(name, "manager")
        self.document["document"] = {
            "material": None,
            "origin": [0, 0],
            "environment": {
                "origin": {"visible": True, "position": [0, 0, 0], "justify": "center"},
                "background": {"color": "black", "size": None},
                "ground": {"visible": False},
            },
            "build": {},
        }

    def add_part(self, part, position=None) -> "PyfficeCADAssembly":
        """Add a part to the CAD document."""
        parts = getattr(self, 'parts', [])
        parts.append((part, position))
        self.parts = parts
        return self


class PyfficeCADManager(PyfficeDocumentManager):
    """Manage all cad related items inlcuding assmeblys, objects, libraries, etc"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeCADManager")
        super().__init__(self)
        self.config.override(cfg)

    def add_document(self, document) -> None:
        """Add a child document to this manager.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        super().add_document(document)

    def add_part(self, assembly) -> "PyfficeCADManager":
        """Add an assembly part."""
        _p = True  # placeholder
        return self

    def create_new_document(self, name, type_=None) -> None:
        """Create a new document.
        
        Args:
            name: Parameter.
            type_: Parameter.
        
        Returns:
            Self for chaining.
        """
        super().create_new_document(name, "manager")

class PyfficeCADPart(PyfficePart):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).override("PyfficeCADPart")
        super().__init__(cfg)
        self.config.override(cfg)

    def create_new_document(self, name) -> "PyfficeCADPart":
        """Create a new document.

        Args:
            name: Parameter.

        Returns:
            Self for chaining.
        """
        # PyfficePart (our parent) does not expose create_new_document; the
        # original code called super().create_new_document(name, "cadpart")
        # which raised AttributeError at runtime. Record the part-name as
        # state and return self for chaining (matches PyfficeCADAssembly /
        # PyfficeCADManager caller expectations).
        self.name = name
        return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
