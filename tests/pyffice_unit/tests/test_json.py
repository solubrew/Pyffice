"""Test JSON document generation and import."""
import pytest
from pyffice.data import json as json_doc


def test_create_json():
    """Test JSON document creation."""
    doc = json_doc.PyfficeJSON()
    doc.write({"name": "test", "value": 123}, "test.json")
    assert True


def test_read_json():
    """Test JSON document reading."""
    doc = json_doc.PyfficeJSON()
    data = doc.read("test.json")
    assert data is not None
