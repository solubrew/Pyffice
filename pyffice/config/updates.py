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
from copy import deepcopy

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "updates.yaml")


class PyfficeUpdate(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeUpdate").override(cfg)
        self.document = None

    def create_temp_file(self):
        """"""
        return

    def process(self):
        """"""

        document = self.config.dikt.get("document", {})
        return document


class PyfficeUnitUpdate(PyfficeUpdate):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("")).override(cfg)

    def create_temp_unit(self):
        """"""


class PyfficeDocumentUpdate(PyfficeUpdate):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("")).override(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeDocumentUpdate")).override(cfg)
        self.data = None
        self.meta_data = None

    def create_temp_document(self):
        """"""

    def process(self, document=None):
        """"""
        if document is None:
            document = self.config.dikt.get("document", {})
        self.document = document
        self.data = deepcopy(document["data"])
        self.meta_data = deepcopy(document["meta_data"])
        document = self.rebuild()
        return document

    def rebuild(self):
        """"""
        document = self.document
        document["data"] = self.data
        document["meta_data"] = self.meta_data
        return document

    def run_adds(self, data):
        """"""

    def run_deletes(self, data):
        """"""

    def run_updates(self, data, chain=[]):
        """"""
        for update in data:
            if isinstance(data[update], dict):
                chain.append(update)
                self.run_updates(data[update], chain)
            elif isinstance(data[update], str):
                self.reset_item(data, update, chain)

    def reset_item(self, data, update, chain):
        if chain == []:
            self.data[data[update]] = self.data[update]
        else:
            for item in chain:
                self.reset_item(data[item], update, chain[1:])

    def update_data(self):
        """"""
        self.run_adds()
        self.run_deletes()
        self.run_updates()
        return self

    def update_document(self):
        """"""
        self.run_adds()
        self.run_deletes()
        self.run_updates()
        return self

    def update_meta_data(self):
        """"""
        self.run_adds()
        self.run_deletes()
        self.run_updates()
        return self

    def update_versions(self, version, document_type):
        """"""
        version = self.update_version_0_0_1_0_1_1(version, document_type)
        return version

    def update_version_0_0_1_0_1_1(self, version, document_type):
        """"""
        if version == "0.0.1.0.1.0":
            self.update_document()
            self.update_meta_data()
            self.update_data()
            if document_type == "browser":
                self.update_version_0_0_1_0_1_1_browser()
            elif document_type == "filesytem":
                self.update_version_0_0_1_0_1_1_filesystem()
            elif document_type == "image":
                self.update_version_0_0_1_0_1_1_image()
            elif document_type == "pdf":
                self.update_version_0_0_1_0_1_1_pdf()
            elif document_type == "prompt":
                self.update_version_0_0_1_0_1_1_prompt()
            elif document_type == "script":
                self.update_version_0_0_1_0_1_1_script()
            version = "0.0.1.0.1.1"
        return version

    def update_version_0_0_1_0_1_1_browser(self):
        """"""
        # add page
        # set url of page to external

    def update_version_0_0_1_0_1_1_filesystem(self):
        """"""

    def update_version_0_0_1_0_1_1_image(self):
        """"""

    def update_version_0_0_1_0_1_1_pdf(self):
        """"""

    def update_version_0_0_1_0_1_1_prompt(self):
        """"""

    def update_version_0_0_1_0_1_1_script(self):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
