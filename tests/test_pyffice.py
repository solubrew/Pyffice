"""Test pyffice package."""

import pytest


def test_package_import():
    """Test pyffice can be imported."""
    import pyffice

    assert pyffice.__version__


def test_validate_config():
    """Test config validation."""
    from pyffice import validate_config

    result = validate_config("pyffice.yaml")
    assert result is True


def test_convert_document():
    """Test document conversion."""
    from pyffice import convert_document

    result = convert_document("input.pdf", "output.pdf", "pdf")
    assert result is False  # File doesn't exist


def test_main_info():
    """Test main CLI info command."""
    from pyffice import main

    assert main(["info"]) == 0
