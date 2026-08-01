"""Tests for pyffice/ports/csv_handler.py.

Migrated from pyffice/data/csv.py (T-NEW-069). Behavior is
preserved verbatim from the original module — the migration is
purely structural (no logic changes).
"""

import csv
import os
import tempfile

import pytest

from pyffice.ports.csv_handler import (
    PyfficeCSV,
    read,
    read_rows,
    write,
    write_rows,
    append,
    append_row,
)


class TestPyfficeCSVModuleFunctions:
    """The module-level CSV helpers (read, write, append, ...)."""

    def test_read_returns_list_of_dicts(self, tmp_path):
        p = tmp_path / "test.csv"
        p.write_text("name,age\nalice,30\nbob,25\n")
        result = read(str(p))
        assert len(result) == 2
        assert result[0]["name"] == "alice"
        assert result[0]["age"] == "30"

    def test_read_rows_returns_list_of_lists(self, tmp_path):
        p = tmp_path / "test.csv"
        p.write_text("a,b,c\n1,2,3\n4,5,6\n")
        result = read_rows(str(p))
        assert result == [["a", "b", "c"], ["1", "2", "3"], ["4", "5", "6"]]

    def test_write_creates_file_with_header(self, tmp_path):
        p = tmp_path / "test.csv"
        write(str(p), [{"name": "alice", "age": 30}])
        with open(p) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["name"] == "alice"
        assert rows[0]["age"] == "30"

    def test_write_empty_data_creates_no_file(self, tmp_path):
        p = tmp_path / "test.csv"
        write(str(p), [])
        assert not p.exists()

    def test_write_rows_writes_raw_rows(self, tmp_path):
        p = tmp_path / "test.csv"
        write_rows(str(p), [["a", "b"], ["1", "2"]])
        with open(p) as f:
            lines = f.read().strip().split("\n")
        assert lines == ["a,b", "1,2"]

    def test_append_writes_header_when_empty(self, tmp_path):
        p = tmp_path / "test.csv"
        append(str(p), {"name": "alice"})
        with open(p) as f:
            content = f.read()
        # Header + row
        assert "name" in content
        assert "alice" in content

    def test_append_no_header_when_exists(self, tmp_path):
        p = tmp_path / "test.csv"
        p.write_text("name\n")
        append(str(p), {"name": "alice"})
        with open(p) as f:
            content = f.read()
        # Header should appear only once
        assert content.count("name") == 1
        assert "alice" in content

    def test_append_row_writes_list(self, tmp_path):
        p = tmp_path / "test.csv"
        append_row(str(p), ["1", "2", "3"])
        with open(p) as f:
            content = f.read()
        assert "1,2,3" in content


class TestPyfficeCSVClass:
    """The PyfficeCSV class — load, save, append, filter, etc."""

    def test_constructs_with_no_args(self):
        h = PyfficeCSV()
        assert h.file_path is None
        assert h.headers == []
        assert h._data == []

    def test_constructs_with_path(self, tmp_path):
        p = tmp_path / "test.csv"
        h = PyfficeCSV(str(p))
        assert h.file_path == p

    def test_load_parses_csv(self, tmp_path):
        p = tmp_path / "test.csv"
        p.write_text("name,age\nalice,30\nbob,25\n")
        h = PyfficeCSV().load(str(p))
        assert h.headers == ["name", "age"]
        assert len(h._data) == 2
        assert h._data[0] == {"name": "alice", "age": "30"}

    def test_load_returns_self(self, tmp_path):
        p = tmp_path / "test.csv"
        p.write_text("a,b\n1,2\n")
        h = PyfficeCSV()
        assert h.load(str(p)) is h

    def test_save_writes_file(self, tmp_path):
        p = tmp_path / "test.csv"
        h = PyfficeCSV()
        h.headers = ["name", "age"]
        h._data = [{"name": "alice", "age": 30}]
        h.save(str(p))
        assert p.exists()
        with open(p) as f:
            content = f.read()
        assert "name,age" in content
        assert "alice" in content

    def test_save_raises_when_no_path(self):
        h = PyfficeCSV()
        h.headers = ["a"]
        h._data = [{"a": 1}]
        with pytest.raises(ValueError):
            h.save()

    def test_save_returns_self(self, tmp_path):
        p = tmp_path / "test.csv"
        h = PyfficeCSV()
        h.headers = ["a"]
        h._data = [{"a": 1}]
        assert h.save(str(p)) is h

    def test_read_returns_copy_of_data(self):
        h = PyfficeCSV()
        h._data = [{"a": 1}]
        result = h.read()
        assert result == [{"a": 1}]
        # Mutating result shouldn't affect internal state.
        result.append({"b": 2})
        assert h._data == [{"a": 1}]

    def test_rows_yields_in_order(self):
        h = PyfficeCSV()
        h._data = [{"a": 1}, {"a": 2}, {"a": 3}]
        rows = list(h.rows())
        assert rows == [{"a": 1}, {"a": 2}, {"a": 3}]

    def test_append_updates_data(self):
        h = PyfficeCSV()
        h.append({"name": "alice"})
        assert h._data == [{"name": "alice"}]
        assert h.headers == ["name"]

    def test_append_preserves_existing_headers(self):
        h = PyfficeCSV()
        h.headers = ["existing"]
        h.append({"existing": 1, "new": 2})
        assert h.headers == ["existing"]

    def test_extend_appends_multiple(self):
        h = PyfficeCSV()
        h.extend([{"a": 1}, {"a": 2}])
        assert len(h._data) == 2

    def test_extend_returns_self(self):
        h = PyfficeCSV()
        assert h.extend([{"a": 1}]) is h

    def test_filter(self):
        h = PyfficeCSV()
        h._data = [{"x": 1}, {"x": 2}, {"x": 3}]
        result = h.filter(lambda r: r["x"] > 1)
        assert result == [{"x": 2}, {"x": 3}]

    def test_select_columns(self):
        h = PyfficeCSV()
        h._data = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]
        result = h.select(["a", "c"])
        assert result == [{"a": 1, "c": 3}, {"a": 4, "c": 6}]

    def test_group_by(self):
        h = PyfficeCSV()
        h._data = [
            {"team": "A", "name": "alice"},
            {"team": "B", "name": "bob"},
            {"team": "A", "name": "carol"},
        ]
        result = h.group_by("team")
        assert result["A"] == [
            {"team": "A", "name": "alice"},
            {"team": "A", "name": "carol"},
        ]
        assert result["B"] == [{"team": "B", "name": "bob"}]

    def test_count(self):
        h = PyfficeCSV()
        h._data = [{"a": 1}, {"a": 2}, {"a": 3}]
        assert h.count() == 3

    def test_clear(self):
        h = PyfficeCSV()
        h._data = [{"a": 1}]
        h.clear()
        assert h._data == []

    def test_clear_returns_self(self):
        h = PyfficeCSV()
        h._data = [{"a": 1}]
        assert h.clear() is h


class TestPyfficeCSVDelimiter:
    """CSV delimiter support (default comma, but configurable)."""

    def test_custom_delimiter_tsv(self, tmp_path):
        p = tmp_path / "test.tsv"
        p.write_text("a\tb\tc\n1\t2\t3\n")
        result = read(str(p), delimiter="\t")
        assert result == [{"a": "1", "b": "2", "c": "3"}]

    def test_custom_delimiter_pipe(self, tmp_path):
        p = tmp_path / "test.psv"
        write(str(p), [{"a": 1, "b": 2}], delimiter="|")
        result = read(str(p), delimiter="|")
        assert result == [{"a": "1", "b": "2"}]
