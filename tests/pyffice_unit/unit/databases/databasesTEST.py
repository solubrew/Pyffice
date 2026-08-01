"""Tests for pyffice/databases/.

Coverage:
- PyfficeDatabaseManager construction (defaults, cfg)
- PyfficeDatabaseManager inheritance from PyfficeDocumentManager
- SERIALIZATION_VERSION tuple
- add_connection, add_database, create_database methods
- get_tables / get_indexes return [] for non-db entries
- PyfficeDatabaseConnection construction (requires a path)
- PyfficeDatabaseConnection.open_file with sqlite
"""

import os
import sqlite3
import tempfile

import pytest

from pyffice.databases.databases import (
    PyfficeDatabaseConnection,
    PyfficeDatabaseManager,
)


class TestPyfficeDatabaseManagerConstruction:
    """PyfficeDatabaseManager() constructs with empty collections."""

    def test_constructs_no_args(self):
        m = PyfficeDatabaseManager()
        assert m is not None
        assert m.databases == {}
        assert m.connections == {}

    def test_constructs_with_cfg(self):
        m = PyfficeDatabaseManager({"key": "value"})
        assert m is not None


class TestPyfficeDatabaseManagerInheritance:
    """PyfficeDatabaseManager extends PyfficeDocumentManager."""

    def test_inherits_document_manager(self):
        from pyffice.document import PyfficeDocumentManager
        assert issubclass(PyfficeDatabaseManager, PyfficeDocumentManager)


class TestPyfficeDatabaseManagerVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_serialization_version_tuple(self):
        assert hasattr(PyfficeDatabaseManager, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeDatabaseManager.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeDatabaseManager.SERIALIZATION_VERSION) == 3


class TestPyfficeDatabaseManagerMethods:
    """add_connection / add_database / create_database are fluent."""

    def test_add_connection_returns_self(self):
        m = PyfficeDatabaseManager()
        conn = object()
        assert m.add_connection("main", conn) is m
        assert m.connections["main"] is conn

    def test_add_database_returns_self(self):
        m = PyfficeDatabaseManager()
        assert m.add_database("logs", "db1") is m
        assert m.databases["logs"] == "db1"

    def test_create_database_returns_self(self):
        m = PyfficeDatabaseManager()
        assert m.create_database("new", "srv", "dbname") is m
        assert m.databases["new"] == {"server": "srv", "database": "dbname"}

    def test_add_server_returns_self(self):
        m = PyfficeDatabaseManager()
        assert m.add_server("srv1", "config") is m
        assert m.servers["srv1"] == "config"

    def test_get_tables_empty_for_non_db(self):
        m = PyfficeDatabaseManager()
        m.add_database("x", "not_a_connection")
        assert m.get_tables("x") == []

    def test_get_indexes_empty_for_non_db(self):
        m = PyfficeDatabaseManager()
        m.add_database("x", "not_a_connection")
        assert m.get_indexes("x") == []

    def test_get_views_empty_for_non_db(self):
        m = PyfficeDatabaseManager()
        m.add_database("x", "not_a_connection")
        assert m.get_views("x") == []

    def test_get_table_out_of_range_returns_none(self):
        m = PyfficeDatabaseManager()
        assert m.get_table("x", 0) is None

    def test_get_table_negative_returns_none(self):
        m = PyfficeDatabaseManager()
        assert m.get_table("x", -1) is None


class TestPyfficeDatabaseConnectionConstruction:
    """PyfficeDatabaseConnection requires a path to construct."""

    @pytest.fixture
    def sqlite_path(self):
        f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        f.close()
        conn = sqlite3.connect(f.name)
        conn.execute("CREATE TABLE sample (id INTEGER)")
        conn.commit()
        conn.close()
        yield f.name
        os.unlink(f.name)

    def test_constructs_with_path(self, sqlite_path):
        c = PyfficeDatabaseConnection(sqlite_path)
        assert c is not None

    def test_open_file_with_str(self, sqlite_path):
        # PyfficeDatabaseConnection() (no path) raises in the base
        # sonql.Doc constructor, so we construct with a dummy path
        # then call open_file to open the real sqlite file.
        c = PyfficeDatabaseConnection(sqlite_path)
        result = c.open_file(sqlite_path)
        assert result is c
        assert hasattr(c, "database")
