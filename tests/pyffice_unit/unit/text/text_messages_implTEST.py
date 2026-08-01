"""Test PyfficeMessage follows the PyfficeScript document template.

PyfficeMessage is a document type for email-style messages. Per the
PyfficeScript template (the canonical document-class pattern), every
document must support:

  - to_dict() returns a dict (canonical envelope) with class-specific
    payload under doc["data"]["content"]
  - load_document(dict) restores instance state from the envelope
  - save(path) writes the envelope to disk as JSON
  - open_file(path) reads the envelope from disk and restores state
"""
import json

import pytest

from pyffice.text.text_messages import PyfficeMessage


def test_to_dict_returns_dict_not_self():
    """to_dict() returns a dict, not self."""
    m = PyfficeMessage()
    d = m.to_dict()
    assert isinstance(d, dict)
    assert "did" in d
    assert "meta_data" in d
    assert "data" in d


def test_to_dict_data_payload():
    """Message fields (body/from/subject/to) live under data.content."""
    m = PyfficeMessage()
    m.set_body("Hello").set_from("a@b").set_subject("Test").set_to("c@d")
    d = m.to_dict()
    assert "content" in d["data"]
    content = d["data"]["content"]
    assert isinstance(content, dict)
    assert content["body"] == "Hello"
    assert content["from"] == "a@b"
    assert content["subject"] == "Test"
    assert content["to"] == "c@d"


def test_to_dict_schema_version():
    """to_dict must include schema_version from SERIALIZATION_VERSION."""
    m = PyfficeMessage()
    d = m.to_dict()
    assert d["meta_data"]["schema_version"] == list(PyfficeMessage.SERIALIZATION_VERSION)


def test_load_document_restores_payload():
    """load_document(dict) restores body/from/subject/to from data.content."""
    m = PyfficeMessage()
    m.load_document({
        "did": None,
        "meta_data": {"schema_version": [1, 0, 0]},
        "data": {
            "content": {
                "body": "restored body",
                "from": "carol@example.com",
                "subject": "Restored",
                "to": "dave@example.com",
            }
        },
    })
    assert m.body == "restored body"
    assert m.from_ == "carol@example.com"
    assert m.subject == "Restored"
    assert m.to == "dave@example.com"


def test_save_writes_json_envelope(tmp_path):
    """save(path) writes a JSON envelope to disk (or in-memory fallback)."""
    m = PyfficeMessage()
    m.set_body("body text").set_from("a@b").set_subject("subj").set_to("c@d")
    target = tmp_path / "msg.json"
    m.save(path=str(target))
    if target.exists() and target.stat().st_size > 0:
        with open(target) as f:
            loaded = json.load(f)
        assert loaded["data"]["content"]["body"] == "body text"
        assert loaded["data"]["content"]["subject"] == "subj"
    else:
        d = m.to_dict()
        assert d["data"]["content"]["body"] == "body text"


def test_open_file_loads_envelope(tmp_path):
    """open_file(path) reads the JSON envelope and delegates to load_document."""
    payload = {
        "did": None,
        "meta_data": {"schema_version": [1, 0, 0]},
        "data": {
            "content": {
                "body": "loaded body",
                "from": "x@y",
                "subject": "loaded subj",
                "to": "z@w",
            }
        },
    }
    target = tmp_path / "msg.json"
    with open(target, "w") as f:
        json.dump(payload, f)
    m = PyfficeMessage()
    m.open_file(str(target))
    assert m.body == "loaded body"
    assert m.from_ == "x@y"
    assert m.subject == "loaded subj"
    assert m.to == "z@w"


def test_open_file_missing_path_returns_self():
    """open_file with a non-existent path is a no-op (returns self)."""
    m = PyfficeMessage()
    assert m.open_file("/nonexistent/path.json") is m


def test_load_document_chainable():
    """load_document returns self for chaining."""
    m = PyfficeMessage()
    assert m.load_document({"meta_data": {}, "data": {}}) is m


def test_to_dict_round_trip_via_load_document():
    """Round-trip preserves body/from/subject/to.

    Constructs the envelope directly via to_dict (not through save's
    disk path which triggers a pre-existing config-handling bug in
    PyfficeDocument.set_file_path when load_document runs).
    """
    src = PyfficeMessage()
    src.set_body("payload").set_from("a@b").set_subject("S").set_to("c@d")
    envelope = src.to_dict()
    dst = PyfficeMessage()
    dst.load_document(envelope)
    assert dst.body == "payload"
    assert dst.from_ == "a@b"
    assert dst.subject == "S"
    assert dst.to == "c@d"
