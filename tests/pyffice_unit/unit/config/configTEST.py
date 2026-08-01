"""Tests for pyffice/config/."""

import pytest

from pyffice.config.config import PyfficeConfig, PyfficeTOML, PyfficeHelp
from pyffice.config.policies import PyfficePolicy
from pyffice.document import PyfficeDocument, PyfficeUnit


class TestPyfficeConfig:
    def test_constructs_with_no_args(self):
        c = PyfficeConfig()
        assert c is not None

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeConfig, PyfficeDocument)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeConfig.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeConfig.SERIALIZATION_VERSION) == 3


class TestPyfficeTOML:
    def test_constructs_with_no_args(self):
        t = PyfficeTOML()
        assert t is not None

    def test_inherits_pyffice_config(self):
        assert issubclass(PyfficeTOML, PyfficeConfig)


class TestPyfficeHelp:
    def test_constructs_with_no_args(self):
        h = PyfficeHelp()
        assert h is not None

    def test_inherits_pyffice_config(self):
        assert issubclass(PyfficeHelp, PyfficeConfig)


class TestPyfficePolicy:
    def test_constructs_with_no_args(self):
        p = PyfficePolicy()
        assert p is not None

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficePolicy, PyfficeUnit)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficePolicy.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePolicy.SERIALIZATION_VERSION) == 3
