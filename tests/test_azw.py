"""Test AZW ebook generation and import."""
import pytest
from pyffice.ebook import azw as azw_doc


def test_create_azw():
    """Test AZW creation."""
    doc = azw_doc.PyfficeAZW()
    doc.create_azw("output.azw")
    assert True


def test_read_azw():
    """Test AZW reading."""
    doc = azw_doc.PyfficeAZW()
    doc.read_azw("input.azw")
    assert True
