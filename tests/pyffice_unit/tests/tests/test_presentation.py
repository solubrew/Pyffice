"""Test PyfficeSlide — instantiation and canonical shape.

PyfficeSlide is a thin wrapper over PyfficeDocument with a SlideShow
config. It does not yet expose add_slide() / save() — those are TBD.
Tests assert only on what the class actually provides.

Note: previously named PyfficePresentation; renamed to PyfficeSlide in
the upstream commit that added the slide document type. Test was
updated to track the rename.
"""
import pytest

from pyffice.presentation.presentation import PyfficeSlide


def test_pyffice_slide_instantiates():
    """PyfficeSlide() returns a non-None instance."""
    sld = PyfficeSlide()
    assert sld is not None
    assert hasattr(sld, "config")


def test_pyffice_slide_has_serialization_version():
    """Canonical PyfficeDocument subclass — carries a SERIALIZATION_VERSION tuple."""
    assert hasattr(PyfficeSlide, "SERIALIZATION_VERSION")
    version = PyfficeSlide.SERIALIZATION_VERSION
    assert isinstance(version, tuple)
    assert len(version) >= 2
    assert all(isinstance(part, int) for part in version)


def test_pyffice_slide_cfg_override():
    """Passing a cfg to __init__ does not raise."""
    sld = PyfficeSlide(cfg={"test": True})
    assert sld is not None
    assert sld.config is not None
