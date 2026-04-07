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

    def check_schema(self, schema):
        """Returns True if the document matches the schema"""
        return True

    def check_extra(self):
        """Returns True if the document has extra fields not in the schema at the schema levels"""

    def check_missing(self):
        """Returns True if the document is missing fields not in the schema at the schema levels"""

    def create_temp_file(self):
        """"""
        return


class PyfficeUnitUpdate(PyfficeUpdate):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(pxcfg).select("PyfficeUnitUpdate").override(cfg)

    def check_schema(self, schema):
        """Returns True if the document matches the schema"""
        return True

    def check_extra(self):
        """Returns True if the document has extra fields not in the schema at the schema levels"""

    def check_missing(self):
        """Returns True if the document is missing fields not in the schema at the schema levels"""

    def create_temp_unit(self):
        """"""

    def get_version_schema(self, version):
        """Get the version schema for a given version."""


class PyfficeDocumentUpdate(PyfficeUpdate):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(pxcfg).select("PyfficeDocumentUpdate").override(cfg)
        self.data = None
        self.meta_data = None

    def check_schema(self, schema):
        """Returns True if the document matches the schema"""
        return True

    def check_extra(self):
        """Returns True if the document has extra fields not in the schema at the schema levels"""

    def check_missing(self):
        """Returns True if the document is missing fields not in the schema at the schema levels"""

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
        self.data = deepcopy(document.get("data", {}))
        self.meta_data = deepcopy(document.get("meta_data", {}))

        version = document.get("version")
        document_type = document.get("document_type")

        if version and document_type:
            new_version = self.update_versions(version, document_type)
            self.document["version"] = new_version

        document = self.rebuild()
        return document

    def rebuild(self):
        """"""
        document = self.document
        document["data"] = self.data
        document["meta_data"] = self.meta_data
        return document

    def run_adds(self, target, update_data):
        """"""
        if not update_data:
            return
        if isinstance(update_data, dict):
            for key, value in update_data.items():
                target[key] = value
        elif isinstance(update_data, list):
            for item in update_data:
                if isinstance(item, dict):
                    target.update(item)

    def run_deletes(self, target, update_data):
        """"""
        if not update_data:
            return
        if isinstance(update_data, dict):
            for key in update_data:
                if key in target:
                    del target[key]
        elif isinstance(update_data, list):
            for key in update_data:
                if key in target:
                    del target[key]
        elif isinstance(update_data, str):
            if update_data in target:
                del target[update_data]

    def run_updates(self, target, update_data):
        """"""
        if not update_data:
            return
        for key, value in update_data.items():
            if (
                isinstance(value, dict)
                and key in target
                and isinstance(target[key], dict)
            ):
                self.run_updates(target[key], value)
            else:
                # If value is a string and it matches another key in target,
                # it might be a rename/move operation based on original code intent
                if isinstance(value, str) and value in target:
                    target[key] = target.pop(value)
                elif isinstance(value, str) and value.startswith("RENAME:"):
                    old_key = value[7:]
                    if old_key in target:
                        target[key] = target.pop(old_key)
                else:
                    target[key] = value

    def update_data(self, update):
        """"""
        if update.get("add") is not None:
            self.run_adds(self.data, update["add"])
        if update.get("delete") is not None:
            self.run_deletes(self.data, update["delete"])
        if update.get("update") is not None:
            self.run_updates(self.data, update["update"])
        return self

    def update_document(self, update):
        """"""
        if update.get("add") is not None:
            self.run_adds(self.document, update["add"])
        if update.get("delete") is not None:
            self.run_deletes(self.document, update["delete"])
        if update.get("update") is not None:
            self.run_updates(self.document, update["update"])
        return self

    def update_meta_data(self, update):
        """"""
        if update.get("add") is not None:
            self.run_adds(self.meta_data, update["add"])
        if update.get("delete") is not None:
            self.run_deletes(self.meta_data, update["delete"])
        if update.get("update") is not None:
            self.run_updates(self.meta_data, update["update"])
        return self

    def update_versions(self, version, document_type):
        """"""
        # Map document_type to YAML keys if necessary
        # The YAML uses keys like pyffice_web_browser, pyffice_web_page etc.
        # But document_type might be 'browser', 'page', etc.
        doc_key = document_type
        if not document_type.startswith("pyffice_"):
            # Try to find the matching key in config
            for key in self.config.dikt:
                if key.endswith(document_type):
                    doc_key = key
                    break

        updated = True
        while updated:
            updated = False
            # Look for updates for the current version
            doc_config = self.config.dikt.get(doc_key, {})
            version_updates = doc_config.get("versions", {}).get(version, {})

            if version_updates:
                # We expect version_updates to be a dict where keys are next versions
                # For simplicity, we take the first one found, usually there's only one next version
                for next_version, updates in version_updates.items():
                    logma.info(
                        f"Updating {document_type} from {version} to {next_version}"
                    )

                    if "document" in updates:
                        self.update_document(updates["document"])
                    if "meta_data" in updates:
                        self.update_meta_data(updates["meta_data"])
                    if "data" in updates:
                        self.update_data(updates["data"])

                    version = next_version
                    updated = True
                    break  # Only one transition per loop
            else:
                break

        return version

    # listing out the update for every version and every document is unsustainable
    # how can we write this to use an yaml config file?


class PyfficeUpdater(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeUpdater").override(cfg)

    def update_document(self):
        """"""

    def update_unit(self):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
