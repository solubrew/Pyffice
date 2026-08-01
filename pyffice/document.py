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
from os.path import abspath, dirname, join, exists
import datetime as dt
import json as j
from collections import deque
from copy import deepcopy

# ======================================3rd Party Library Modules=====================================================||
# from sentence_transformers import SentenceTransformer

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from squirl.orgnql import conql, yonql
from subtrix.utilities import uuid
from pycurity.pytime import PyTime
from pyffice.tags.tags import PyfficeTag
from pyffice.updates.updates import PyfficeUnitUpdate, PyfficeDocumentUpdate
from pycurity.pyhash import text_hashing_function
from squirl.objnql import txtonql

# MissingPathError / InvalidConfigurationError imported locally inside
# methods that raise them (T-NEW-055) to avoid the circular import
# (document.py <-> pyffice.pyffice).

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()
CHANGE_LIMIT = 100
# ====================================================================================================================||
pxcfg = join(here, "_data_", "document.yaml")


class PyfficeUnit(object):
    """"""

    # T-NEW-005 (item 2): per-class serialization version
    # (semver triple). When ``to_dict``'s schema changes in a
    # non-backward-compatible way, bump ``MAJOR`` (or
    # ``MINOR`` for additive-but-required changes). The
    # receiving side reads ``meta_data["schema_version"]``
    # from the payload and dispatches upgrade paths by
    # comparing this triple to the producer's triple.
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeUnit").override(cfg)
        self.unit = self.config.select("template").override(self.config.select("unit"))
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
        self.time = PyTime()  # RESOLVED: Using common PyTime instance
        self.version = 0
        self.versions = None

    def add_change(self, label, value, new_value, action="set", params=None):
        """Record a change entry for this document.
        
        Args:
            label: Parameter.
            value: Parameter.
            new_value: Parameter.
            action: Parameter.
            params: Parameter.
        
        Returns:
            Self for chaining.
        """
        # logma.info(f"Add Change {label} {action}")
        change_limit = CHANGE_LIMIT if self.change_limit is None else self.change_limit
        if self.changes is None:
            self.changes = []
        if isinstance(value, dict):
            value = deepcopy(value)
        if isinstance(new_value, dict):
            new_value = deepcopy(new_value)
        # elif isinstance(value, PyfficeUnit):
        #     value = value.to_dict()
        # if isinstance(new_value, PyfficeUnit):
        #     new_value = new_value.to_dict()

        if action == "add":
            self.changes.append(
                {
                    "action": action,
                    "label": label,
                    "value": deepcopy(value),
                    "new_value": new_value,
                }
            )
        elif action == "set":
            self.changes.append(
                {
                    "action": action,
                    "label": label,
                    "value": value,
                    "new_value": new_value,
                }
            )
        self.changes = self.changes[-change_limit:]
        return self

    def _set_with_change(self, attr, value, label=None, default=None):
        """Set ``self.<attr> = value`` and record a change entry.

        Consolidates the recurring pattern across every ``set_X``
        method on this class:

            if X != self.X:
                self.add_change("X", self.X, X)
                self.X = X
            return self

        Subclasses that need custom behaviour (e.g. ``set_hash``
        and ``set_saved``) keep their own implementations; this is
        the shared shortcut for the common case.

        Args:
            attr: Attribute name on ``self`` to set.
            value: New value. If ``value is None`` and ``default``
                is not None, ``default`` is used instead.
            label: Change-tracking label. Defaults to ``attr``.
            default: Fallback value when ``value`` is ``None``.

        Returns:
            Self for chaining.
        """
        if value is None and default is not None:
            value = default
        if label is None:
            label = attr
        current = getattr(self, attr, None)
        if value != current:
            self.add_change(label, current, value)
            setattr(self, attr, value)
        return self

    def _del_from_dict(self, attr, key, label):
        """Delete an entry from a dict-typed attribute and record the change.

        Used by ``del_layer`` (and similar) on classes that store
        collections in a ``self.<attr>`` dict. Tracks the change so
        undo/redo works.

        Args:
            attr: Name of the dict attribute on ``self``
                (e.g. ``"layers"``).
            key: Dict key to delete.
            label: Change-tracking label (e.g. ``"layers"``).

        Returns:
            Self for chaining.
        """
        collection = getattr(self, attr)
        self.add_change(label, collection, collection.get(key), "del")
        del collection[key]
        return self

    def _add_to_collection(self, attr, value, label):
        """Append ``value`` to a list-typed attribute and record the change.

        Used by ``add_source``, ``add_view``, etc. on classes that
        store collections in a ``self.<attr>`` list/set. Tracks the
        change so undo/redo works.

        Args:
            attr: Name of the collection attribute on ``self``
                (e.g. ``"sources"``).
            value: Value to add.
            label: Change-tracking label.

        Returns:
            Self for chaining.
        """
        collection = getattr(self, attr)
        self.add_change(label, collection, value, "add")
        if isinstance(collection, set):
            collection.add(value)
        else:
            collection.append(value)
        return self

    def _del_from_collection(self, attr, value, label):
        """Remove ``value`` from a list-typed attribute and record the change.

        Used by ``del_source``, ``del_view``, etc.

        Args:
            attr: Name of the collection attribute on ``self``.
            value: Value to remove.
            label: Change-tracking label.

        Returns:
            Self for chaining.
        """
        collection = getattr(self, attr)
        self.add_change(label, collection, value, "del")
        collection.remove(value)
        return self

    def add_editor(self, editor):
        """Add an editor to the document."""
        self.editors = getattr(self, 'editors', [])
        self.editors.append(editor)
        return self

    def add_tag(self, tag_name, description=""):
        """Attach a tag to this document.
        
        Args:
            tag_name: Parameter.
            description: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {}
        tag = PyfficeTag(cfg)
        self.tags.append(tag)
        return self

    def del_editor(self, dex):
        """Delete an editor by index."""
        editors = getattr(self, 'editors', [])
        if 0 <= dex < len(editors):
            editors.pop(dex)
        return self

    def del_reference(self, reference):
        """Delete a reference."""
        refs = getattr(self, 'references', [])
        if reference in refs:
            refs.remove(reference)
        return self

    def del_tag(self, tag):
        """Remove a tag from this document.
        
        Args:
            tag: Parameter.
        
        Returns:
            Self for chaining.
        """
        tags = self.tags
        self.tags.remove(tag)
        self.add_change("tags", tags, self.tags)
        return self

    def get_context(self):
        """Return the current document context as a string.
        
        Returns:
            Self for chaining.
        """
        self.context = self.to_string()
        return self.context

    def get_hash(self):
        """Return a hash of the current document context.
        
        Returns:
            Self for chaining.
        """
        self.hash = text_hashing_function(self.context)
        return self.hash

    def get_tags(self):
        """Return the list of tags attached to this document.
        
        Returns:
            Self for chaining.
        """
        return self.tags

    def increment_version(self):
        """Increment the document version counter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Increment Version {self.version}")
        self.version = int(self.version) + 1
        #         8 02:49:17", "mod_dttm": "2026-07-28 02:49:17"}, "unit": {"original_path": null, "active_url": null, "trust_level": null, "qualified_path": null, "domain": null, "redirect_path": null}}, "source": null}}}
        #         2026-07-27 22:49:17,464 - nchantdoffice.models                      439: INFO     - Document Content Saved
        #         Traceback (most recent call last):
        #         File "/mnt/iverse/SB/3_Functions/Projects/NchantdOffice/3_Work/1_DELTA/nchantdoffice/nchantdoffice/widgets/widgets.py", line 163, in on_tab_focus
        #         self.model.load_tab(self.model.tabsdata[tabn], tabn, self.pane_position)
        #     File "/mnt/iverse/SB/3_Functions/Projects/NchantdOffice/3_Work/1_DELTA/nchantdoffice/nchantdoffice/models.py", line 3258, in load_tab
        #     super().load_tab(tab, tabn, tabset, active_tab_position)
        # File "/mnt/iverse/SB/3_Functions/Operations/opENGRg/3_Work/jobElfSys/actvPython/tskNchantrs/1_DELTA/nchantrs/nchantrs/models/tabsetmodels.py", line 237, in load_tab
        # self.tab_widgets.insert(tabn, self.load_widget(self.parse_widget_data(tab), tabset, tab))
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # File "/mnt/iverse/SB/3_Functions/Projects/NchantdOffice/3_Work/1_DELTA/nchantdoffice/nchantdoffice/models.py", line 3334, in load_widget
        # tabW.initWidget()
        # File "/mnt/iverse/SB/3_Functions/Projects/NchantdOffice/3_Work/1_DELTA/nchantdoffice/nchantdoffice/widgets/documents/atnrg/browsers.py", line 1699, in initWidget
        # self.initView()
        # File "/mnt/iverse/SB/3_Functions/Projects/NchantdOffice/3_Work/1_DELTA/nchantdoffice/nchantdoffice/widgets/documents/atnrg/browsers.py", line 1693, in initView
        # self.populate_document()
        # File "/mnt/iverse/SB/3_Functions/Projects/NchantdOffice/3_Work/1_DELTA/nchantdoffice/nchantdoffice/widgets/documents/atnrg/browsers.py", line 1724, in populate_document
        # self.document.save()
        # File "/mnt/iverse/SB/3_Functions/Projects/Pyffice/3_Work/1_DELTA/pyffice/pyffice/document.py", line 519, in save
        # self.increment_version()
        # File "/mnt/iverse/SB/3_Functions/Projects/Pyffice/3_Work/1_DELTA/pyffice/pyffice/document.py", line 164, in increment_version
        # self.version = int(self.version)
        # ^^^^^^^^^^^^^^^^^
        # ValueError: invalid literal for int() with base 10: '1.0.1.0'
        # 2026-07-27 22:49:17,629 - nchantrs.widgets.browsers.browsers        336: INFO     - URL Changed: PySide6.QtCore.QUrl('https://duckduckgo.com/')
        return self

    def load_unit(self, unit=None):
        """Load a unit dict into this document.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        # logma.inspect_caller()
        logma.info(f"Load Unit {unit}")
        if isinstance(unit, str):
            unit = j.loads(unit)
        unit = self.unit.override(unit).dikt
        self.versions = self.config.dikt.get("versions", {})
        # unit = self.update_unit_structure(unit)
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
        logma.info(f"Load Unit {unit}")
        self.redos = []
        return self

    def redo_change(self):
        """Redo the last undone change.
        
        Returns:
            Self for chaining.
        """
        change = self.redos.pop()
        setattr(self, change["label"], change["new_value"])
        if change["action"] == "set":
            self.add_change(change["label"], change["value"], change["new_value"], "set")
        return self

    def set_author(self, author):
        """Set the document author.
        
        Args:
            author: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("author", author, default='')

    def set_change_limit(self, limit=None):
        """Set the change limit.
        
        Args:
            limit: Parameter.
        
        Returns:
            Self for chaining.
        """
        if limit != self.change_limit:
            self.add_change("change_limit", self.change_limit, limit)
            self.change_limit = limit
        return self

    def set_changes(self, changes):
        """Set the changes.
        
        Args:
            changes: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("changes", changes, default=[])

    def set_context(self, context):
        """Set the context.
        
        Args:
            context: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("context", context, default='')

    def set_creon(self, creon=None):
        """Set the creon.
        
        Args:
            creon: Parameter.
        
        Returns:
            Self for chaining.
        """
        if creon is None:
            creon = self.time.get_current_datetime_str()
        if creon != self.creon:
            self.add_change("creon", self.creon, creon)
            self.creon = creon
        return self

    def set_data(self, data):
        """Set the data.
        
        Args:
            data: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("data", data)

    def set_description(self, description):
        """Set the description.
        
        Args:
            description: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("description", description, default='')

    def set_did(self, did=None):
        """Set the did.
        
        Args:
            did: Parameter.
        
        Returns:
            Self for chaining.
        """
        if did is None:
            did = uuid()
        if did != self.did:
            self.add_change("did", self.did, did)
            self.did = did
        return self

    def set_editors(self, editors):
        """Set the editors.
        
        Args:
            editors: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("editors", editors, default=[])

    def set_encoding(self, encoding=None):
        """Set the encoding.
        
        Args:
            encoding: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("encoding", encoding, default='utf-8')

    def set_hash(self, hash_):
        """Set the hash.
        
        Args:
            hash_: Parameter.
        
        Returns:
            Self for chaining.
        """
        if hash_ is None:
            hash_ = text_hashing_function(self.context)
        logma.info(f"Hash {hash_}")
        # RESOLVED: Hash computed from full context in set_hash()
        if hash_ != self.hash:
            self.add_change("hash", self.hash, hash_)
            self.hash = hash_
        return self

    def set_location(self, location):
        """Set the location.
        
        Args:
            location: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("location", location, default='internal')

    def set_meta_data(self, meta_data):
        """Set the meta data.
        
        Args:
            meta_data: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("meta_data", meta_data)

    def set_modon(self, modon=None):
        """Set the modon.
        
        Args:
            modon: Parameter.
        
        Returns:
            Self for chaining.
        """
        if modon is None:
            modon = self.time.get_current_datetime_str()
        if modon != self.modon:
            self.add_change("modon", self.modon, modon)
            self.modon = modon
        return self

    def set_name(self, name):
        """Set the name.
        
        Args:
            name: Parameter.
        
        Returns:
            Self for chaining.
        """
        if name is None:
            name = self.did
        if name != self.name:
            self.add_change("name", self.name, name)
            self.name = name
        return self

    def set_path(self, path):
        """Set the path.
        
        Args:
            path: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("path", path, default='')

    def set_redos(self, redos):
        """Set the redos.
        
        Args:
            redos: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("redos", redos)

    def set_references(self, references):
        """Set the references.
        
        Args:
            references: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("references", references, default=[])

    def set_saved(self, saved):
        """Set the saved.
        
        Args:
            saved: Parameter.
        
        Returns:
            Self for chaining.
        """
        if saved != self.is_saved:
            self.add_change("saved", self.is_saved, saved)
            self.is_saved = saved
        return self

    def set_syntax(self, syntax):
        """Set the syntax.
        
        Args:
            syntax: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("syntax", syntax, default='plain-text')

    def set_tags(self, tags):
        """Set the tags.
        
        Args:
            tags: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("tags", tags, default=[])

    def set_version(self, version):
        """Set the version.
        
        Args:
            version: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("version", version, default=0)

    def to_dict(self):
        """Serialize this object to a dict.
        
        Returns:
            Self for chaining.
        """
        from pyffice.pyffice import InvalidConfigurationError
        """Each Docuement Subclass will need to implement this method
        add creation and mod dates
        add author information

        these additional meta datas are not neccesarily internally as their values are carried in context

        T-NEW-005 (item 2): ``meta_data["semver"]`` records the
        Pyffice package version that produced this payload. The
        receiving side uses it to dispatch upgrade paths when
        loading older payloads.
        """
        # Lazy import to avoid a circular import at module
        # load time (PyfficeUnit is defined before the
        # ``pyffice`` package init is fully populated).
        from pyffice import __version__

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
            "semver": __version__,
            "schema_version": list(self.SERIALIZATION_VERSION),
            "creon_dttm": self.set_creon().creon,
            "mod_dttm": self.set_modon().modon,
        }
        if self.tags is not None:
            if isinstance(self.tags, list):
                doc["meta_data"]["tags"] = [x.to_dict() for x in self.tags]
            elif isinstance(self.tags, (str, int, float)):
                doc["meta_data"]["tags"] = [self.tags]
            else:
                raise InvalidConfigurationError(f"Tags not properly formated {self.tags}")
        doc["unit"] = {"content": self.content}
        return doc

    def to_html(self):
        """Convert this document to html.
        
        Returns:
            Self for chaining.
        """
        return self.html

    def _canonicalize(self, doc):
        """Add the canonical, additive shape keys to a subclass's
        to_dict() payload.

        This helper is part of the T-NEW-005 additive-shape
        normalization (Sprint 18, User NEW TODO #5). Existing
        per-subclass keys (``table``, ``pages``, ``path``, etc.)
        are PRESERVED — only missing canonical keys are filled in.
        A ``pyffice_compat`` marker records which canonical keys
        were added so downstream readers can identify the
        normalized shape without breaking older payloads.

        The canonical keys are:
          - ``data["content"]``: dict — the primary payload. If a
            subclass writes its payload under ``table``, ``pages``,
            etc., that key is mirrored into ``content`` (without
            overwriting an existing ``content`` key).
          - ``data["path"]``: file_path string (mirrored from
            ``meta_data["path"]`` if available, otherwise from
            ``self.file_path``).
          - ``data["schema_version"]``: list of
            ``self.SERIALIZATION_VERSION`` (also lives in
            ``meta_data``; mirrored for symmetry).
          - ``pyffice_compat``: dict — the version of the
            canonical-shape normalizer that produced this payload.
            Older payloads without this key are still loadable.

        Args:
            doc: The dict built by ``to_dict()``. Mutated in place.

        Returns:
            The same ``doc`` (for chaining).
        """
        from pyffice import __version__

        data = doc.setdefault("data", {})
        if not isinstance(data, dict):
            return doc

        # Mirror a primary payload key into ``content`` if absent.
        # Heuristic: the first key in ``data`` that's not a meta
        # field is the primary payload. Subclasses that already set
        # ``content`` are left alone.
        if "content" not in data:
            meta_keys = {
                "document_type", "schema_version", "path", "tags",
                "encoding", "syntax", "semver", "creon_dttm",
                "mod_dttm", "compatibility", "documents",
            }
            for candidate_key, candidate_val in data.items():
                if candidate_key in meta_keys:
                    continue
                # Only mirror dict/list/scalar payloads, not other
                # nested structures.
                if isinstance(candidate_val, (dict, list, str, int, float, bool)) \
                        or candidate_val is None:
                    data["content"] = candidate_val
                    break

        # Mirror ``path`` if missing.
        if "path" not in data:
            meta = doc.get("meta_data", {})
            data["path"] = meta.get("path") or getattr(self, "file_path", None)

        # Mirror schema_version for symmetry with meta_data.
        if "schema_version" not in data:
            data["schema_version"] = list(self.SERIALIZATION_VERSION)

        # Stamp the compat marker. If a subclass already set one,
        # leave it alone.
        if "pyffice_compat" not in doc:
            doc["pyffice_compat"] = {
                "normalizer": "additive-canonical",
                "package": __version__,
                "schema_version": list(self.SERIALIZATION_VERSION),
            }
        return doc

    def to_string(self):
        """Convert this document to string.
        
        Returns:
            Self for chaining.
        """
        return j.dumps(self.to_dict())

    def undo_change(self):
        """Undo change.
        
        Returns:
            Self for chaining.
        """
        last_change = self.changes.pop()
        self.redos.append(last_change)
        setattr(self, last_change["label"], last_change["value"])
        return self

    def update_unit_structure(self, unit):
        """Update unit structure.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        unit = PyfficeUnitUpdate(unit).process()
        return unit


class PyfficeDocument(PyfficeUnit):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDocument").override(cfg))
        self.document = self.config.select("template").override(self.config.select("document").dikt)
        self.cache = None
        self.compatibility = None
        self.data = None
        self.doc_types = None
        self.document_type = None
        self.file_path = None
        self.file_type = None
        self.hash = None
        self.porter = None
        self.policy = None
        self.vectors = {}
        # self.lang = utils.invert_dict(self.config.dikt.get("imageLIST", None))
        # self.img = utils.invert_dict(self.config.dikt.get("textLIST", None))

    def file_export(self, file_=None):
        """Export document to file via the appropriate Port class.

        Dispatches on the destination file extension to select the
        correct exporter (Excel -> PyfficePortExcel, CSV ->
        PyfficePortCSV, image -> PyfficePortImage, etc.) and writes
        the document contents out.

        Args:
            file_: Destination path. If None, uses ``self.file_path``.

        Returns:
            ``self`` for chaining.
        """
        if not file_:
            file_ = self.file_path
        if not file_:
            from pyffice.pyffice import MissingPathError

            raise MissingPathError("file_export requires a destination path")
        from pathlib import Path
        ext = Path(str(file_)).suffix.lower()

        # Lazy import the matching Port class for the extension
        port = self._port_for_ext(ext)
        if port is not None:
            port.file_path = str(file_)
            port.export(self)
        return self

    def file_import(self, file_path=None):
        """Import document content from a file via the matching Port.

        Detects the file extension and dispatches to the right Port
        class (PyfficePortExcel for .xlsx, PyfficePortCSV for .csv,
        PyfficePortImage for image formats, etc.). The Port loads the
        file, then this method copies the loaded payload into
        ``self.data``.

        Args:
            file_path: Source path. If None, uses ``self.file_path``.

        Returns:
            ``self`` for chaining.
        """
        if file_path is None:
            file_path = self.file_path
        if not file_path:
            from pyffice.pyffice import MissingPathError

            raise MissingPathError("file_import requires a source path")
        from pathlib import Path
        ext = Path(str(file_path)).suffix.lower()

        port = self._port_for_ext(ext)
        if port is not None:
            port.file_path = str(file_path)
            loaded = port.import_data()
            if loaded is not None:
                self.set_data(loaded)
        return self

    def _port_for_ext(self, ext):
        """Return a fresh Port instance for the given extension, or
        None if no Port class matches the extension."""
        if not ext:
            return None
        # Local imports avoid cycles
        try:
            from pyffice.ports.ports import (
                PyfficePortExcel,
                PyfficePortCSV,
                PyfficePortImage,
                PyfficePortDia,
                PyfficePortFileSystem,
            )
        except ImportError:
            return None

        mapping = {
            ".xlsx": PyfficePortExcel,
            ".xlsm": PyfficePortExcel,
            ".xls": PyfficePortExcel,
            ".csv": PyfficePortCSV,
            ".tsv": PyfficePortCSV,
            ".png": PyfficePortImage,
            ".jpg": PyfficePortImage,
            ".jpeg": PyfficePortImage,
            ".gif": PyfficePortImage,
            ".bmp": PyfficePortImage,
            ".svg": PyfficePortImage,
            ".webp": PyfficePortImage,
            ".dia": PyfficePortDia,
        }
        cls = mapping.get(ext)
        if cls is None:
            return PyfficePortFileSystem()
        return cls()

    def file_open(self, file_path, open_=True):
        """Open a file and return its raw text content.

        For binary formats (.xlsx, .pdf, .png, etc.), this returns
        ``None`` and the caller should use ``file_import`` instead
        so the appropriate Port can decode the binary payload.

        Args:
            file_path: Path to the file.
            open_: If True, read the file content; otherwise just
                record the path on ``self.file_path``.

        Returns:
            Decoded text, or None if the file is binary.
        """
        if file_path is None:
            file_path = self.file_path
        self.file_path = file_path
        text = None
        if open_ is True:
            from pathlib import Path
            ext = Path(str(file_path)).suffix.lower()
            # Detect binary by extension
            binary_exts = {
                ".xlsx", ".xlsm", ".xls", ".pdf", ".png", ".jpg",
                ".jpeg", ".gif", ".bmp", ".webp", ".zip", ".tar",
                ".gz", ".bz2", ".7z", ".rar", ".mp4", ".mp3",
                ".wav", ".ogg", ".flac", ".heic", ".raw",
            }
            if ext in binary_exts:
                return None
            with open(str(self.file_path), "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        return text

    def load_document(self, document=None):
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        if isinstance(document, str):
            document = j.loads(document)
        document = self.document.override(document).dikt
        self.load_unit(document)
        logma.warning(f"Document {document}")
        data = document.get("data", {}) or {}
        self.set_content(data.get("content", {}))
        meta_data = document.get("meta_data", {}) or {}
        self.set_compatibility(meta_data.get("compatibility", "pyffice"))
        self.set_document_type(meta_data.get("document_type", "text"))
        self.set_data(data)
        self.set_file_path(document.get("path", None))
        self.set_version(document.get("version", None))
        return self

    def update_document_time(self):
        """Update document time.
        
        Returns:
            Self for chaining.
        """
        self.set_modon(self.time.get_current_datetime_str())
        return self

    def save(self, path=None, syntax=None, encrypt_key=None):
        """Save the document.
        
        Args:
            path: Parameter.
            syntax: Parameter.
            encrypt_key: Parameter.
        
        Returns:
            Self for chaining.
        """
        # if path is None:
        #     path = self.file_path
        # if syntax is None:
        #     syntax = self.syntax
        self.increment_version()
        # if syntax is None:
        #     self.save_pyffice(path, syntax, encrypt_key)
        #     self.is_saved = True
        return self

    def save_copy(self, path, syntax=None, encrypt_key=None):
        """Save a copy of the document at the given path.

        Args:
            path: Destination path for the copy.
            syntax: Optional syntax/format identifier.
            encrypt_key: Optional encryption key.

        Returns:
            Self for chaining.
        """
        self.save_as(path, False, syntax, encrypt_key)
        return self

    def save_pyffice(self, path, syntax, encrypt_key=None):
        """Save the document to a .pyof file in Pyffice native format.

        Args:
            path: Destination path.
            syntax: Format/syntax identifier.
            encrypt_key: Optional encryption key.

        Returns:
            Self for chaining.
        """
        from pyffice.pyffice import MissingPathError
        # use syntax to select a template
        if path is None:
            raise MissingPathError(f"No path provided")
        if encrypt_key:
            txtonql.Doc(path).write(encrypt256(self.to_string(), encrypt_key))
        else:
            yonql.Doc(path).write(self.to_dict())
        return self

    def save_as(self, path, set_file_active=True, syntax=None, encrypt_key=None):
        """Save the document.
        
        Args:
            path: Parameter.
            set_file_active: Parameter.
            syntax: Parameter.
            encrypt_key: Parameter.
        
        Returns:
            Self for chaining.
        """
        if set_file_active:
            self.file_path = path
        self.save(path, syntax, encrypt_key)
        return self

    def search_document(self, term):
        """Search document.
        
        Args:
            term: Parameter.
        
        Returns:
            Self for chaining.
        """
        if term in self.get_context():
            return True
        return False

    def search_vector(self, query):
        """Search vectors for query."""
        # Placeholder - would use vector similarity search
        return []

    def search_word(self, term):
        """Search word.
        
        Args:
            term: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self.search_document(term)

    def set_cache(self, cache):
        """Set the cache.
        
        Args:
            cache: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.cache = conql.Doc()
        self.cache.load(cache)
        return self

    def set_compatibility(self, compatibility):
        """Set the compatibility.
        
        Args:
            compatibility: Parameter.
        
        Returns:
            Self for chaining.
        """
        if compatibility != self.compatibility:
            self.add_change("compatibility", self.compatibility, compatibility)
            self.compatibility = compatibility
        return self

    def set_content(self, content):
        """Set the content.
        
        Args:
            content: Parameter.
        
        Returns:
            Self for chaining.
        """
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
        """Set the context.
        
        Args:
            context: Parameter.
        
        Returns:
            Self for chaining.
        """
        if context is None:
            context = ""
        if context != self.context:
            self.add_change("context", self.context, context)
            # self.vectorize(content)
            self.context = context
        return self

    def set_data(self, data):
        """Set the data.
        
        Args:
            data: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Data {data}")
        data = data or {}
        if isinstance(data, str):
            data = j.loads(data)
        super().set_data(data)
        return self

    def set_document_type(self, document_type):
        """Set the document type.
        
        Args:
            document_type: Parameter.
        
        Returns:
            Self for chaining.
        """
        if document_type != self.document_type:
            self.add_change("document_type", self.document_type, document_type)
            self.document_type = document_type
        return self

    def set_file_path(self, file_path):
        """Set the file path.
        
        Args:
            file_path: Parameter.
        
        Returns:
            Self for chaining.
        """
        if file_path is None:
            file_path = self.config.dikt.get("file_path", None)
        if file_path is None:  # PyfficePDF
            data = self.config.dikt.get("data", {}) or {}
            content = data.get("content", {}) or {}
            file_path = content.get("file_path", None)
        if file_path is None:
            document = self.config.dikt.get("document", {}) or {}
            content = document.get("content", {}) or {}
            file_path = content.get("file_path", None)
        if file_path is None:  # PyfficeImage
            document = self.config.dikt.get("document", {}) or {}
            data = document.get("data", {}) or {}
            content = data.get("content", {}) or {}
            file_path = content.get("file_path", None)
        if file_path is None:  # PyfficeScript
            document = self.config.dikt.get("document", {}) or {}
            data = document.get("data", {}) or {}
            content = data.get("content", {}) or {}
            content = content.get("content", {}) or {}
            file_path = content.get("file_path", None)
        if file_path is None:
            document = self.config.dikt.get("document", {}) or {}
            file_path = document.get("path", None)
        logma.info(f"\n[PyfficeDocument] Document {self.config.dikt}\n")
        logma.info(f"\n[PyfficeDocument] File Path {file_path}\n")
        if file_path is None:
            return self
        if exists(file_path):
            if file_path != self.file_path:
                self.add_change("file_path", self.file_path, file_path)
                self.file_path = file_path
                self.set_location("external")
        else:
            logma.warning(f"File Path Does Not Exist {file_path}")
        logma.info(f"[PyfficeDocument] File Path {self.file_path}")
        return self

    def set_file_type(self, file_type):
        """Set the file type.
        
        Args:
            file_type: Parameter.
        
        Returns:
            Self for chaining.
        """
        if file_type != self.file_type:
            self.add_change("file_type", self.file_type, file_type)
            self.file_type = file_type
        return self

    def to_dict(self):
        """Convert this document to dict.
        
        Returns:
            Self for chaining.
        """
        doc = super().to_dict()
        doc["file_path"] = self.file_path
        doc["data"] = deepcopy(doc["unit"])
        del doc["unit"]
        # Normalize the canonical shape once at the base layer
        # so every subclass gets ``data["content"]``,
        # ``data["path"]``, and ``pyffice_compat`` automatically.
        # The call is idempotent (subclasses that already added
        # ``content`` are left alone).
        return self._canonicalize(doc)

    def update_document_structure(self, document):
        """Update document structure.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        update = PyfficeDocumentUpdate(document)
        document = update.process()
        return document

    def vectorize(self, content):
        """create context and vectors for the document"""
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(content.split("\n"))
        for i, (text, emb) in enumerate(zip(content.split("\n"), embeddings)):
            self.vectors[i] = {"embeddings": emb, "text": text}
        return self


class PyfficeDocumentManager(PyfficeDocument):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDocumentManager")).override(cfg)
        self.store = conql.Doc()
        self.documents = {}

    def add_document(self, document):
        """Add a child document to this manager.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.documents[document.name] = document
        return self

    def del_document(self, name):
        """Remove the document.
        
        Args:
            name: Parameter.
        
        Returns:
            Self for chaining.
        """
        if name not in self.documents:
            return self
        del self.documents[name]
        return self

    def get_context(self):
        """Return the current document context as a string.
        
        Returns:
            Self for chaining.
        """
        return super().get_context()

    def get_document(self, name):
        """Return the document.
        
        Args:
            name: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self.documents[name]

    def load_document(self, document=None):
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
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
        """Search.
        
        Args:
            term: Parameter.
        
        Returns:
            Self for chaining.
        """
        result = self.search_documents(term)
        if result is None:
            return None
        return self.documents[result]

    def search_documents(self, term):
        """Search documents.
        
        Args:
            term: Parameter.
        
        Returns:
            Self for chaining.
        """
        for name, document in self.documents.items():
            if document.search(term):
                return name
        return None

    def set_documents(self, documents):
        """Set the documents.
        
        Args:
            documents: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.documents = documents
        return self

    def set_doc_types(self, doc_types):
        """Set the doc types.
        
        Args:
            doc_types: Parameter.
        
        Returns:
            Self for chaining.
        """
        if doc_types is None:
            doc_types = []
        self.doc_types = doc_types
        return self

    def to_dict(self):
        """Convert this document to dict.
        
        Returns:
            Self for chaining.
        """
        doc = super().to_dict() or {}
        if "data" not in doc.keys():
            doc["data"] = {}
        doc["data"]["documents"] = []
        if self.documents is None:
            return doc
        for name, document in self.documents.items():
            doc["data"]["documents"].append({name: document.to_dict()})
        return doc


class PyfficeDeque(PyfficeDocument, deque):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        PyfficeDocument.__init__(self, self.config)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeDeque")).override(cfg)
        self.max_items = None
        self.set_max_items()
        self.history = deque()

    def append(self, item):
        """Append.
        
        Args:
            item: Parameter.
        
        Returns:
            Self for chaining.
        """
        if self.max_items is not None:
            if len(self) >= self.max_items:
                self.history.append(self.popleft())
        super().append(item)

    def appendleft(self, item):
        """Add item to the left side of the deque."""
        if self.max_items is not None:
            if len(self) >= self.max_items:
                self.history.append(self.pop())
        super().appendleft(item)

    def set_max_items(self, max_items=None):
        """Set the max items.
        
        Args:
            max_items: Parameter.
        
        Returns:
            Self for chaining.
        """
        if max_items is None:
            max_items = self.config.dikt.get("max_items", 10)
        self.max_items = max_items
        return self

    def to_dict(self):
        """Convert this document to dict.
        
        Returns:
            Self for chaining.
        """
        doc = super().to_dict()
        doc["data"]["history"] = [x for x in self.history]
        doc["data"]["max_items"] = self.max_items
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
