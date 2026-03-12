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
from condor import condor
from ogma.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.ports.cadports import get_ports_manager, import_cad, export_cad, convert_cad

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "cad.yaml")


class PyfficeCADAssembly(PyfficeDocumentManager):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeCADAssembly")
        super().__init__(self.config)
        self.config.override(cfg)

    def add_document(self, document):
        """"""
        super().add_document(document)

    def create_new_document(self, name, type_=None):
        """"""
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

    def add_part(self, part, position=None):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeCADManager(PyfficeDocumentManager):
    """Manage all cad related items inlcuding assmeblys, objects, libraries, etc"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeCADManager")
        super().__init__(self)
        self.config.override(cfg)

    def add_document(self, document):
        """"""
        super().add_document(document)

    def add_part(self, assembly):
        """"""

    def create_new_document(self, name, type_=None):
        """"""
        super().create_new_document(name, "manager")

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeCADPart(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).override("PyfficeCADPart")
        super().__init__(cfg)
        self.config.override(cfg)

    def create_new_document(self, name):
        """"""
        super().create_new_document(name, "cadpart")

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
