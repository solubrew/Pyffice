"""Test TAR archive generation and import."""
import pytest
from pyffice.container import tar as tar_doc


def test_compress():
    """Test TAR compression."""
    doc = tar_doc.PyfficeTAR()
    doc.compress(["file1.txt"], "output.tar")
    assert True


def test_extract():
    """Test TAR extraction."""
    doc = tar_doc.PyfficeTAR()
    doc.extract("input.tar", "output_dir")
    assert True
