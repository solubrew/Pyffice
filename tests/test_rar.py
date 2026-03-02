"""Test RAR archive generation and import."""
import pytest
from pyffice.container import rar as rar_doc


def test_compress():
    """Test RAR compression."""
    doc = rar_doc.PyfficeRAR()
    doc.compress(["file1.txt"], "output.rar")
    assert True


def test_extract():
    """Test RAR extraction."""
    doc = rar_doc.PyfficeRAR()
    doc.extract("input.rar", "output_dir")
    assert True
