"""Tests for pyffice/tags/.

Coverage:
- PyfficeTag construction (defaults, doc_type, setters)
- PyfficeTag setters: set_description, set_label, set_value
- PyfficeTag.load_tag populates from dict
- PyfficeRating extends PyfficeTag
- PyfficeReference extends PyfficeTag
- PyfficeTagsManager construction

Note: PyfficeTag.to_dict() was deleted in d9d4fa9 (T-NEW-067
cleanup) because it had no callers. The canonical-shape assertion
is therefore NOT applied here — PyfficeTag inherits from `object`,
not PyfficeUnit, so it never had the canonical envelope.
"""

import pytest

from pyffice.tags.tags import PyfficeTag
from pyffice.tags.ratings import PyfficeRating
from pyffice.tags.references import PyfficeReference
from pyffice.tags.manager import PyfficeTagsManager


class TestPyfficeTagConstruction:
    """PyfficeTag() constructs with default None attributes."""

    def test_default_attributes(self):
        t = PyfficeTag()
        assert t.description is None
        assert t.label is None
        assert t.value is None
        assert t.doc_type == "tags"

    def test_version_class_attr(self):
        assert hasattr(PyfficeTag, "VERSION")

    def test_constructs_with_cfg(self):
        t = PyfficeTag({"label": "x"})
        assert t is not None


class TestPyfficeTagSetters:
    """The set_X methods are fluent (return self)."""

    def test_set_description_returns_self(self):
        t = PyfficeTag()
        assert t.set_description("a tag") is t
        assert t.description == "a tag"

    def test_set_label_returns_self(self):
        t = PyfficeTag()
        assert t.set_label("alpha") is t
        assert t.label == "alpha"

    def test_set_value_returns_self(self):
        t = PyfficeTag()
        assert t.set_value(42) is t
        assert t.value == 42


class TestPyfficeTagLoadTag:
    """load_tag reads from a dict and applies set_X methods."""

    def test_load_tag_from_dict(self):
        t = PyfficeTag()
        t.load_tag({"label": "beta", "description": "the second", "value": "B"})
        assert t.label == "beta"
        assert t.description == "the second"
        assert t.value == "B"

    def test_load_tag_returns_self(self):
        t = PyfficeTag()
        assert t.load_tag({"label": "x"}) is t


class TestPyfficeRating:
    """PyfficeRating extends PyfficeTag — same construction contract."""

    def test_inherits_pyffice_tag(self):
        assert issubclass(PyfficeRating, PyfficeTag)

    def test_constructs(self):
        r = PyfficeRating()
        assert r is not None
        assert r.description is None
        assert r.label is None
        assert r.value is None

    def test_set_label_inherited(self):
        r = PyfficeRating()
        r.set_label("5-stars")
        assert r.label == "5-stars"

    def test_load_tag_inherited(self):
        r = PyfficeRating()
        r.load_tag({"label": "4-stars", "value": 4})
        assert r.label == "4-stars"
        assert r.value == 4


class TestPyfficeReference:
    """PyfficeReference extends PyfficeTag — same construction contract."""

    def test_inherits_pyffice_tag(self):
        assert issubclass(PyfficeReference, PyfficeTag)

    def test_constructs(self):
        ref = PyfficeReference()
        assert ref is not None
        assert ref.doc_type == "tags"

    def test_set_description_inherited(self):
        ref = PyfficeReference()
        ref.set_description("see also")
        assert ref.description == "see also"


class TestPyfficeTagsManager:
    """PyfficeTagsManager is the (PyfficeDocumentManager) facade."""

    def test_constructs(self):
        m = PyfficeTagsManager()
        assert m is not None

    def test_inherits_document_manager(self):
        from pyffice.document import PyfficeDocumentManager
        assert issubclass(PyfficeTagsManager, PyfficeDocumentManager)
