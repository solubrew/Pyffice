"""Test RAW image format support."""
import pytest
from pyffice.media.raw import PyfficeRAW


def test_read_raw():
    """Test reading RAW image files."""
    raw = PyfficeRAW()
    assert raw is not None


def test_convert_raw():
    """Test converting RAW to other formats."""
    raw = PyfficeRAW()
    result = raw.to_jpeg("test.raw")
    assert result is not None
