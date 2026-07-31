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

from click import style

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from subtrix.utilities import uuid
from pyffice.items.cells import PyfficeCell
from pyffice.document import PyfficeDocument, PyfficeDocumentManager, PyfficeUnit
from pyffice.items.colors import PyfficeColor
from pyffice.items.text import PyfficeText

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "_data_", "diagrams.yaml")


class PyfficeEdge(PyfficeUnit):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeEdge")).override(cfg)
        self.active = None
        self.endpoints = None
        self.envelope_size = None
        self.color = None
        self.line_width = None
        self.lock = None
        self.padding = None
        self.position = None
        self.height = None
        self.show_background = None
        self.style = None
        self.text = None
        self.texts = None
        self.type = None
        self.version = None
        self.visible = None
        self.width = None

    def add_endpoint(self, position, connection, style="solid", color="black"):
        """"""
        uid = uuid()
        cfg = {"color": color}
        color = PyfficeColor(cfg)
        endpoint = {
            "position": position,
            "connection": connection,
            "style": style,
            "color": color,
        }
        self.add_change("endpoints", self.endpoints, endpoint, "add")
        self.endpoints[uid] = endpoint
        return self

    def add_text(self, value, postion, size=12, color="black", style="courier-new"):
        """"""
        cfg = {
            "value": value,
            "position": postion,
            "size": size,
            "color": color,
            "style": style,
        }
        text = PyfficeText(cfg)
        if text != self.text:
            self.add_change("text", self.texts, text, "add")
        self.texts.append(text)
        return self

    def del_endpoint(self, endpoint):
        """"""
        self.add_change("endpoints", self.endpoints, endpoint, "del")
        del self.endpoints[endpoint]
        return self

    def del_text(self, index):
        """"""
        self.add_change("text", self.texts, index, "del")
        del self.texts[index]
        return self

    def load_unit(self, unit):
        """"""
        if unit is None:
            unit = {}
        super().load_unit(unit)
        self.set_color(unit.get("color", {}))
        self.set_endpoints(unit.get("endpoints", {}))
        self.set_envelope_size(unit.get("envelope_size", [10, 10]))
        self.set_line_width(unit.get("line_width", 1))
        self.set_lock(unit.get("lock", True))
        self.set_position(unit.get("position", [0, 0]))
        self.set_style(unit.get("style", "solid"))
        self.set_texts(unit.get("texts", []))
        return self

    def set_color(self, color):
        """"""
        cfg = {"color": color}
        color = PyfficeColor(cfg)
        if color != self.color:
            self.add_change("color", self.color, color, "set")
            self.color = color
        return self

    def set_endpoints(self, endpoints):
        """"""
        if endpoints != self.endpoints:
            self.add_change("endpoints", self.endpoints, endpoints, "set")
            self.endpoints = endpoints
        return self

    def set_envelope_size(self, envelope_size=None):
        """"""
        if envelope_size != [self.width, self.height]:
            self.add_change("envelope_size", self.envelope_size, envelope_size, "set")
        if envelope_size is not None:
            self.width = envelope_size[0]
            self.height = envelope_size[1]
        return self

    def set_line_width(self, line_width):
        """"""
        if line_width != self.line_width:
            self.add_change("line_width", self.line_width, line_width, "set")
        self.line_width = line_width
        return self

    def set_lock(self, lock=True, absolute=True):
        """"""
        if lock != self.lock:
            self.add_change("lock", self.lock, lock)
        self.lock = lock
        return self

    def set_position(self, position):
        """"""
        if self.lock:
            return self
        if position != self.position:
            self.add_change("position", self.position, position, "set")
        self.position = position
        return self

    def set_position_endpoint(self, endpoint, position):
        """"""
        if position != self.endpoints[endpoint]["position"]:
            self.add_change("position", self.endpoints[endpoint]["position"], position, "set")
        self.endpoints[endpoint]["position"] = position
        return self

    def set_style(self, style):
        """"""
        if style != self.style:
            self.add_change("style", self.style, style, "set")
        self.style = style
        return self

    def set_texts(self, texts):
        """"""
        if texts != self.texts:
            self.add_change("texts", self.texts, texts, "set")
        self.texts = texts
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"] = {
            "texts": [x.to_dict for x in self.texts],
            "endpoints": self.endpoints,
            "color": self.color.to_dict(),
            "lock": self.lock,
            "position": self.position,
            "size": self.envelope_size,
            "line_width": self.line_width,
            "style": style,
        }
        return doc


class PyfficeDiagram(PyfficeDocumentManager):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDiagram").override(cfg))

    def add_connection(self, connection):
        """"""
        cfg = {"connection": connection}
        connection = PyfficeDiagramConnection(cfg)
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
        layer = PyfficeDiagramLayer(cfg)
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

    def to_md(self):
        """"""
        return self


class PyfficeDiagramLayer(PyfficeUnit):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDiagramLayer")).override(cfg)
        self.objects = None

    def load_unit(self, unit):
        """"""
        if unit is None:
            unit = {}
        super().load_unit(unit)
        self.set_objects(unit.get("objects", []))
        return self

    def set_objects(self, objects):
        """"""
        if objects is None:
            objects = []
        if objects != self.objects:
            self.add_change("objects", self.objects, objects, "set")
            self.objects = objects
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"] = {"objects": [x.to_dict() for x in self.objects]}
        return doc


class PyfficeNode(PyfficeUnit):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeNode")).override(cfg)
        self.cells = None
        self.lock = None
        self.position = None

    def add_cell(self, object_=PyfficeCell, cfg=None, lock=True, position=[0, 0]):
        """The cell object is default to an individual pyffice cell but can be replaced with any PyfficeDocument"""
        if cfg is None:
            cfg = {"position": position, "lock": lock, "object": object_}
        cell = object_(cfg)
        self.add_change("cells", self.cells, cell, "add")
        self.cells.append(cell)
        return self

    def del_cell(self, index):
        """"""
        self.add_change("cells", self.cells, index, "del")
        del self.cells[index]
        return self

    def load_unit(self, unit):
        """"""
        if unit is None:
            unit = {}
        super().load_unit(unit)
        self.set_cells(unit.get("cells", []))
        self.set_lock(unit.get("lock", True))
        self.set_position(unit.get("position", [0, 0]))
        return self

    def set_cells(self, cells):
        """"""
        if cells != self.cells:
            self.add_change("cells", self.cells, cells, "set")
        self.cells = cells
        return self

    def set_lock(self, lock=True):
        """"""
        if lock != self.lock:
            self.add_change("lock", self.lock, lock)
        self.lock = lock
        return self

    def set_position(self, position):
        """"""
        if self.lock:
            return self
        if position != self.position:
            self.add_change("position", self.position, position, "set")
        self.position = position
        return self

    def set_position_cell(self, cell, position):
        """"""
        if position != self.cells[cell]["position"]:
            self.add_change("position", self.cells[cell]["position"], position, "set")
        self.cells[cell]["position"] = position
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"] = {
            "cells": [x.to_dict() for x in self.cells],
            "lock": self.lock,
            "position": self.position,
        }
        return doc


class PyfficeDiagramConnection(PyfficeUnit):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDiagramConnection")).override(cfg)
        self.endpoints = None
        self.lock = None
        self.position = None

    def connect(self, object_, endpoint):
        """"""
        self.endpoints.append(object_.connect(self, endpoint))
        return self

    def load_unit(self, unit):
        """"""
        if unit is None:
            unit = {}
        super().load_unit(unit)
        self.set_endpoints(unit.get("endpoints", []))
        self.set_position(unit.get("position", [0, 0]))
        return self

    def set_lock(self, lock=True):
        """"""
        self.lock = lock
        return self

    def set_endpoints(self, endpoints):
        """"""
        self.endpoints = endpoints
        return self

    def set_position(self, position):
        """"""
        self.position = position
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"] = {
            "endpoints": self.endpoints,
            "position": self.position,
            "lock": self.lock,
        }
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
