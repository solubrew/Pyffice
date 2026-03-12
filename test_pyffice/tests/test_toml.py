"""Test TOML document generation and import."""
import pytest
from pyffice.config import toml as toml_doc


def test_create_toml():
    """Test TOML document creation."""
    doc = toml_doc.PyfficeTOML()
    doc.write({"title": "Test"}, "test.toml")
    assert True


def test_read_toml():
    """Test TOML document reading."""
    doc = toml_doc.PyfficeTOML()
    data = doc.read("test.toml")
    assert data is not None
