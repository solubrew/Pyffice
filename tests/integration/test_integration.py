"""Integration tests for pyffice top-level package."""
import pytest


class TestPyfficeIntegration:
    """Integration tests for pyffice."""

    def test_import_pyffice(self):
        """pyffice imports cleanly and exposes a string version."""
        import pyffice
        assert pyffice.__version__ == "0.1.0"

    def test_pyffice_exposes_public_subpackages(self):
        """The top-level package re-exports PyfficeCodex via lazy proxy."""
        import pyffice
        # _LAZY_EXPORTS proxies the canonical facade; PyfficeCodex must resolve.
        assert pyffice.PyfficeCodex is not None
        assert pyffice.PyfficeCodexError is not None
