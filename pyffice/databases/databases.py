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

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeDatabaseConnection(sonql.Doc):
    """Manages database connections."""

    def __init__(self, path=None, cfg=None):
        """Initialize the database connection."""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeDatabaseConnection")
        super().__init__(path)
        self.config.override(cfg)
    def open_file(self, document):
        """Open a database file."""
        if isinstance(document, str):
            import sqlite3
            conn = sqlite3.connect(document)
            self.database = conn
        return self


class PyfficeDatabaseManager(PyfficeDocumentManager):
    """"""

    VERSION = "0.0.1.0.1.0"
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
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

    def add_connection(self, name, connection) -> "PyfficeDatabaseManager":
        """Add a database connection."""
        self.connections[name] = connection
        return self

    def add_server(self, name, server) -> "PyfficeDatabaseManager":
        """Add a database server."""
        self.servers = getattr(self, 'servers', {})
        self.servers[name] = server
        return self

    def add_database(self, name, database) -> "PyfficeDatabaseManager":
        """Add a database."""
        self.databases[name] = database
        return self

    def create_database(self, name, server, database) -> "PyfficeDatabaseManager":
        """Create a new database."""
        self.databases[name] = {"server": server, "database": database}
        return self

    def get_indexes(self, name) -> list:
        """Get indexes for a database."""
        if name in self.databases and hasattr(self.databases[name], 'execute'):
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

    def get_tables(self, name) -> list:
        """Get tables for a database."""
        if name in self.databases and hasattr(self.databases[name], 'execute'):
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

    def get_views(self, name) -> list:
        """Get views for a database."""
        if name in self.databases and hasattr(self.databases[name], 'execute'):
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
# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
