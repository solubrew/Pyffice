"""Unit tests for pyffice document functionality."""

import pytest
from pyffice.document import PyfficeDocument


class TestDocument:
    """Test cases for PyfficeDocument."""

    def test_document_initialization(self):
        """Test document initializes correctly."""
        doc = PyfficeDocument()
        assert doc is not None

    def test_document_content(self):
        """Test document has content attribute."""
        doc = PyfficeDocument()
        assert hasattr(doc, 'content')
