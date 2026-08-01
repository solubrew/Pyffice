"""Tests for pyffice/text/.

Coverage:
- PyfficeTextDocument construction (defaults, metadata, text attr)
- PyfficeTextDocument inheritance from PyfficeDocument
- SERIALIZATION_VERSION tuple
- __str__ returns plain text
- PyfficeMessage construction (defaults, cfg)
- PyfficeMessage setters: set_body, set_from, set_subject, set_to
- PyfficeMessage.to_dict canonical shape
"""

import pytest

from pyffice.document import PyfficeDocument
from pyffice.text.textdoc import PyfficeTextDocument
from pyffice.text.text_messages import PyfficeMessage


class TestPyfficeTextDocumentConstruction:
    """PyfficeTextDocument() constructs with a PyfficeText and empty metadata."""

    def test_constructs_no_args(self):
        td = PyfficeTextDocument()
        assert td is not None
        assert td.text is not None
        assert td.metadata == {}

    def test_text_is_pyffice_text(self):
        from pyffice.items.text import PyfficeText
        td = PyfficeTextDocument()
        assert isinstance(td.text, PyfficeText)

    def test_metadata_mutable_dict(self):
        td = PyfficeTextDocument()
        td.metadata["key"] = "value"
        assert td.metadata["key"] == "value"


class TestPyfficeTextDocumentInheritance:
    """PyfficeTextDocument extends PyfficeDocument."""

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeTextDocument, PyfficeDocument)


class TestPyfficeTextDocumentVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_serialization_version_tuple(self):
        assert hasattr(PyfficeTextDocument, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeTextDocument.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeTextDocument.SERIALIZATION_VERSION) == 3


class TestPyfficeTextDocumentStr:
    """__str__ returns the plain-text representation.

    xfail: PyfficeTextDocument.__str__ delegates to self.text.text,
    but PyfficeText has no ``.text`` attribute (its content lives
    under ``.value``). This is a source bug in textdoc.py:91 — marked
    xfail rather than fixing source (tests-only scope).
    """

    @pytest.mark.xfail(
        reason="PyfficeText has no .text attr; __str__ raises AttributeError (source bug)",
        strict=True,
    )
    def test_str_returns_text(self):
        td = PyfficeTextDocument()
        assert str(td) == td.text.text


class TestPyfficeMessageConstruction:
    """PyfficeMessage() constructs with defaults and accepts a cfg dict."""

    def test_constructs_no_args(self):
        m = PyfficeMessage()
        assert m is not None

    def test_constructs_with_cfg(self):
        m = PyfficeMessage({"body": "hello"})
        assert m is not None


class TestPyfficeMessageInheritance:
    """PyfficeMessage extends PyfficeDocument."""

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeMessage, PyfficeDocument)


class TestPyfficeMessageVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_serialization_version_tuple(self):
        assert hasattr(PyfficeMessage, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeMessage.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeMessage.SERIALIZATION_VERSION) == 3


class TestPyfficeMessageSetters:
    """The set_X methods are fluent (return self) and store values."""

    def test_set_body_returns_self(self):
        m = PyfficeMessage()
        assert m.set_body("hello") is m
        assert m.body == "hello"

    def test_set_from_returns_self(self):
        m = PyfficeMessage()
        assert m.set_from("alice") is m
        assert m.from_ == "alice"

    def test_set_subject_returns_self(self):
        m = PyfficeMessage()
        assert m.set_subject("greeting") is m
        assert m.subject == "greeting"

    def test_set_to_returns_self(self):
        m = PyfficeMessage()
        assert m.set_to("bob") is m
        assert m.to == "bob"

    def test_chained_setters(self):
        m = PyfficeMessage()
        m.set_body("hi").set_from("a").set_to("b").set_subject("s")
        assert m.body == "hi"
        assert m.from_ == "a"
        assert m.to == "b"
        assert m.subject == "s"


class TestPyfficeMessageToDict:
    """to_dict() produces the canonical additive shape."""

    def test_to_dict_keys(self):
        m = PyfficeMessage()
        d = m.to_dict()
        assert "did" in d
        assert "meta_data" in d
        assert "data" in d
        assert "pyffice_compat" in d

    def test_to_dict_data_payload(self):
        m = PyfficeMessage()
        m.set_body("hello").set_from("a").set_to("b").set_subject("s")
        d = m.to_dict()
        assert d["data"]["body"] == "hello"
        assert d["data"]["from"] == "a"
        assert d["data"]["to"] == "b"
        assert d["data"]["subject"] == "s"

    def test_to_dict_schema_version(self):
        m = PyfficeMessage()
        d = m.to_dict()
        assert d["meta_data"]["schema_version"] == list(PyfficeMessage.SERIALIZATION_VERSION)
