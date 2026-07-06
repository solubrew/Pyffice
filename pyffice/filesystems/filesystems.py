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
from os.path import abspath, dirname, exists, join, expanduser, isfile, isdir
from os import listdir
import datetime as dt
from pathlib import Path

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocumentManager
from squirl.orgnql import fonql

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "filesystems.yaml")


class PyfficeFileSystem(PyfficeDocumentManager):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeFileSystem")).override(cfg)
        self.directories = None
        self.files = None
        self.doc_type = "files"
        self.root = None
        self.location = None
        self.file_path = None
        self.content = None
        self.tree = None

    def add_directory(self, directory):
        """"""
        self.add_change("directories", self.directories, directory)
        self.directories.append(directory)
        return self

    def add_file(self, file_):
        """"""
        self.add_change("files", self.files, file_)
        self.files.append(file_)
        return self

    def add_root(self, root):
        """"""
        self.add_change("root", self.root, root)
        self.roots.append(root)
        return self

    def del_directory(self, index):
        """"""
        self.add_change("directories", self.directories, index, "del")
        self.directories.pop(index)
        return self

    def del_file(self, index):
        """"""
        self.add_change("files", self.files, index, "del")
        self.files.pop(index)
        return self

    def get_files(self):
        """"""

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        document["location"] = "external"
        super().load_document(document)
        self.set_tree(document.get("tree", {}))
        self.set_table(document.get("table", {}))
        return self

    def set_tree(self, tree):
        """"""
        self.set_root(tree.get("root", None))
        self.tree = tree.get("children", None)
        return self

    def set_table(self, table):
        """"""
        self.set_directories(table.get("directories", []))
        self.set_files(table.get("files", []))
        return self

    def open_file(self, file=None):
        """"""
        self.set_file_path(file)
        self.set_root(file)
        self.set_directories()
        self.set_files()
        return self

    def set_content(self, content):
        """"""
        if self.location is None:
            self.set_location(None)
        if self.location == "external":
            content = {"file_path": self.file_path}
        else:
            raise Exception(f"Unknown Location {self.location}")
        if content != self.content:
            self.add_change("content", self.content, content)
            self.content = content
        return self

    def set_directories(self, directories=[]):
        """"""
        if directories == []:
            logma.info(f"Root {self.root}")
            if self.root is None:
                self.set_root()
            if exists(self.root):
                directories = [x for x in listdir(self.root) if isdir(x)]
        if directories != self.directories:
            self.add_change("directories", self.directories, directories)
            self.directories = directories
        return self

    def set_files(self, files=[]):
        """"""
        if files == []:
            if exists(self.root):
                files = [x for x in listdir(self.root) if isfile(x)]
        if files != self.files:
            self.add_change("files", self.files, files)
            self.files = files
        return self

    def set_root(self, root=None):
        """"""
        if root is None:
            # root = join(expanduser("~"), "Documents")
            root = expanduser("~")
        root = str(root)
        if root != self.root:
            self.add_change("root", self.root, root)
            self.root = root
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["data"] = {
            "path": self.path,
            "tree": self.tree,
            "table": {
                "directories": self.directories,
                "files": self.files,
            },
        }
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
