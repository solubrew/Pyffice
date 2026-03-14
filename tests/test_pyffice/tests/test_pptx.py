"""Test PPTX document generation and import."""
import pytest
from pyffice.presentation import pptx as pptx_doc


def test_create_presentation():
    """Test PPTX document creation."""
    doc = pptx_doc.PyfficePPTX()
    doc.create_presentation()
    assert True


def test_add_slide():
    """Test slide addition."""
    doc = pptx_doc.PyfficePPTX()
    doc.add_slide()
    assert True
