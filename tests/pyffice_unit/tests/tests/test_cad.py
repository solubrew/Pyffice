"""Test CAD file format support.

The cad module exposes:
- PyfficeCADAssembly(PyfficeDocumentManager) — assembly-level CAD
- PyfficeCADManager(PyfficeDocumentManager) — manager-level CAD
- PyfficeCADPart(PyfficePart) — single-part CAD

(There is no top-level 'PyfficeCAD' class — the canonical entry is
PyfficeCADPart, the part-level handler.)

Tests assert on real instantiated state, not on log lines.
"""
import pytest

from pyffice.cad import cad as PyfficeCAD


def test_module_exposes_cad_classes():
    """The cad module exposes PyfficeCADAssembly, PyfficeCADManager, PyfficeCADPart."""
    assert hasattr(PyfficeCAD, "PyfficeCADAssembly")
    assert hasattr(PyfficeCAD, "PyfficeCADManager")
    assert hasattr(PyfficeCAD, "PyfficeCADPart")


def test_pyffice_cad_part_instantiates():
    """PyfficeCADPart() returns an instance with the canonical shape."""
    part = PyfficeCAD.PyfficeCADPart()
    assert part is not None
    # PyfficeDocument-derived classes carry a 'changes' slot (may be None at init).
    assert hasattr(part, "changes")
    assert hasattr(part, "config")


def test_pyffice_cad_part_create_new_document():
    """create_new_document(name) registers the name and returns self for chaining."""
    part = PyfficeCAD.PyfficeCADPart()
    result = part.create_new_document("my_part")
    assert result is part  # chainable
    assert part.name == "my_part"


def test_pyffice_cad_manager_instantiates():
    """PyfficeCADManager() returns an instance."""
    mgr = PyfficeCAD.PyfficeCADManager()
    assert mgr is not None
    assert hasattr(mgr, "changes")
    assert hasattr(mgr, "config")
