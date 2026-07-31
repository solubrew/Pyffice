"""Unit tests for pyffice core public surface.

T-NEW-048 (Option B). The previous version imported
`validate_config`, `convert_document`, and `main` from
`pyffice` — none of those names exist. The real public
surface (post T-NEW-043) is:

    import pyffice
    pyffice.__version__              # str, e.g. "0.1.0"
    pyffice.__version_info__         # tuple, e.g. (0, 1, 0)
    from pyffice import PyfficeCodex  # the main class
    from pyffice import (
        PyfficeCodexError, DocumentNotFoundError, InitializationError,
    )

These tests assert that surface is reachable.
"""

import pytest


def test_version_is_string():
    """Test __version__ is a dotted-decimal string."""
    import pyffice
    assert pyffice.__version__ == "0.1.0"
    assert isinstance(pyffice.__version__, str)


def test_version_info_is_3tuple():
    """Test __version_info__ is a 3-tuple of ints."""
    import pyffice
    assert pyffice.__version_info__ == (0, 1, 0)
    assert isinstance(pyffice.__version_info__, tuple)
    assert len(pyffice.__version_info__) == 3
    assert all(isinstance(p, int) for p in pyffice.__version_info__)


def test_version_string_matches_version_info():
    """Test __version__ is the dotted form of __version_info__."""
    import pyffice
    assert pyffice.__version__ == ".".join(
        str(p) for p in pyffice.__version_info__
    )


def test_pyffice_codex_importable_from_root():
    """Test PyfficeCodex is exposed at package root (T-NEW-043)."""
    from pyffice import PyfficeCodex
    assert PyfficeCodex.__name__ == "PyfficeCodex"


def test_exception_classes_importable_from_root():
    """Test the 3 exception classes are exposed at package root."""
    from pyffice import (
        PyfficeCodexError,
        DocumentNotFoundError,
        InitializationError,
    )
    assert issubclass(PyfficeCodexError, Exception)
    assert issubclass(DocumentNotFoundError, PyfficeCodexError)
    assert issubclass(InitializationError, PyfficeCodexError)


def test_pyffice_codex_constructs():
    """Test PyfficeCodex() can be instantiated."""
    from pyffice import PyfficeCodex
    codex = PyfficeCodex()
    assert codex is not None
    assert codex.config is not None