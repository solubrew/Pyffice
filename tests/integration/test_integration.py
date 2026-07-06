"""Integration tests for pyffice."""
import pytest


class TestPyfficeIntegration:
    """Integration tests for pyffice."""

    def test_import_pyffice(self):
        """Test pyffice can be imported."""
        import pyffice
        assert pyffice.__version__ == "0.1.0"

    def test_cli_entry_point(self):
        """Test CLI entry point works."""
        from pyffice import main
        result = main(["info"])
        assert result == 0
