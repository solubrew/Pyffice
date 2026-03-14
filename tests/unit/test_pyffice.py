"""Unit tests for pyffice core functionality."""
import pytest

from pyffice import __version__, validate_config, convert_document


class TestPyfficeCore:
    """Test core pyffice functions."""

    def test_version(self):
        """Test version is defined."""
        assert __version__ == "0.1.0"

    def test_validate_config_returns_bool(self):
        """Test validate_config returns a boolean."""
        result = validate_config("test.yaml")
        assert isinstance(result, bool)

    def test_convert_document_returns_bool(self):
        """Test convert_document returns a boolean."""
        result = convert_document("input.docx", "output.pdf", "pdf")
        assert isinstance(result, bool)
