"""Tests for pyffice/presentation/."""

import pytest

from pyffice.presentation.presentation import PyfficePresentation
from pyffice.document import PyfficeDocument


class TestPyfficePresentationConstruction:
    def test_constructs_with_no_args(self):
        p = PyfficePresentation()
        assert p is not None

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficePresentation, PyfficeDocument)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficePresentation.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePresentation.SERIALIZATION_VERSION) == 3
