"""Test CAD file format support."""
import pytest
from pyffice.cad import cad as PyfficeCAD


def test_read_any():
    """Test reading any CAD format."""
    cad = PyfficeCAD.PyfficeCAD()
    assert cad is not None


def test_export_cad():
    """Test CAD format export."""
    cad = PyfficeCAD.PyfficeCAD()
    result = cad.to_obj("model")
    assert result is not None
