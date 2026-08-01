"""Tests for pyffice/analytics/sources.py.

Coverage:
- PyfficeSource construction (defaults, cfg dict)
- PyfficeSource inheritance (PyfficeDocumentManager)
- PyfficeSource SERIALIZATION_VERSION tuple
- PyfficeSource fluent setters: add_data_set, add_data_view,
  edit_data_set, edit_data_view, load_document
- PyfficeSourceManager construction + inheritance + SERIALIZATION_VERSION
- PyfficeSourceManager fluent setters: set_sources
- PyfficeDataSet construction + inheritance + SERIALIZATION_VERSION
- PyfficeDataView construction + inheritance + SERIALIZATION_VERSION
"""

import pytest

from pyffice.analytics.sources import (
    PyfficeSource,
    PyfficeSourceManager,
    PyfficeDataSet,
    PyfficeDataView,
)
from pyffice.document import PyfficeDocument, PyfficeDocumentManager


class TestPyfficeSourceConstruction:
    """PyfficeSource(cfg) constructs with default attributes."""

    def test_constructs_with_cfg(self):
        s = PyfficeSource({"name": "src1"})
        assert s is not None

    def test_default_data_sets_empty(self):
        s = PyfficeSource({"name": "src1"})
        assert s.data_sets == []

    def test_default_data_views_empty(self):
        s = PyfficeSource({"name": "src1"})
        assert s.data_views == []


class TestPyfficeSourceInheritance:
    """PyfficeSource subclasses PyfficeDocumentManager."""

    def test_subclasses_document_manager(self):
        assert issubclass(PyfficeSource, PyfficeDocumentManager)

    def test_subclasses_document(self):
        assert issubclass(PyfficeSource, PyfficeDocument)


class TestPyfficeSourceSerializationVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_is_tuple_of_len_3(self):
        assert isinstance(PyfficeSource.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeSource.SERIALIZATION_VERSION) == 3


class TestPyfficeSourceSetters:
    """Fluent setters return self for chaining."""

    def test_add_data_set_returns_self(self):
        s = PyfficeSource({"name": "src1"})
        assert s.add_data_set({"a": 1}) is s
        assert s.data_sets == [{"a": 1}]

    def test_add_data_view_returns_self(self):
        s = PyfficeSource({"name": "src1"})
        assert s.add_data_view({"b": 2}) is s
        assert s.data_views == [{"b": 2}]

    def test_edit_data_set_returns_self(self):
        s = PyfficeSource({"name": "src1"})
        assert s.edit_data_set([{"x": 9}]) is s
        assert s.data_sets == [{"x": 9}]

    def test_edit_data_view_returns_self(self):
        s = PyfficeSource({"name": "src1"})
        assert s.edit_data_view([{"y": 8}]) is s
        assert s.data_views == [{"y": 8}]

    def test_load_document_returns_self(self):
        s = PyfficeSource({"name": "src1"})
        assert s.load_document({}) is s


class TestPyfficeSourceManagerConstruction:
    """PyfficeSourceManager(cfg) constructs with default attributes."""

    def test_constructs_no_args(self):
        m = PyfficeSourceManager()
        assert m is not None

    def test_constructs_with_cfg(self):
        m = PyfficeSourceManager({"name": "mgr"})
        assert m is not None

    def test_default_sources_empty(self):
        m = PyfficeSourceManager()
        assert m.sources == []


class TestPyfficeSourceManagerInheritance:
    """PyfficeSourceManager subclasses PyfficeDocumentManager."""

    def test_subclasses_document_manager(self):
        assert issubclass(PyfficeSourceManager, PyfficeDocumentManager)


class TestPyfficeSourceManagerSerializationVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_is_tuple_of_len_3(self):
        assert isinstance(PyfficeSourceManager.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeSourceManager.SERIALIZATION_VERSION) == 3


class TestPyfficeSourceManagerSetters:
    """Fluent setters return self for chaining."""

    def test_set_sources_returns_self(self):
        m = PyfficeSourceManager()
        assert m.set_sources(["a", "b"]) is m
        assert m.sources == ["a", "b"]

    def test_set_sources_none_becomes_empty(self):
        m = PyfficeSourceManager()
        m.set_sources(None)
        assert m.sources == []

    def test_load_document_returns_self(self):
        m = PyfficeSourceManager()
        assert m.load_document({}) is m


class TestPyfficeDataSetConstruction:
    """PyfficeDataSet(cfg) constructs with default attributes."""

    def test_constructs_no_args(self):
        d = PyfficeDataSet()
        assert d is not None

    def test_constructs_with_cfg(self):
        d = PyfficeDataSet({"name": "ds"})
        assert d is not None

    def test_default_attributes(self):
        d = PyfficeDataSet()
        assert d.path is None
        assert d.sources is None
        assert d.relationships is None
        assert d.views == set()


class TestPyfficeDataSetInheritance:
    """PyfficeDataSet subclasses PyfficeDocument."""

    def test_subclasses_document(self):
        assert issubclass(PyfficeDataSet, PyfficeDocument)


class TestPyfficeDataSetSerializationVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_is_tuple_of_len_3(self):
        assert isinstance(PyfficeDataSet.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeDataSet.SERIALIZATION_VERSION) == 3


class TestPyfficeDataViewConstruction:
    """PyfficeDataView(cfg) constructs with default attributes."""

    def test_constructs_no_args(self):
        v = PyfficeDataView()
        assert v is not None

    def test_constructs_with_cfg(self):
        v = PyfficeDataView({"name": "view"})
        assert v is not None

    def test_default_attributes(self):
        v = PyfficeDataView()
        assert v.columns is None
        assert v.filters is None
        assert v.records is None
        assert v.summarizations is None
        assert v.type is None


class TestPyfficeDataViewInheritance:
    """PyfficeDataView subclasses PyfficeDocument."""

    def test_subclasses_document(self):
        assert issubclass(PyfficeDataView, PyfficeDocument)


class TestPyfficeDataViewSerializationVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_is_tuple_of_len_3(self):
        assert isinstance(PyfficeDataView.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeDataView.SERIALIZATION_VERSION) == 3
