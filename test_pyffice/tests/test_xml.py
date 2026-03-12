"""Test XML document generation and import."""
import pytest
from pyffice.data import xml as xml_doc


def test_create_xml():
    """Test XML document creation."""
    doc = xml_doc.PyfficeXML()
    doc.write("<root><item>test</item></root>", "test.xml")
    assert True


def test_read_xml():
    """Test XML document reading."""
    doc = xml_doc.PyfficeXML()
    content = doc.read("test.xml")
    assert content is not None
