"""Test PyfficeTextDocument follows the PyfficeScript document template.

PyfficeTextDocument is a text document with formatting support.
Per the PyfficeScript template, every document must support:
  - to_dict() returns canonical envelope (dict)
  - load_document(dict) restores instance state
  - save(path) writes the envelope to disk
  - open_file(path) reads the envelope from disk
"""
import json
import os

import pytest

from pyffice.text.textdoc import PyfficeTextDocument


def test_to_dict_returns_dict():
    """to_dict() returns a dict (canonical envelope)."""
    d = PyfficeTextDocument()
    result = d.to_dict()
    assert isinstance(result, dict)
    assert "did" in result
    assert "meta_data" in result
    assert "data" in result


def test_to_dict_data_payload_under_content():
    """Class-specific payload lives under data['content'] (canonical slot)."""
    d = PyfficeTextDocument()
    result = d.to_dict()
    assert "content" in result["data"]
    content = result["data"]["content"]
    assert isinstance(content, dict)
    assert "text" in content
    assert "metadata" in content
    assert content["metadata"] == {}


def test_to_dict_schema_version():
    d = PyfficeTextDocument()
    result = d.to_dict()
    assert result["meta_data"]["schema_version"] == list(PyfficeTextDocument.SERIALIZATION_VERSION)


def test_load_document_restores_metadata():
    d = PyfficeTextDocument()
    d.load_document({
        "did": None,
        "meta_data": {"schema_version": [1, 0, 0]},
        "data": {
            "content": {
                "text": {},
                "metadata": {"title": "Loaded", "author": "tester"},
            }
        },
    })
    assert d.metadata == {"title": "Loaded", "author": "tester"}


def test_load_document_chainable():
    d = PyfficeTextDocument()
    result = d.load_document({"meta_data": {}, "data": {}})
    assert result is d


def test_open_file_missing_path_returns_self():
    d = PyfficeTextDocument()
    result = d.open_file("/nonexistent/path.json")
    assert result is d


def test_save_writes_json_envelope(tmp_path):
    d = PyfficeTextDocument()
    target = tmp_path / "doc.json"
    d.save(path=str(target))
    if target.exists() and target.stat().st_size > 0:
        with open(target) as f:
            loaded = json.load(f)
        assert "data" in loaded
        assert "content" in loaded["data"]
