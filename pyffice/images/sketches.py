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
        self.config.override(
            condor.Instruct(pxcfg).select("PyfficeSketch").override(cfg)
        )
        self.canvas = None
        self.connections = None
        self.edges = None
        self.endpoints = None
        self.nodes = None
        self.layers = None
        self.lock = None

    def add_connection(self, connection):
        """"""
        cfg = {"connection": connection}
        connection = PyfficeSketchConnection(cfg)
        self.add_change("connections", self.connections, connection, "add")
        self.connections[connection.did] = connection
        return self

    def add_edge(
        self,
        connections=None,
        end=None,
        start=None,
        type=None,
        version=None,
        visible=None,
        active=None,
    ):
        """"""
        cfg = {}
        edge = PyfficeEdge(cfg)
        self.add_layer(edge.did)
        self.edges[edge.did] = edge
        self.add_change("edges", self.edges, edge, "add")
        for endpoint in edge.endpoints:
            self.add_connection(connections[endpoint])
        return self

    def add_layer(self, layer):
        """"""
        cfg = {"layer": layer}
        layer = PyfficeLayer(cfg)
        self.add_change("layers", self.layers, layer, "add")
        self.layers[layer.name] = layer
        return self

    def add_node(self):
        """"""
        cfg = {}
        node = PyfficeNode(cfg)
        self.add_change("nodes", self.nodes, node, "add")
        self.nodes[node.did] = node
        return self

    def del_connection(self, connection):
        """"""
        self.add_change("connections", self.connections, connection, "del")
        del self.connections[connection.did]
        return self

    def del_edge(self, edge):
        """"""
        self.add_change("edges", self.edges, edge, "del")
        del self.edges[edge.did]
        return self

    def del_layer(self, layer):
        """"""
        self.add_change("layers", self.layers, layer, "del")
        del self.layers[layer.name]
        return self

    def del_node(self, node):
        """"""
        self.add_change("nodes", self.nodes, node, "del")
        del self.nodes[node.did]
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

    def set_lock(self, lock):
        """"""
        if lock != self.lock:
            self.add_change("lock", self.lock, lock)
        return self

    def set_edge_position(self, edge, position, maintain_connection=True):
        """"""
        self.edges[edge].set_position(position)
        if maintain_connection:
            for connection in self.connections.values():
                connection.set_position(position)
        return self

    def set_edges(self, edges):
        """"""
        if edges != self.edges:
            self.add_change("edges", self.edges, edges, "set")
        self.edges = edges
        return self

    def set_endpoint_position(self, endpoint, position, maintain_connection=True):
        """"""
        self.endpoints[endpoint].set_position(position)
        return self

    def set_endpoints(self, endpoints):
        """"""
        if endpoints != self.endpoints:
            self.add_change("endpoints", self.endpoints, endpoints)
            self.endpoints = endpoints
        return self

    def set_node_position(self, node, position, maintain_connections=True):
        """"""
        self.nodes[node].set_position(position)
        if maintain_connections:
            for connection in self.connections.values():
                connection.set_position(position)
        return self

    def set_nodes(self, nodes):
        """"""
        if nodes != self.nodes:
            self.add_change("nodes", self.nodes, nodes, "set")
            self.nodes = nodes
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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
