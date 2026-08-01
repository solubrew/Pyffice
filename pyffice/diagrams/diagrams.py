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
        """Add a endpoint.
        
        Args:
            position: Parameter.
            connection: Parameter.
            style: Parameter.
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
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
        """Add a text.
        
        Args:
            value: Parameter.
            postion: Parameter.
            size: Parameter.
            color: Parameter.
            style: Parameter.
        
        Returns:
            Self for chaining.
        """
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
        """Remove the endpoint.
        
        Args:
            endpoint: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("endpoints", self.endpoints, endpoint, "del")
        del self.endpoints[endpoint]
        return self

    def del_text(self, index):
        """Remove the text.
        
        Args:
            index: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("text", self.texts, index, "del")
        del self.texts[index]
        return self

    def load_unit(self, unit):
        """Load a unit dict into this document.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
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
        """Set the color.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"color": color}
        color = PyfficeColor(cfg)
        if color != self.color:
            self.add_change("color", self.color, color, "set")
            self.color = color
        return self

    def set_endpoints(self, endpoints):
        """Set the endpoints.
        
        Args:
            endpoints: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("endpoints", endpoints)

    def set_envelope_size(self, envelope_size=None):
        """Set the envelope size.
        
        Args:
            envelope_size: Parameter.
        
        Returns:
            Self for chaining.
        """
        if envelope_size != [self.width, self.height]:
            self.add_change("envelope_size", self.envelope_size, envelope_size, "set")
        if envelope_size is not None:
            self.width = envelope_size[0]
            self.height = envelope_size[1]
        return self

    def set_line_width(self, line_width):
        """Set the line width.
        
        Args:
            line_width: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("line_width", line_width)

    def set_lock(self, lock=True, absolute=True):
        """Set the lock.
        
        Args:
            lock: Parameter.
            absolute: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("lock", lock)

    def set_position(self, position):
        """Set the position.
        
        Args:
            position: Parameter.
        
        Returns:
            Self for chaining.
        """
        if self.lock:
            return self
        if position != self.position:
            self.add_change("position", self.position, position, "set")
        self.position = position
        return self

    def set_position_endpoint(self, endpoint, position):
        """Set the position endpoint.
        
        Args:
            endpoint: Parameter.
            position: Parameter.
        
        Returns:
            Self for chaining.
        """
        if position != self.endpoints[endpoint]["position"]:
            self.add_change("position", self.endpoints[endpoint]["position"], position, "set")
        self.endpoints[endpoint]["position"] = position
        return self

    def set_style(self, style):
        """Set the style.

        Args:
            style: Parameter.

        Returns:
            Self for chaining.
        """
        return self._set_with_change("style", style)

    def set_texts(self, texts):
        """Set the texts.
        
        Args:
            texts: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("texts", texts)

class PyfficeDiagram(PyfficeDocumentManager):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDiagram").override(cfg))

    def add_connection(self, connection):
        """Add a connection.
        
        Args:
            connection: Parameter.
        
        Returns:
            Self for chaining.
        """
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
        """Add a edge.
        
        Args:
            connections: Parameter.
            end: Parameter.
            start: Parameter.
            type: Parameter.
            version: Parameter.
            visible: Parameter.
            active: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {}
        edge = PyfficeEdge(cfg)
        self.add_layer(edge.did)
        self.edges[edge.did] = edge
        self.add_change("edges", self.edges, edge, "add")
        for endpoint in edge.endpoints:
            self.add_connection(connections[endpoint])
        return self

    def add_layer(self, layer):
        """Add a layer.
        
        Args:
            layer: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"layer": layer}
        layer = PyfficeDiagramLayer(cfg)
        self.add_change("layers", self.layers, layer, "add")
        self.layers[layer.name] = layer
        return self

    def add_node(self):
        """Add a node.
        
        Returns:
            Self for chaining.
        """
        cfg = {}
        node = PyfficeNode(cfg)
        self.add_change("nodes", self.nodes, node, "add")
        self.nodes[node.did] = node
        return self

    def del_connection(self, connection):
        """Remove the connection.
        
        Args:
            connection: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("connections", self.connections, connection, "del")
        del self.connections[connection.did]
        return self

    def del_edge(self, edge):
        """Remove the edge.
        
        Args:
            edge: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("edges", self.edges, edge, "del")
        del self.edges[edge.did]
        return self

    def del_layer(self, layer):
        """Remove the layer.

        Args:
            layer: Parameter.

        Returns:
            Self for chaining.
        """
        return self._del_from_dict("layers", layer.name, "layers")

    def del_node(self, node):
        """Remove the node.
        
        Args:
            node: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("nodes", self.nodes, node, "del")
        del self.nodes[node.did]
        return self

    def set_lock(self, lock):
        """Set the lock.
        
        Args:
            lock: Parameter.
        
        Returns:
            Self for chaining.
        """
        if lock != self.lock:
            self.add_change("lock", self.lock, lock)
        return self

    def set_edge_position(self, edge, position, maintain_connection=True):
        """Set the edge position.
        
        Args:
            edge: Parameter.
            position: Parameter.
            maintain_connection: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.edges[edge].set_position(position)
        if maintain_connection:
            for connection in self.connections.values():
                connection.set_position(position)
        return self

    def set_edges(self, edges):
        """Set the edges.
        
        Args:
            edges: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("edges", edges)

    def set_endpoint_position(self, endpoint, position, maintain_connection=True):
        """Set the endpoint position.
        
        Args:
            endpoint: Parameter.
            position: Parameter.
            maintain_connection: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.endpoints[endpoint].set_position(position)
        return self

    def set_endpoints(self, endpoints):
        """Set the endpoints.
        
        Args:
            endpoints: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("endpoints", endpoints)

    def set_node_position(self, node, position, maintain_connections=True):
        """Set the node position.
        
        Args:
            node: Parameter.
            position: Parameter.
            maintain_connections: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.nodes[node].set_position(position)
        if maintain_connections:
            for connection in self.connections.values():
                connection.set_position(position)
        return self

    def set_nodes(self, nodes):
        """Set the nodes.
        
        Args:
            nodes: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("nodes", nodes)

    def to_dict(self):
        """Convert to dictionary."""
        return {"name": getattr(self, 'name', None),
                "type": getattr(self, 'type', None)}

    def to_md(self):
        """Convert to markdown."""
        return ""


class PyfficeDiagramLayer(PyfficeUnit):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDiagramLayer")).override(cfg)
        self.objects = None

    def load_unit(self, unit):
        """Load a unit dict into this document.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        if unit is None:
            unit = {}
        super().load_unit(unit)
        self.set_objects(unit.get("objects", []))
        return self

    def set_objects(self, objects):
        """Set the objects.
        
        Args:
            objects: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("objects", objects)

class PyfficeNode(PyfficeUnit):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

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
        """Remove the cell.
        
        Args:
            index: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("cells", self.cells, index, "del")
        del self.cells[index]
        return self

    def load_unit(self, unit):
        """Load a unit dict into this document.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        if unit is None:
            unit = {}
        super().load_unit(unit)
        self.set_cells(unit.get("cells", []))
        self.set_lock(unit.get("lock", True))
        self.set_position(unit.get("position", [0, 0]))
        return self

    def set_cells(self, cells):
        """Set the cells.
        
        Args:
            cells: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("cells", cells)

    def set_lock(self, lock=True):
        """Set the lock.
        
        Args:
            lock: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("lock", lock)

    def set_position(self, position):
        """Set the position.
        
        Args:
            position: Parameter.
        
        Returns:
            Self for chaining.
        """
        if self.lock:
            return self
        if position != self.position:
            self.add_change("position", self.position, position, "set")
        self.position = position
        return self

    def set_position_cell(self, cell, position):
        """Set the position cell.
        
        Args:
            cell: Parameter.
            position: Parameter.
        
        Returns:
            Self for chaining.
        """
        if position != self.cells[cell]["position"]:
            self.add_change("position", self.cells[cell]["position"], position, "set")
        self.cells[cell]["position"] = position
        return self

class PyfficeDiagramConnection(PyfficeUnit):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDiagramConnection")).override(cfg)
        self.endpoints = None
        self.lock = None
        self.position = None

    def connect(self, object_, endpoint):
        """Connect.
        
        Args:
            object_: Parameter.
            endpoint: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.endpoints.append(object_.connect(self, endpoint))
        return self

    def load_unit(self, unit):
        """Load a unit dict into this document.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        if unit is None:
            unit = {}
        super().load_unit(unit)
        self.set_endpoints(unit.get("endpoints", []))
        self.set_position(unit.get("position", [0, 0]))
        return self

    def set_lock(self, lock=True):
        """Set the lock.
        
        Args:
            lock: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.lock = lock
        return self

    def set_endpoints(self, endpoints):
        """Set the endpoints.
        
        Args:
            endpoints: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.endpoints = endpoints
        return self

    def set_position(self, position):
        """Set the position.
        
        Args:
            position: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.position = position
        return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
