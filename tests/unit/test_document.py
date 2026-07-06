"""Unit tests for pyffice document functionality."""

import pytest


class TestDocument:
    """Test cases for PyfficeDocument."""

    def test_document_initialization(self):
        """Test document initializes correctly."""
        try:
            from pyffice.document import PyfficeDocument
            doc = PyfficeDocument()
            assert doc is not None
            assert hasattr(doc, 'did')
        except ImportError:
            pytest.skip("Missing pyffice dependencies")

    def test_document_set_name(self):
        """Test setting document name."""
        try:
            from pyffice.document import PyfficeDocument
            doc = PyfficeDocument()
            doc.set_name("Test Document")
            assert doc.name == "Test Document"
        except ImportError:
            pytest.skip("Missing pyffice dependencies")

    def test_document_version(self):
        """Test document version attribute."""
        try:
            from pyffice.document import PyfficeDocument
            doc = PyfficeDocument()
            assert hasattr(doc, 'version')
        except ImportError:
            pytest.skip("Missing pyffice dependencies")


class TestDiagrams:
    """Test cases for diagram functionality."""

    def test_diagram_formats_defined(self):
        """Test that diagram formats are defined."""
        try:
            from pyffice.diagrams.formats import DIAGRAM_FORMATS
            assert isinstance(DIAGRAM_FORMATS, dict)
            assert ".dia" in DIAGRAM_FORMATS
            assert ".dot" in DIAGRAM_FORMATS
        except ImportError:
            pytest.skip("Missing pyffice dependencies")

    def test_diagram_converter_exists(self):
        """Test diagram converter exists."""
        try:
            from pyffice.diagrams.formats import DiagramConverter
            assert DiagramConverter is not None
        except ImportError:
            pytest.skip("Missing pyffice dependencies")
