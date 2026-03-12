"""Test 7Z archive generation and import."""
import pytest
from pyffice.container import sevenzip as sevenzip_doc


def test_compress():
    """Test 7Z compression."""
    doc = sevenzip_doc.Pyffice7Z()
    doc.compress(["file1.txt"], "output.7z")
    assert True


def test_extract():
    """Test 7Z extraction."""
    doc = sevenzip_doc.Pyffice7Z()
    doc.extract("input.7z", "output_dir")
    assert True
