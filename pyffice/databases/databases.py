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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from squirl.orgnql import sonql

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeDatabaseConnection(sonql.Doc):
    """"""

    def __init__(self, path=None, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeDatabaseConnection")
        super().__init__(path)
        self.config.override(cfg)

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""


class PyfficeDatabaseManager(PyfficeDocumentManager):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("").override(cfg)
        self.databases = {}
        self.connections = {}

    def load_database(self, database):
        """"""
        self.databases[database] = self.notion.search_db(database)
        if self.databases[database] is not None and self.databases[database] != []:
            self.databases[database] = self.databases[database].item()
            return self.databases[database]
        return None

    def add_connection(self, name, connection):
        """"""
        return self

    def add_server(self, name, server):
        """"""
        return self

    def add_database(self, name, database):
        """"""
        return self

    def create_database(self, name, server, database):
        """"""
        return self

    def get_indexes(self, name):
        """"""
        return self

    def get_index(self, name, index):
        """"""
        return self

    def get_tables(self, name):
        """"""
        return self

    def get_table(self, name, table):
        """"""
        return self

    def get_views(self, name):
        """"""
        return self

    def get_view(self, name, view):
        """"""
        return self

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
