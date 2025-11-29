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

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


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
        self.config.override(condor.Instruct(pxcfg).select("PyfficeUnitUpdate")).override(cfg)

    def create_temp_unit(self):
        """"""


class PyfficeDocumentUpdate(PyfficeUpdate):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeDocumentUpdate")).override(cfg)
        self.data = None
        self.meta_data = None

    def create_temp_document(self):
        """"""

    def process(self, document=None):
        """"""
        if document is None:
            document = self.config.dikt.get("document", {})
        if document == {}:
            return document
        self.document = document
        logma.info(f"Update Document {document}")
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

    def run_adds(self, data, type_):
        """"""
        if type_ == "data":
            for add in data:
                if isinstance(data[add], dict):
                    self.run_adds(data[add], type_)
                elif isinstance(data[add], str):
                    self.data[add] = self.data[data[add]]
        elif type_ == "meta_data":
            for add in data:
                if isinstance(data[add], dict):
                    self.run_adds(data[add], type_)
        elif type_ == "document":
            for add in data:
                if isinstance(data[add], dict):
                    self.run_adds(data[add], type_)
                elif isinstance(data[add], str):
                    self.data[add] = self.data[data[add]]
        else:
            raise Exception(f"Unknown type: {type_}")

    def run_deletes(self, data, type_):
        """"""
        if type_ == "data":
            for delete in data:
                if isinstance(data[delete], dict):
                    self.run_deletes(data[delete], type_)
                elif isinstance(data[delete], str):
                    del self.data[delete]
        elif type_ == "meta_data":
            for delete in data:
                if isinstance(data[delete], dict):
                    self.run_deletes(data[delete], type_)
        elif type_ == "document":
            for delete in data:
                if isinstance(data[delete], dict):
                    self.run_deletes(data[delete], type_)
                elif isinstance(data[delete], str):
                    del self.data[delete]
        else:
            raise Exception(f"Unknown type: {type_}")

    def run_updates(self, data, type_, chain=[]):
        """"""
        if type_ == "data":
            for update in data:
                if isinstance(data[update], dict):
                    chain.append(update)
                    self.run_updates(data[update], chain)
                elif isinstance(data[update], str):
                    self.reset_item(data, update, chain)
        elif type_ == "meta_data":
            for update in data:
                if isinstance(data[update], dict):
                    chain.append(update)
        elif type_ == "document":
            for update in data:
                if isinstance(data[update], dict):
                    chain.append(update)
                    self.run_updates(data[update], chain)
                elif isinstance(data[update], str):
                    self.reset_item(data, update, chain)
        else:
            raise Exception(f"Unknown type: {type_}")

    def reset_item(self, data, update, chain):
        if chain == []:
            self.data[data[update]] = self.data[update]
        else:
            for item in chain:
                self.reset_item(data[item], update, chain[1:])

    def update_data(self, update):
        """"""
        if update.get("add", None) is not None:
            self.run_adds(self.data, "data", update["add"])
        if update.get("delete", None) is not None:
            self.run_deletes(self.data, "data", update["delete"])
        if update.get("update", None) is not None:
            self.run_updates(self.data, "data", update["update"])
        return self

    def update_document(self, update):
        """"""
        if update.get("add", None) is not None:
            self.run_adds(self.data, "document", update["add"])
        if update.get("delete", None) is not None:
            self.run_deletes(self.data, "document", update["delete"])
        if update.get("update", None) is not None:
            self.run_updates(self.data, "document", update["update"])
        return self

    def update_meta_data(self, update):
        """"""
        if update.get("add", None) is not None:
            self.run_adds(self.data, "meta_data", update["add"])
        if update.get("delete", None) is not None:
            self.run_deletes(self.data, "meta_data", update["delete"])
        if update.get("update", None) is not None:
            self.run_updates(self.data, "meta_data", update["update"])
        return self

    def update_versions(self, version, document_type):
        """"""
        version = self.update_version_0_0_1_0_1_1(version, document_type)
        return version

    def update_version_0_0_1_0_1_1(self, version, document_type):
        """"""
        if version == "0.0.1.0.1.0":
            if document_type == "browser":
                updates = self.config.select("pyffice_browser").dikt[version]
                for update in updates:
                    self.update_document(updates[update]["document"])
                    self.update_meta_data(updates[update]["meta_data"])
                    self.update_data(updates[update]["data"])
                    self.update_version_0_0_1_0_1_1_browser()
            elif document_type == "filesystem":
                updates = self.config.select("pyffice_browser").dikt[version]
                for update in updates:
                    self.update_document(updates[update]["document"])
                    self.update_meta_data(updates[update]["meta_data"])
                    self.update_data(updates[update]["data"])
                self.update_version_0_0_1_0_1_1_filesystem()
            elif document_type == "image":
                updates = self.config.select("pyffice_browser").dikt[version]
                for update in updates:
                    self.update_document(updates[update]["document"])
                    self.update_meta_data(updates[update]["meta_data"])
                    self.update_data(updates[update]["data"])
                self.update_version_0_0_1_0_1_1_image()
            elif document_type == "pdf":
                updates = self.config.select("pyffice_browser").dikt[version]
                for update in updates:
                    self.update_document(updates[update]["document"])
                    self.update_meta_data(updates[update]["meta_data"])
                    self.update_data(updates[update]["data"])
                self.update_version_0_0_1_0_1_1_pdf()
            elif document_type == "prompt":
                updates = self.config.select("pyffice_browser").dikt[version]
                for update in updates:
                    self.update_document(updates[update]["document"])
                    self.update_meta_data(updates[update]["meta_data"])
                    self.update_data(updates[update]["data"])
                self.update_version_0_0_1_0_1_1_prompt()
            elif document_type == "script":
                updates = self.config.select("pyffice_browser").dikt[version]
                for update in updates:
                    self.update_document(updates[update]["document"])
                    self.update_meta_data(updates[update]["meta_data"])
                    self.update_data(updates[update]["data"])
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
