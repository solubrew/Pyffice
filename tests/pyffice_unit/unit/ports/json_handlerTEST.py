from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/ports/json_handler.py.

Migrated from pyffice/data/json.py (T-NEW-069). The migration drops
the PyfficeDataMixin inheritance (the base class is being deleted
as dead code) and re-implements the two methods it contributed
(`get` and `set`) as plain helpers on the PyfficeJSON class.
"""

import json

import pytest

from pyffice.ports.json_handler import (
    PyfficeJSON,
    read,
    parse,
    write,
    to_string,
    create,
    add_child,
)


class TestPyfficeJSONModuleFunctions:
    """The module-level JSON helpers."""

    def test_read_returns_dict(self, tmp_path):
        logma.debug("TestPyfficeJSONModuleFunctions test class")
        p = tmp_path / "test.json"
        p.write_text('{"name": "alice", "age": 30}')
        result = read(str(p))
        assert result == {"name": "alice", "age": 30}

    def test_parse_returns_python_object(self):
        assert parse('{"a": 1}') == {"a": 1}
        assert parse('[1, 2, 3]') == [1, 2, 3]
        assert parse('"hello"') == "hello"

    def test_write_creates_file(self, tmp_path):
        p = tmp_path / "test.json"
        write(str(p), {"name": "alice"})
        content = p.read_text()
        assert '"name"' in content
        assert '"alice"' in content

    def test_to_string_returns_json(self):
        s = to_string({"a": 1})
        assert json.loads(s) == {"a": 1}

    def test_to_string_with_indent(self):
        s = to_string({"a": 1}, indent=4)
        assert json.loads(s) == {"a": 1}

    def test_create_empty(self):
        obj = create()
        assert obj._data is None

    def test_create_with_initial(self):
        obj = create({"a": 1})
        assert obj._data == {"a": 1}

    def test_add_child_mutates_parent(self):
        parent = {}
        result = add_child(parent, "key", "value")
        assert parent == {"key": "value"}
        assert result is parent


class TestPyfficeJSONClass:
    """The PyfficeJSON class — load, save, get, set."""

    def test_constructs_with_no_args(self):
        logma.debug("TestPyfficeJSONClass test class")
        j = PyfficeJSON()
        assert j.file_path is None
        assert j._data is None

    def test_constructs_with_path(self, tmp_path):
        p = tmp_path / "test.json"
        j = PyfficeJSON(str(p))
        assert j.file_path == p

    def test_load_parses_json(self, tmp_path):
        p = tmp_path / "test.json"
        p.write_text('{"name": "alice"}')
        j = PyfficeJSON().load(str(p))
        assert j._data == {"name": "alice"}

    def test_load_returns_self(self, tmp_path):
        p = tmp_path / "test.json"
        p.write_text("{}")
        j = PyfficeJSON()
        assert j.load(str(p)) is j

    def test_load_raises_when_no_path(self):
        j = PyfficeJSON()
        with pytest.raises(ValueError):
            j.load()

    def test_save_writes_file(self, tmp_path):
        p = tmp_path / "test.json"
        j = PyfficeJSON()
        j._data = {"name": "alice"}
        j.save(str(p))
        assert p.exists()
        with open(p) as f:
            assert json.load(f) == {"name": "alice"}

    def test_save_raises_when_no_path(self):
        j = PyfficeJSON()
        j._data = {"a": 1}
        with pytest.raises(ValueError):
            j.save()

    def test_save_returns_self(self, tmp_path):
        p = tmp_path / "test.json"
        j = PyfficeJSON()
        j._data = {"a": 1}
        assert j.save(str(p)) is j

    def test_to_string(self):
        j = PyfficeJSON()
        j._data = {"name": "alice"}
        assert json.loads(j.to_string()) == {"name": "alice"}

    def test_from_string(self):
        j = PyfficeJSON.from_string('{"name": "alice"}')
        assert j._data == {"name": "alice"}


class TestPyfficeJSONDottedAccess:
    """The get/set methods that replaced PyfficeDataMixin."""

    def test_get_simple_key(self):
        logma.debug("TestPyfficeJSONDottedAccess test class")
        j = PyfficeJSON()
        j._data = {"name": "alice"}
        assert j.get("name") == "alice"

    def test_get_dotted_key(self):
        j = PyfficeJSON()
        j._data = {"user": {"profile": {"name": "alice"}}}
        assert j.get("user.profile.name") == "alice"

    def test_get_missing_key_returns_default(self):
        j = PyfficeJSON()
        j._data = {"name": "alice"}
        assert j.get("missing") is None
        assert j.get("missing", "fallback") == "fallback"

    def test_get_on_none_data(self):
        j = PyfficeJSON()
        assert j.get("any.key") is None
        assert j.get("any.key", "default") == "default"

    def test_get_traverses_non_dict_returns_default(self):
        j = PyfficeJSON()
        j._data = {"user": "alice"}  # not a dict
        assert j.get("user.name", "default") == "default"

    def test_set_simple_key(self):
        j = PyfficeJSON()
        j.set("name", "alice")
        assert j._data == {"name": "alice"}

    def test_set_dotted_key_creates_intermediate(self):
        j = PyfficeJSON()
        j.set("user.profile.name", "alice")
        assert j._data == {"user": {"profile": {"name": "alice"}}}

    def test_set_on_none_data_initializes(self):
        j = PyfficeJSON()
        j.set("key", "value")
        assert j._data == {"key": "value"}

    def test_set_returns_self(self):
        j = PyfficeJSON()
        assert j.set("key", "value") is j
