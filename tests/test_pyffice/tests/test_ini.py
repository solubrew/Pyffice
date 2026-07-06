"""Test INI document generation and import."""
import pytest
from pyffice.config import ini as ini_doc


def test_create_ini():
    """Test INI document creation."""
    doc = ini_doc.PyfficeINI()
    doc.write("[section1]\nkey1=value1\n", "test.ini")
    assert True


def test_read_ini():
    """Test INI document reading."""
    doc = ini_doc.PyfficeINI()
    data = doc.read("test.ini")
    assert data is not None
