"""Test YAML document generation and import."""
import pytest
from pyffice.data import yaml as yaml_doc


def test_create_yaml():
    """Test YAML document creation."""
    doc = yaml_doc.PyfficeYAML()
    doc.write({"key": "value", "list": [1, 2, 3]}, "test.yaml")
    assert True


def test_read_yaml():
    """Test YAML document reading."""
    doc = yaml_doc.PyfficeYAML()
    data = doc.read("test.yaml")
    assert data is not None
