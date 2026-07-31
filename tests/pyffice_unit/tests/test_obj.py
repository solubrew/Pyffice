"""Test OBJ CAD file generation and import."""
import pytest
from pyffice.cad import obj as obj_doc


def test_read_obj():
    """Test OBJ reading."""
    doc = obj_doc.PyfficeOBJ()
    doc.read_obj("input.obj")
    assert True


def test_write_obj():
    """Test OBJ writing."""
    doc = obj_doc.PyfficeOBJ()
    doc.write_obj([], "output.obj")
    assert True
