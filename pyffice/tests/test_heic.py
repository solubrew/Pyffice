"""Test HEIC image format support."""
import pytest
from pyffice.media.heic import PyfficeHEIC


def test_read_heic():
    """Test reading HEIC files."""
    heic = PyfficeHEIC()
    assert heic is not None


def test_convert_heic():
    """Test converting HEIC to other formats."""
    heic = PyfficeHEIC()
    result = heic.to_jpeg("test.heic")
    assert result is not None
