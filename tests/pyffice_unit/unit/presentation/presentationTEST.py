"""Tests for pyffice/presentation/.

Note: previously tested PyfficePresentation; renamed to PyfficeSlide
in the upstream commit that added the slide document type. Tests
updated to track the rename.
"""
import pytest

from pyffice.presentation.presentation import PyfficeSlide
from pyffice.document import PyfficeDocument


class TestPyfficeSlideConstruction:
    def test_constructs_with_no_args(self):
        s = PyfficeSlide()
        assert s is not None

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeSlide, PyfficeDocument)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeSlide.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeSlide.SERIALIZATION_VERSION) == 3
