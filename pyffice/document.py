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
import json as j
from collections import deque
from copy import deepcopy

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from squirl.orgnql import conql, yonql
from subtrix.subtrix import uuid
from pycurity.pytime import PyTime
from pyffice.tags.tags import PyfficeTag
from pycurity.pyhash import text_hashing_function
from pycurity.pyhash import decode64

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()
CHANGE_LIMIT = 100
# ====================================================================================================================||
pxcfg = join(here, "_data_", "document.yaml")


class PyfficeUnit(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeUnit").override(cfg)
        self.author = None
        self.change_limit = None
        self.changes = None
        self.content = None
        self.content_original = None
        self.context = None
        self.creon = None
        self.data = None
        self.description = None
        self.did = None
        self.doc_type = None
        self.editors = None
        self.encoding = None
        self.hash = None
        self.html = None
        self.is_saved = False
        self.location = None
        self.meta_data = None
        self.modon = None
        self.name = None
        self.path = None
        self.redos = None
        self.references = None
        self.syntax = None
        self.tags = None
        self.time = PyTime()  # TODO build override to allow for time object to be common across application
        self.unit = None
        self.version = 0

    def add_change(self, label, value, new_value, action="set", params=None):
        """"""
        # logma.info(f"Add Change {label} {action}")
        change_limit = CHANGE_LIMIT if self.change_limit is None else self.change_limit
        if self.changes is None:
            self.changes = []
        if isinstance(value, dict):
            value = deepcopy(value)
        if action == "add":
            self.changes.append({"action": action, "label": label, "value": deepcopy(value), "new_value": new_value})
        elif action == "set":
            self.changes.append({"action": action, "label": label, "value": value, "new_value": new_value})
        self.changes = self.changes[-change_limit:]
        return self

    def add_editor(self):
        """"""
        return self

    def add_tag(self, tag_name, description=""):
        """"""
        cfg = {}
        tag = PyfficeTag(cfg)
        self.tags.append(tag)
        return self

    def del_editor(self, dex):
        """"""
        return self

    def del_reference(self, reference):
        """"""
        return self

    def del_tag(self, tag):
        """"""
        tags = self.tags
        self.tags.remove(tag)
        self.add_change("tags", tags, self.tags)
        return self

    def get_context(self):
        """"""
        self.context = self.to_string()
        return self.context

    def get_hash(self):
        """"""
        self.hash = text_hashing_function(self.context)
        return self.hash

    def get_tags(self):
        """"""
        return self.tags

    def increment_version(self):
        """"""
        self.version += 1
        return self

    def load_unit(self, unit=None):
        """"""
        logma.info(f"Load Unit {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        if isinstance(unit, str):
            unit = j.loads(unit)
        self.time = PyTime()
        self.set_changes(unit.get("changes", None))
        self.set_author(unit.get("meta_data", {}).get("author", None))
        self.set_context(unit.get("context", None))
        self.set_creon(unit.get("meta_data", {}).get("creon", None))
        self.set_description(unit.get("description", None))
        self.set_did(unit.get("did", None))
        self.set_editors(unit.get("meta_data", {}).get("editors", None))
        self.set_encoding(unit.get("encoding", None))
        self.set_hash(unit.get("hash", None))
        self.set_saved(True)
        self.set_syntax(unit.get("syntax", None))
        self.set_location(unit.get("location", None))
        self.set_modon(unit.get("meta_data", {}).get("modon", None))
        self.set_name(unit.get("name", None))
        self.set_path(unit.get("path", None))
        self.set_tags(unit.get("tags", None))
        logma.info(f"Version {unit.get('version', None)}")
        self.set_version(unit.get("version", None))
        logma.info(f"Load Unit {unit}")
        self.redos = []
        return self

    def redo_change(self):
        """"""
        change = self.redos.pop()
        setattr(self, change["label"], change["new_value"])
        if change["action"] == "set":
            self.add_change(change["label"], change["value"], change["new_value"], "set")
        return self

    def set_author(self, author):
        """"""
        if author is None:
            author = ""
        if author != self.author:
            self.add_change("author", self.author, author)
            self.author = author
        return self

    def set_change_limit(self, limit=None):
        """"""
        if limit != self.change_limit:
            self.add_change("change_limit", self.change_limit, limit)
            self.change_limit = limit
        return self

    def set_changes(self, changes):
        """"""
        if changes is None:
            changes = []
        if changes != self.changes:
            self.add_change("changes", self.changes, changes)
            self.changes = changes
        return self

    def set_content(self, content):
        """"""
        if content is None:
            content = ""
        if self.content_original is None:
            self.add_change("content_original", self.content_original, content, "set")
            self.content_original = content
        if content != self.content:
            self.add_change("content", self.content, content)
            self.content = content
        return self

    def set_context(self, context):
        """"""
        if context is None:
            context = ""
        if context != self.context:
            self.add_change("context", self.context, context)
            self.context = context
        return self

    def set_creon(self, creon=None):
        """"""
        if creon is None:
            creon = self.time.get_current_datetime_str()
        if creon != self.creon:
            self.add_change("creon", self.creon, creon)
            self.creon = creon
        return self

    def set_data(self, data):
        """"""
        if data != self.data:
            self.add_change("data", self.data, data)
            self.data = data
        return self

    def set_description(self, description):
        """"""
        if description is None:
            description = ""
        if description != self.description:
            self.add_change("description", self.description, description)
            self.description = description
        return self

    def set_did(self, did=None):
        """"""
        if did is None:
            did = uuid()
        if did != self.did:
            self.add_change("did", self.did, did)
            self.did = did
        return self

    def set_editors(self, editors):
        """"""
        if editors is None:
            editors = []
        if editors != self.editors:
            self.add_change("editors", self.editors, editors)
            self.editors = editors
        return self

    def set_encoding(self, encoding=None):
        """"""
        if encoding is None:
            encoding = "utf-8"
        if encoding != self.encoding:
            self.add_change("encoding", self.encoding, encoding)
            self.encoding = encoding
        return self

    def set_hash(self, hash_):
        """"""
        if hash_ is None:
            hash_ = text_hashing_function(self.context)
        logma.info(f"Hash {hash_}")
        # TODO need to determine what parts get hased and when/where that happens
        if hash_ != self.hash:
            self.add_change("hash", self.hash, hash_)
            self.hash = hash_
        return self

    def set_location(self, location):
        """"""
        if location is None:
            location = ""
        if location != self.location:
            self.add_change("location", self.location, location)
            self.location = location
        return self

    def set_meta_data(self, meta_data):
        """"""
        if meta_data != self.meta_data:
            self.add_change("meta_data", self.meta_data, meta_data)
            self.meta_data = meta_data
        return self

    def set_modon(self, modon=None):
        """"""
        if modon is None:
            modon = self.time.get_current_datetime_str()
        if modon != self.modon:
            self.add_change("modon", self.modon, modon)
            self.modon = modon
        return self

    def set_name(self, name):
        """"""
        if name is None:
            name = self.did
        if name != self.name:
            self.add_change("name", self.name, name)
            self.name = name
        return self

    def set_path(self, path):
        """"""
        if path is None:
            path = ""
        if path != self.path:
            self.add_change("path", self.path, path)
            self.path = path
        return self

    def set_redos(self, redos):
        """"""
        if redos != self.redos:
            self.add_change("redos", self.redos, redos)
            self.redos = redos
        return self

    def set_references(self, references):
        """"""
        if references is None:
            references = []
        if references != self.references:
            self.add_change("references", self.references, references)
            self.references = references
        return self

    def set_saved(self, saved):
        """"""
        if saved != self.is_saved:
            self.add_change("saved", self.is_saved, saved)
            self.is_saved = saved
        return self

    def set_syntax(self, syntax):
        """"""
        if syntax is None:
            syntax = "plain-text"
        if syntax != self.syntax:
            self.add_change("syntax", self.syntax, syntax)
            self.syntax = syntax
        return self

    def set_tags(self, tags):
        """"""
        if tags is None:
            tags = []
        if tags != self.tags:
            self.add_change("tags", self.tags, tags)
            self.tags = tags
        return self

    def set_version(self, version):
        """"""
        if version is None:
            version = 0
        if version != self.version:
            self.add_change("version", self.version, version)
            self.version = version
        return self

    def to_dict(self):
        """Each Docuement Subclass will need to implement this method
        add creation and mod dates
        add author information

        these additional meta datas are not neccesarily internally as their values are carried in context

        """
        doc = {"did": self.did}
        doc["name"] = self.name
        doc["description"] = self.description
        doc["meta_data"] = {
            "author": self.author,
            "context": self.context,
            "editors": self.editors,
            "encoding": self.encoding,
            "hash": self.hash,
            "location": self.location,
            "path": self.path,
            "syntax": self.syntax,
            "creon_dttm": self.set_creon().creon,
            "mod_dttm": self.set_modon().modon,
        }
        if self.tags is not None:
            doc["meta_data"]["tags"] = [x.to_dict() for x in self.tags]
        doc["unit"] = {"content": self.content, "changes": self.changes[:30]}
        # doc["changes"] = self.changes[:30]
        return doc

    def to_html(self):
        """"""
        return self.html

    def to_string(self):
        """"""
        return j.dumps(self.to_dict())

    def undo_change(self):
        """"""
        last_change = self.changes.pop()
        self.redos.append(last_change)
        setattr(self, last_change["label"], last_change["value"])
        return self


class PyfficeDocument(PyfficeUnit):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeDocument")).override(cfg)
        self.cache = None
        self.compatibility = None
        self.document = None
        self.doc_types = None
        self.file_path = None
        self.file_type = None
        self.hash = None
        self.porter = None
        self.policy = None
        # self.lang = utils.invert_dict(self.config.dikt.get("imageLIST", None))
        # self.img = utils.invert_dict(self.config.dikt.get("textLIST", None))

    def file_export(self, file_=None):
        """"""

    def file_import(self, file_type):
        """"""

    def file_open(self, file_path, open_=True):
        """"""
        if file_path is None:
            file_path = self.file_path
        self.file_path = file_path
        text = None
        if open_ is True:
            with open(str(self.file_path), "r") as f:
                text = f.read()
        return text

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        if isinstance(document, str):
            document = j.loads(document)
        logma.info(f"Load Unit {document}")
        self.load_unit(document)
        # self.set_cache(document.get("cache", None))
        self.set_compatibility(document.get("compatibility", "pyffice"))
        self.set_document(document.get("document", {}))
        logma.info(f"File Path {document.get('file_path', None)}")
        self.set_file_path(document.get("file_path", None))
        self.set_file_type(document.get("file_type", None))
        return self

    def update_document_time(self):
        """"""
        self.set_modon(self.time.get_current_datetime_str())
        return self

    def save(self, path=None, syntax=None, encrypt_key=None):
        """"""
        if path is None:
            path = self.file_path
        if syntax is None:
            syntax = self.syntax
        self.increment_version()
        if syntax is None:
            self.save_pyffice(path, syntax, encrypt_key)
            self.is_saved = True
        return self

    def save_copy(self, path, syntax=None, encrypt_key=None):
        """"""
        self.save_as(path, False, syntax, encrypt_key)
        return self

    def save_pyffice(self, path, syntax, encrypt_key=None):
        """ """
        # use syntax to select a template
        if encrypt_key:
            doc = encrypt256(self.to_string(), encrypt_key)
            txtonql.Doc(doc).write(path)
        else:
            doc = self.to_dict()
            yonql.Doc(doc).write(path)
        return self

    def save_as(self, path, set_file_active=True, syntax=None, encrypt_key=None):
        """"""
        if set_file_active:
            self.file_path = path
        self.save(path, syntax, encrypt_key)
        return self

    def search(self, term):
        """"""
        return self.search_document(term)

    def search_document(self, term):
        """"""
        if term in self.get_context():
            return True
        return False

    def set_cache(self, cache):
        """"""
        self.cache = conql.Doc()
        self.cache.load(cache)
        return self

    def set_compatibility(self, compatibility):
        """"""
        if compatibility != self.compatibility:
            self.add_change("compatibility", self.compatibility, compatibility)
            self.compatibility = compatibility
        return self

    def set_document(self, document):
        """"""
        if document is None:
            document = {}
        if isinstance(document, str):
            document = j.loads(document)
        self.document = document
        return self

    def set_file_path(self, file_path):
        """"""
        if file_path is None:
            file_path = self.config.dikt.get("file_path", "")
        if file_path != self.file_path:
            self.add_change("file_path", self.file_path, file_path)
            self.file_path = file_path
        return self

    def set_file_type(self, file_type):
        """"""
        if file_type != self.file_type:
            self.add_change("file_type", self.file_type, file_type)
            self.file_type = file_type
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["file_path"] = self.file_path
        doc["document"] = doc["unit"]
        del doc["unit"]
        return doc


class PyfficeDocumentManager(PyfficeDocument):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeDocumentManager")).override(cfg)
        self.store = conql.Doc()

    def add_document(self, document):
        """"""
        self.documents[document.name] = document
        return self

    def del_document(self, name):
        """"""
        if name not in self.documents:
            return self
        del self.documents[name]
        return self

    def get_context(self):
        """"""
        super().get_context()
        return self

    def get_document(self, name):
        """"""
        return self.documents[name]

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_doc_types(document.get("doc_types", []))
        self.set_documents(document.get("documents", {}))
        return self

    def search(self, term):
        """"""
        result = self.search_documents(term)
        if result is None:
            return None
        return self.documents[result]

    def search_documents(self, term):
        """"""
        for name, document in self.documents.items():
            if document.search(term):
                return name
        return None

    def set_documents(self, documents):
        """"""
        self.documents = documents
        return self

    def set_doc_types(self, doc_types):
        """"""
        if doc_types is None:
            doc_types = []
        self.doc_types = doc_types
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"]["documents"] = []
        if self.documents is None:
            return doc
        for name, document in self.documents.items():
            doc["document"]["documents"].append({name: document.to_dict()})
        return doc


class PyfficeDeque(PyfficeDocument, deque):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        PyfficeDocument.__init__(self, self.config)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeDeque")).override(cfg)
        self.max_items = None
        self.set_max_items()
        self.history = deque()

    def append(self, item):
        """"""
        if self.max_items is not None:
            if len(self) >= self.max_items:
                self.history.append(self.popleft())
        super().append(item)

    def appendleft(self, item):
        """"""
        raise Exception("")

    def set_max_items(self, max_items=None):
        """"""
        if max_items is None:
            max_items = self.config.dikt.get("max_items", 10)
        self.max_items = max_items
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
