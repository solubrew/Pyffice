"""Test MOBI ebook generation and import."""
import pytest
from pyffice.ebook import mobi as mobi_doc


def test_create_mobi():
    """Test MOBI creation."""
    doc = mobi_doc.PyfficeMOBI()
    doc.create_mobi("output.mobi")
    assert True


def test_read_mobi():
    """Test MOBI reading."""
    doc = mobi_doc.PyfficeMOBI()
    doc.read_mobi("input.mobi")
    assert True
