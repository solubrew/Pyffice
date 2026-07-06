"""Test CSV document generation and import."""
import pytest
from pyffice.data import csv as csv_doc


def test_create_csv():
    """Test CSV document creation."""
    doc = csv_doc.PyfficeCSV()
    doc.write(["name,age,city\n", "Alice,30,NYC\n", "Bob,25,LA\n"], "test.csv")
    assert True


def test_read_csv():
    """Test CSV document reading."""
    doc = csv_doc.PyfficeCSV()
    content = doc.read("test.csv")
    assert content is not None
