"""Test ZIP archive generation and import."""
import pytest
from pyffice.container import zip as zip_doc


def test_compress():
    """Test ZIP compression."""
    doc = zip_doc.PyfficeZIP()
    doc.compress(["file1.txt", "file2.txt"], "output.zip")
    assert True


def test_extract():
    """Test ZIP extraction."""
    doc = zip_doc.PyfficeZIP()
    doc.extract("input.zip", "output_dir")
    assert True
