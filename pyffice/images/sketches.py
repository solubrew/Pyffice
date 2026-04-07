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
from pyffice.items.layers import PyfficeLayer

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeSketch(PyfficeDocument):
    """A Sketch overlay custom components ontop of a standard image"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeSketch").override(cfg))
        self.canvas = None
        self.connections = None
        self.edges = None
        self.endpoints = None
        self.nodes = None
        self.layers = None
        self.lock = None

    def add_layer(self, layer):
        """"""
        cfg = {"layer": layer}
        layer = PyfficeLayer(cfg)
        self.add_change("layers", self.layers, layer, "add")
        self.layers[layer.name] = layer
        return self

    def del_layer(self, layer):
        """"""
        self.add_change("layers", self.layers, layer, "del")
        del self.layers[layer.name]
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_lock(document.get("lock", False))
        self.set_edges(document.get("edges", {}))
        self.set_endpoints(document.get("endpoints", {}))
        self.set_nodes(document.get("nodes", {}))
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        if self.connections is None:
            self.connections = {}
        if self.edges is None:
            self.edges = {}
        if self.endpoints is None:
            self.endpoints = {}
        if self.nodes is None:
            self.nodes = {}
        if self.layers is None:
            self.layers = {}
        doc["document"] = {
            "canvas": self.canvas,
            "edges": {x.did: x.to_dict() for x in self.edges},
            "layers": self.layers,
            "nodes": {x.did: x.to_dict() for x in self.nodes},
            "connections": {x.did: x.to_dict() for x in self.connections},
        }
        return doc

    def to_md(self):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
