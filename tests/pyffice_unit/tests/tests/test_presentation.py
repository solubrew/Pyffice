"""Test PyfficePresentation — instantiation and canonical shape.

PyfficePresentation is a thin wrapper over PyfficeDocument with a SlideShow
config. It does not yet expose add_slide() / save() — those are TBD. Tests
assert only on what the class actually provides.
"""
import pytest

from pyffice.presentation.presentation import PyfficePresentation


def test_pyffice_presentation_instantiates():
    """PyfficePresentation() returns a non-None instance."""
    ppt = PyfficePresentation()
    assert ppt is not None
    assert hasattr(ppt, "config")


def test_pyffice_presentation_has_serialization_version():
    """Canonical PyfficeDocument subclass — carries a SERIALIZATION_VERSION tuple."""
    assert hasattr(PyfficePresentation, "SERIALIZATION_VERSION")
    version = PyfficePresentation.SERIALIZATION_VERSION
    assert isinstance(version, tuple)
    assert len(version) >= 2
    assert all(isinstance(part, int) for part in version)


def test_pyffice_presentation_cfg_override():
    """Passing a cfg to __init__ does not raise."""
    ppt = PyfficePresentation(cfg={"test": True})
    assert ppt is not None
    assert ppt.config is not None
