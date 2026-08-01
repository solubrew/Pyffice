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
from pyffice.items.layers import PyfficeLayer

from typing import Any, Dict, List, Optional, Tuple, Union, Set, FrozenSet

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeSketch(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """A Sketch overlay custom components ontop of a standard image"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeSketch").override(cfg))
        self.canvas = None
        self.connections = None
        self.edges = None
        self.endpoints = None
        self.nodes = None
        self.layers = None
        self.lock = None

    def add_layer(self, layer) -> "PyfficeSketch":
        """Add a layer.
        
        Args:
            layer: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"layer": layer}
        layer = PyfficeLayer(cfg)
        self.add_change("layers", self.layers, layer, "add")
        self.layers[layer.name] = layer
        return self

    def del_layer(self, layer) -> Any:
        """Remove the layer.

        Args:
            layer: Parameter.

        Returns:
            Self for chaining.
        """
        return self._del_from_dict("layers", layer.name, "layers")

    def load_document(self, document=None) -> "PyfficeSketch":
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
        self.set_lock(document.get("lock", False))
        self.set_edges(document.get("edges", {}))
        self.set_endpoints(document.get("endpoints", {}))
        self.set_nodes(document.get("nodes", {}))
        return self

    def set_lock(self, lock) -> "PyfficeSketch":
        """Set lock state."""
        self.lock = lock
        return self

    def set_edges(self, edges) -> "PyfficeSketch":
        """Set edges."""
        self.edges = edges
        return self

    def set_endpoints(self, endpoints) -> "PyfficeSketch":
        """Set endpoints."""
        self.endpoints = endpoints
        return self

    def set_nodes(self, nodes) -> "PyfficeSketch":
        """Set nodes."""
        self.nodes = nodes
        return self
    def to_md(self) -> str:
        """Convert to Markdown."""
        # Placeholder - would generate markdown
        return ""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
