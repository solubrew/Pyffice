"""Test presentation module."""
import pytest
from pyffice.presentation.presentation import PyfficePresentation


def test_create():
    """Test creating a presentation."""
    ppt = PyfficePresentation()
    assert ppt is not None


def test_add_slide():
    """Test adding a slide."""
    ppt = PyfficePresentation()
    slide = ppt.add_slide()
    assert slide is not None


def test_save():
    """Test saving presentation."""
    ppt = PyfficePresentation()
    result = ppt.save("test.pptx")
    assert result is not None
