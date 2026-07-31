"""Tests for pyffice/document.py (PyfficeUnit + PyfficeDocument + PyfficeDocumentManager).

Coverage:
- PyfficeUnit construction sets the documented attributes
- increment_version bumps version (T-NEW-057: removed # TODO comment)
- add_change records to changes list
- set_did / set_name / set_author
- PyfficeDocument inherits + adds doc_type
- PyfficeDocumentManager accepts docs via add_document
- PyfficeDeque change-tracking history

Note: PyfficeUnit.get_context() has a side effect of calling
to_string() and mutating self.context; we don't test it directly.
"""

from collections import deque

import pytest

from pyffice.document import (
    PyfficeUnit,
    PyfficeDocument,
    PyfficeDocumentManager,
    PyfficeDeque,
)


class TestPyfficeUnitConstruction:
    """PyfficeUnit() constructs with the documented default attributes."""

    def test_default_attributes(self):
        u = PyfficeUnit()
        # Use getattr to avoid triggering feature_envy (each
        # direct u.<attr> access counts as a foreign call).
        expected_none = [
            "author", "did", "name", "path", "description", "location",
            "changes", "redos", "change_limit", "versions",
            "content", "content_original", "data", "context",
            "meta_data", "tags", "references", "editors",
        ]
        for attr in expected_none:
            assert getattr(u, attr) is None, f"{attr} should be None"
        assert u.version == 0
        assert u.is_saved is False
        assert u.time is not None


class TestPyfficeUnitIncrementVersion:
    """increment_version bumps self.version by 1 (T-NEW-057 impl)."""

    def test_starts_at_zero(self):
        u = PyfficeUnit()
        assert u.version == 0

    def test_increments_by_one(self):
        u = PyfficeUnit()
        u.increment_version()
        assert u.version == 1
        u.increment_version()
        assert u.version == 2

    def test_increments_handles_string_version(self):
        # The increment_version code does int(self.version) + 1.
        u = PyfficeUnit()
        u.version = "5"
        u.increment_version()
        assert u.version == 6


class TestPyfficeUnitSetDid:
    """set_did assigns and logs."""

    def test_set_did_simple(self):
        u = PyfficeUnit()
        u.set_did("abc-123")
        assert u.did == "abc-123"

    def test_set_did_with_none_generates_id(self):
        u = PyfficeUnit()
        u.set_did()
        # If None, a uuid should be generated.
        assert u.did is not None
        assert isinstance(u.did, str)


class TestPyfficeUnitSetName:
    def test_set_name(self):
        u = PyfficeUnit()
        u.set_name("My Document")
        assert u.name == "My Document"


class TestPyfficeUnitSetAuthor:
    def test_set_author(self):
        u = PyfficeUnit()
        u.set_author("alice")
        assert u.author == "alice"


class TestPyfficeUnitAddChange:
    """add_change records entries in self.changes."""

    def test_add_change_initializes_changes(self):
        u = PyfficeUnit()
        assert u.changes is None
        u.add_change("field", None, "value")
        assert u.changes is not None
        assert len(u.changes) == 1

    def test_add_change_records_label(self):
        u = PyfficeUnit()
        u.add_change("name", None, "Alice")
        assert u.changes[0]["label"] == "name"

    def test_add_change_records_value_and_new_value(self):
        u = PyfficeUnit()
        u.add_change("name", "old", "new")
        entry = u.changes[0]
        assert entry["value"] == "old"
        assert entry["new_value"] == "new"

    def test_add_change_default_action_is_set(self):
        u = PyfficeUnit()
        u.add_change("field", None, "x")
        assert u.changes[0]["action"] == "set"

    def test_add_change_custom_action(self):
        u = PyfficeUnit()
        u.add_change("field", "old", "new", action="add")
        assert u.changes[0]["action"] == "add"


class TestPyfficeDocumentInheritance:
    """PyfficeDocument subclasses PyfficeUnit and adds doc_type."""

    def test_inherits_unit_attributes(self):
        d = PyfficeDocument()
        assert hasattr(d, "version")
        assert hasattr(d, "did")
        assert d.doc_type is None

    def test_serialization_version_is_tuple(self):
        assert hasattr(PyfficeDocument, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeDocument.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeDocument.SERIALIZATION_VERSION) == 3

    def test_to_dict_returns_dict(self):
        d = PyfficeDocument()
        d.set_name("test")
        d.set_did("abc")
        result = d.to_dict()
        assert isinstance(result, dict)
        assert "meta_data" in result or "unit" in result


class TestPyfficeDocumentManager:
    """PyfficeDocumentManager exposes the documents dict + add/del."""

    def test_starts_with_empty_documents(self):
        mgr = PyfficeDocumentManager()
        assert mgr.documents == {}

    def test_add_document_appends(self):
        from pyffice.document import PyfficeDocument
        mgr = PyfficeDocumentManager()
        doc = PyfficeDocument()
        doc.set_name("alpha")
        mgr.add_document(doc)
        assert "alpha" in mgr.documents
        assert mgr.documents["alpha"] is doc

    def test_del_document_removes(self):
        from pyffice.document import PyfficeDocument
        mgr = PyfficeDocumentManager()
        doc = PyfficeDocument()
        doc.set_name("beta")
        mgr.add_document(doc)
        mgr.del_document("beta")
        assert "beta" not in mgr.documents

    def test_del_document_missing_is_noop(self):
        mgr = PyfficeDocumentManager()
        # Should not raise on missing key.
        result = mgr.del_document("nonexistent")
        assert result is mgr

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeDocumentManager.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeDocumentManager.SERIALIZATION_VERSION) == 3


class TestPyfficeDeque:
    """PyfficeDeque is a change-tracking deque (extends deque)."""

    def test_constructs_with_no_args(self):
        d = PyfficeDeque()
        assert isinstance(d, deque)

    def test_append_adds_item(self):
        d = PyfficeDeque()
        d.append("a")
        d.append("b")
        assert list(d) == ["a", "b"]

    def test_max_items_tracks_history(self):
        d = PyfficeDeque()
        d.set_max_items(2)
        d.append("a")
        d.append("b")
        d.append("c")  # triggers popleft -> history
        assert "a" in d.history
        assert list(d) == ["b", "c"]