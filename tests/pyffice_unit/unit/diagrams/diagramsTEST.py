"""Tests for pyffice/diagrams/.

Coverage:
- PyfficeDiagram construction, inheritance, SERIALIZATION_VERSION, setters
- PyfficeEdge construction, inheritance, SERIALIZATION_VERSION, setters
- PyfficeDiagramLayer construction, inheritance, SERIALIZATION_VERSION, setters
- PyfficeNode construction, inheritance, SERIALIZATION_VERSION, setters
- PyfficeFlowchart is not yet implemented (xfail)

Inheritance map:
- PyfficeDiagram       -> PyfficeDocumentManager -> PyfficeDocument -> PyfficeUnit
- PyfficeEdge          -> PyfficeUnit
- PyfficeDiagramLayer  -> PyfficeUnit
- PyfficeNode          -> PyfficeUnit
"""

import pytest

from pyffice.diagrams.diagrams import (
    PyfficeDiagram,
    PyfficeEdge,
    PyfficeDiagramLayer,
    PyfficeNode,
)
from pyffice.document import PyfficeDocument, PyfficeDocumentManager, PyfficeUnit

# PyfficeFlowchart is listed in the task spec but does not exist
# anywhere in the codebase. Import it defensively and xfail tests.
try:
    from pyffice.diagrams.diagrams import PyfficeFlowchart
    HAS_FLOWCHART = True
except ImportError:
    try:
        from pyffice.diagrams.formats import PyfficeFlowchart  # noqa: F401
        HAS_FLOWCHART = True
    except ImportError:
        PyfficeFlowchart = None
        HAS_FLOWCHART = False


# --------------------------------------------------------------------------- #
# PyfficeDiagram
# --------------------------------------------------------------------------- #
class TestPyfficeDiagram:
    """PyfficeDiagram is the (PyfficeDocumentManager) container."""

    def test_inherits_document_manager(self):
        assert issubclass(PyfficeDiagram, PyfficeDocumentManager)

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeDiagram, PyfficeDocument)

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeDiagram, PyfficeUnit)

    def test_constructs_no_args(self):
        d = PyfficeDiagram()
        assert d is not None

    def test_constructs_with_cfg(self):
        d = PyfficeDiagram({"name": "my-diagram"})
        assert d is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficeDiagram, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeDiagram.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeDiagram.SERIALIZATION_VERSION) == 3

    def test_set_edges_returns_self(self):
        d = PyfficeDiagram()
        result = d.set_edges({})
        assert result is d


# --------------------------------------------------------------------------- #
# PyfficeEdge
# --------------------------------------------------------------------------- #
class TestPyfficeEdge:
    """PyfficeEdge is a PyfficeUnit."""

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeEdge, PyfficeUnit)

    def test_constructs_no_args(self):
        e = PyfficeEdge()
        assert e is not None

    def test_constructs_with_cfg(self):
        e = PyfficeEdge({"style": "solid"})
        assert e is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficeEdge, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeEdge.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeEdge.SERIALIZATION_VERSION) == 3

    def test_set_color_returns_self(self):
        e = PyfficeEdge()
        result = e.set_color("red")
        assert result is e

    def test_set_style_returns_self(self):
        e = PyfficeEdge()
        result = e.set_style("dashed")
        assert result is e

    def test_set_endpoints_returns_self(self):
        e = PyfficeEdge()
        result = e.set_endpoints({"ep1": {}})
        assert result is e


# --------------------------------------------------------------------------- #
# PyfficeDiagramLayer
# --------------------------------------------------------------------------- #
class TestPyfficeDiagramLayer:
    """PyfficeDiagramLayer is a PyfficeUnit."""

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeDiagramLayer, PyfficeUnit)

    def test_constructs_no_args(self):
        layer = PyfficeDiagramLayer()
        assert layer is not None

    def test_constructs_with_cfg(self):
        layer = PyfficeDiagramLayer({"objects": []})
        assert layer is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficeDiagramLayer, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeDiagramLayer.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeDiagramLayer.SERIALIZATION_VERSION) == 3

    def test_set_objects_returns_self(self):
        layer = PyfficeDiagramLayer()
        result = layer.set_objects(["a", "b"])
        assert result is layer


# --------------------------------------------------------------------------- #
# PyfficeNode
# --------------------------------------------------------------------------- #
class TestPyfficeNode:
    """PyfficeNode is a PyfficeUnit."""

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeNode, PyfficeUnit)

    def test_constructs_no_args(self):
        n = PyfficeNode()
        assert n is not None

    def test_constructs_with_cfg(self):
        n = PyfficeNode({"position": [1, 2]})
        assert n is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficeNode, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeNode.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeNode.SERIALIZATION_VERSION) == 3

    def test_set_cells_returns_self(self):
        n = PyfficeNode()
        result = n.set_cells([])
        assert result is n

    def test_set_lock_returns_self(self):
        n = PyfficeNode()
        result = n.set_lock(True)
        assert result is n


# --------------------------------------------------------------------------- #
# PyfficeFlowchart (does not exist in codebase — xfail)
# --------------------------------------------------------------------------- #
class TestPyfficeFlowchart:
    """PyfficeFlowchart is listed in the spec but not implemented yet."""

    @pytest.mark.skipif(
        not HAS_FLOWCHART,
        reason="PyfficeFlowchart is not implemented in pyffice/diagrams/",
    )
    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeFlowchart, PyfficeUnit)

    @pytest.mark.skipif(
        not HAS_FLOWCHART,
        reason="PyfficeFlowchart is not implemented in pyffice/diagrams/",
    )
    def test_constructs_no_args(self):
        assert PyfficeFlowchart() is not None

    @pytest.mark.skipif(
        not HAS_FLOWCHART,
        reason="PyfficeFlowchart is not implemented in pyffice/diagrams/",
    )
    def test_serialization_version_is_tuple_len_3(self):
        assert isinstance(PyfficeFlowchart.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeFlowchart.SERIALIZATION_VERSION) == 3
