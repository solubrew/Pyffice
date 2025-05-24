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

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeFileSystem")).override(cfg)
        self.directories = None
        self.files = None
        self.doc_type = "files"

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

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_directories(document.get("directories", []))
        self.set_files(document.get("files", []))
        return self

    def set_directories(self, directories):
        """"""
        if directories != self.directories:
            self.add_change("directories", self.directories, directories)
            self.directories = directories
        return self

    def set_files(self, files):
        """"""
        if files != self.files:
            self.add_change("files", self.files, files)
            self.files = files
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = {"directories": self.directories, "files": self.files}
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
