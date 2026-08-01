# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid:
    name:
    description: >
    version: 0.0.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt
import sqlite3

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from squirl.orgnql import sonql
from typing import Any
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeDatabaseConnection(sonql.Doc):
    """Manages database connections."""

    def __init__(self, path=None, cfg=None) -> None:
        """Initialize the database connection."""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeDatabaseConnection")
        super().__init__(path)
        self.config.override(cfg)

    def open_file(self, document) -> Self:
        """Open a database file."""
        if isinstance(document, str):
            import sqlite3

            conn = sqlite3.connect(document)
            self.database = conn
        return self

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "config" in content:
                setattr(self, "config", content["config"])
            if "database" in content:
                setattr(self, "database", content["database"])
        return self

    def save(self, path=None, format_=None, encrypt=None):
        logma.debug(f"{self.__class__.__name__}.save called path={path!r}")
        super().save(path, format_, encrypt)
        if path is None:
            path = self.file_path
        if not path:
            logma.warning(f"{self.__class__.__name__}.save: no path available")
            return
        import json as _json
        doc = self.to_dict()
        with open(path, "w") as f:
            _json.dump(doc, f, indent=2, default=str)
        return

    def to_dict(self):
        # TODO implement method
        super().to_dict()
        return self


class PyfficeDatabaseManager(PyfficeDocumentManager):
    """"""

    VERSION = "0.0.1.0.1.0"
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficeDatabaseManager.__init__ called")
        self.config = kahndor.Instruct(pxcfg).select("").override(cfg)
        self.databases = {}
        self.connections = {}

    def load_database(self, database) -> Any:
        """Load database into this document.

        Args:
            database: Parameter.

        Returns:
            Self for chaining.
        """
        self.databases[database] = self.notion.search_db(database)
        if self.databases[database] is not None and self.databases[database] != []:
            self.databases[database] = self.databases[database].item()
            return self.databases[database]
        return None

    def add_connection(self, name, connection) -> Self:
        """Add a database connection."""
        self.connections[name] = connection
        return self

    def add_server(self, name, server) -> Self:
        """Add a database server."""
        self.servers = getattr(self, "servers", {})
        self.servers[name] = server
        return self

    def add_database(self, name, database) -> Self:
        """Add a database."""
        self.databases[name] = database
        return self

    def create_database(self, name, server, database) -> Self:
        """Create a new database."""
        self.databases[name] = {"server": server, "database": database}
        return self

    def get_indexes(self, name) -> Any:
        """Get indexes for a database."""
        if name in self.databases and hasattr(self.databases[name], "execute"):
            try:
                cursor = self.databases[name].execute("SELECT name FROM sqlite_master WHERE type='index'")
                return [row[0] for row in cursor.fetchall()]
            except sqlite3.DatabaseError:
                pass
        return []

    def get_index(self, name, index) -> Any:
        """Get a specific index."""
        indexes = self.get_indexes(name)
        return indexes[index] if 0 <= index < len(indexes) else None

    def get_tables(self, name) -> Any:
        """Get tables for a database."""
        if name in self.databases and hasattr(self.databases[name], "execute"):
            try:
                cursor = self.databases[name].execute("SELECT name FROM sqlite_master WHERE type='table'")
                return [row[0] for row in cursor.fetchall()]
            except sqlite3.DatabaseError:
                pass
        return []

    def get_table(self, name, table) -> Any:
        """Get a specific table."""
        tables = self.get_tables(name)
        return tables[table] if 0 <= table < len(tables) else None

    def get_views(self, name) -> Any:
        """Get views for a database."""
        if name in self.databases and hasattr(self.databases[name], "execute"):
            try:
                cursor = self.databases[name].execute("SELECT name FROM sqlite_master WHERE type='view'")
                return [row[0] for row in cursor.fetchall()]
            except sqlite3.DatabaseError:
                pass
        return []

    def get_view(self, name, view) -> Any:
        """Get a specific view."""
        views = self.get_views(name)
        return views[view] if 0 <= view < len(views) else None

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "config" in content:
                setattr(self, "config", content["config"])
            if "databases" in content:
                setattr(self, "databases", content["databases"])
            if "connections" in content:
                setattr(self, "connections", content["connections"])
            if "servers" in content:
                setattr(self, "servers", content["servers"])
        return self

    def open_file(self, file_=None):
        import json as _json
        from os.path import exists
        if file_ is None:
            file_ = self.file_path
        if not file_ or not exists(file_):
            logma.warning(f"{self.__class__.__name__}.open_file: no such path {file_!r}")
            return self
        try:
            with open(file_, "r") as f:
                doc = _json.load(f)
        except (OSError, ValueError) as e:
            logma.warning(f"{self.__class__.__name__}.open_file failed for {file_!r}: {e}")
            return self
        return self.load_document(doc)

    def save(self, path=None, format_=None, encrypt=None):
        logma.debug(f"{self.__class__.__name__}.save called path={path!r}")
        super().save(path, format_, encrypt)
        if path is None:
            path = self.file_path
        if not path:
            logma.warning(f"{self.__class__.__name__}.save: no path available")
            return
        import json as _json
        doc = self.to_dict()
        with open(path, "w") as f:
            _json.dump(doc, f, indent=2, default=str)
        return

    def to_dict(self):
        # TODO implement method
        super().to_dict()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
