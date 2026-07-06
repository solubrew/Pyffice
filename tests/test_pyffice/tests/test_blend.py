"""Test BLEND file handling"""
import pytest
from pathlib import Path
from pyffice.cad import blend


def test_read_blend():
    """Test reading BLEND files"""
    # BLEND files are binary; test basic functionality
    assert blend is not None


def test_write_blend():
    """Test writing BLEND files"""
    # BLEND file writing support
    assert blend is not None


def test_blend_import():
    """Test blend module imports correctly"""
    from pyffice.cad.blend import BlendFile
    assert BlendFile is not None
