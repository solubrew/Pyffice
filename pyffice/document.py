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
try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# ======================================Solutions Brewer Library Modules==============================================||
try:
    from condor import condor

    CONDOR_AVAILABLE = True
except ImportError:
    condor = None
    CONDOR_AVAILABLE = False
from ogma.logma import Logma

# from squirl.orgnql import conql, yonql
from subtrix.utilities import uuid
from pycurity.pytime import PyTime
from pyffice.tags.tags import PyfficeTag
from pyffice.updates.updates import PyfficeUnitUpdate, PyfficeDocumentUpdate
from pycurity.pyhash import text_hashing_function

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
# logma.off()
CHANGE_LIMIT = 100
# ====================================================================================================================||

__all__ = [
    "PyfficeUnit",
    "PyfficeDocument",
    "PyfficeDocumentManager",
    "PyfficeDeque",
    "SENTENCE_TRANSFORMERS_AVAILABLE",
    "CONDOR_AVAILABLE",
]

pxcfg = join(here, "_data_", "document.yaml")


class PyfficeUnit(object):
    """Base unit class for all Pyffice documents.

    PyfficeUnit is the foundational class that provides core functionality for
    document versioning, change tracking, and metadata management.

    Attributes:
        VERSION: Version string for the class format.
        config: Configuration dictionary for the unit.
        author: Author of the document.
        did: Unique document identifier.
        name: Document name.
        description: Document description.
        content: Main content of the document.
        context: Serialized context for searching/embedding.
        hash: Content hash for deduplication.
        tags: List of PyfficeTag objects.
        version: Integer version number.
        changes: List of change records for undo/redo.
        redos: List of undone changes for redo operations.

    Example:
        >>> unit = PyfficeUnit()
        >>> unit.set_name("My Document").set_author("John Doe")
        >>> unit.set_content("Hello world")
        >>> print(unit.get_hash())
    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """Initialize a new PyfficeUnit.

        Args:
            cfg: Optional configuration dictionary. Defaults to None.
        """
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
        try:
            self.time = PyTime()  # TODO build override to allow for time object to be common across application
        except Exception:
            import datetime

            self.time = None  # Fallback - time functions limited
        self.version = 0
        self.versions = None

    def add_change(self, label, value, new_value, action="set", params=None):
        """Record a change to the unit for undo/redo tracking.

        Args:
            label: The attribute name that changed.
            value: The original value.
            new_value: The new value after the change.
            action: The type of change - "set" or "add". Defaults to "set".
            params: Optional additional parameters. Defaults to None.

        Returns:
            self: Returns self for method chaining.

        Example:
            >>> unit.add_change("name", "old_name", "new_name")
        """
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
            self.changes.append({"action": action, "label": label, "value": deepcopy(value), "new_value": new_value})
        elif action == "set":
            self.changes.append({"action": action, "label": label, "value": value, "new_value": new_value})
        self.changes = self.changes[-change_limit:]
        return self

    def add_editor(self):
        """Add an editor to the document.

        Returns:
            self: Returns self for method chaining.
        """
        return self

    def add_tag(self, tag_name, description=""):
        """Add a tag to the document.

        Args:
            tag_name: Name of the tag to add.
            description: Optional description for the tag. Defaults to "".

        Returns:
            self: Returns self for method chaining.
        """
        cfg = {}
        tag = PyfficeTag(cfg)
        self.tags.append(tag)
        return self

    def del_editor(self, dex):
        """Remove an editor from the document by index.

        Args:
            dex: Index of the editor to remove.

        Returns:
            self: Returns self for method chaining.
        """
        return self

    def del_reference(self, reference):
        """Remove a reference from the document.

        Args:
            reference: Reference dictionary or string to remove.

        Returns:
            self: Returns self for method chaining.
        """
        return self

    def del_tag(self, tag):
        """Remove a tag from the document.

        Args:
            tag: PyfficeTag object or tag name to remove.

        Returns:
            self: Returns self for method chaining.
        """
        tags = self.tags
        self.tags.remove(tag)
        self.add_change("tags", tags, self.tags)
        return self

    def get_context(self):
        """Get the serialized context of the document.

        Returns:
            str: JSON string representation of the document.
        """
        self.context = self.to_string()
        return self.context

    def get_hash(self):
        """Generate and return a hash of the document content.

        Returns:
            str: Hash string of the document context.
        """
        self.hash = text_hashing_function(self.context)
        return self.hash

    def get_tags(self):
        """Get the list of tags attached to the document.

        Returns:
            list: List of PyfficeTag objects.
        """
        return self.tags

    def increment_version(self):
        """Increment the document version number.

        Returns:
            self: Returns self for method chaining.
        """
        logma.info(f"Increment Version {self.version}")
        # self.version = int(self.version)
        # self.version += 1
        return self

    def load_unit(self, unit=None):
        """Load unit data from a dictionary or JSON string.

        Args:
            unit: Dictionary or JSON string containing unit data. Defaults to None.

        Returns:
            self: Returns self for method chaining.

        Raises:
            ValueError: If unit cannot be parsed as valid JSON.
        """
        # logma.inspect_caller()
        logma.info(f"Load Unit {unit}")
        if isinstance(unit, str):
            unit = j.loads(unit)
        unit = self.unit.override(unit).dikt
        self.versions = self.config.dikt.get("versions", {})
        # unit = self.update_unit_structure(unit)
        try:
            self.time = PyTime()
        except Exception:
            import datetime

            self.time = None  # Fallback - time functions limited
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
            self: Returns self for method chaining.

        Raises:
            IndexError: If there are no changes to redo.
        """
        change = self.redos.pop()
        setattr(self, change["label"], change["new_value"])
        if change["action"] == "set":
            self.add_change(change["label"], change["value"], change["new_value"], "set")
        return self

    def set_author(self, author):
        """Set the author of the document.

        Args:
            author: Author name string. Defaults to empty string if None.

        Returns:
            self: Returns self for method chaining.
        """
        if author is None:
            author = ""
        if author != self.author:
            self.add_change("author", self.author, author)
            self.author = author
        return self

    def set_change_limit(self, limit=None):
        """Set the maximum number of changes to track.

        Args:
            limit: Maximum number of changes. Defaults to CHANGE_LIMIT if None.

        Returns:
            self: Returns self for method chaining.
        """
        if limit != self.change_limit:
            self.add_change("change_limit", self.change_limit, limit)
            self.change_limit = limit
        return self

    def set_changes(self, changes):
        """Set the list of tracked changes.

        Args:
            changes: List of change dictionaries. Defaults to empty list if None.

        Returns:
            self: Returns self for method chaining.
        """
        if changes is None:
            changes = []
        if changes != self.changes:
            self.add_change("changes", self.changes, changes)
            self.changes = changes
        return self

    def set_context(self, context):
        """Set the document context (used for searching/embedding).

        Args:
            context: Context string. Defaults to empty string if None.

        Returns:
            self: Returns self for method chaining.
        """
        if context is None:
            context = ""
        if context != self.context:
            self.add_change("context", self.context, context)
            self.context = context
        return self

    def set_creon(self, creon=None):
        """Set the creation timestamp.

        Args:
            creon: ISO datetime string. Defaults to current time if None.

        Returns:
            self: Returns self for method chaining.
        """
        if creon is None:
            if self.time is not None:
                creon = self.time.get_current_datetime_str()
            else:
                import datetime

                creon = datetime.datetime.now().isoformat()
        if creon != self.creon:
            self.add_change("creon", self.creon, creon)
            self.creon = creon
        return self

    def set_data(self, data):
        """Set arbitrary data on the unit.

        Args:
            data: Data dictionary to store.

        Returns:
            self: Returns self for method chaining.
        """
        if data != self.data:
            self.add_change("data", self.data, data)
            self.data = data
        return self

    def set_description(self, description):
        """Set the document description.

        Args:
            description: Description string. Defaults to empty string if None.

        Returns:
            self: Returns self for method chaining.
        """
        if description is None:
            description = ""
        if description != self.description:
            self.add_change("description", self.description, description)
            self.description = description
        return self

    def set_did(self, did=None):
        """Set the unique document identifier.

        Args:
            did: UUID string. Auto-generates UUID if None.

        Returns:
            self: Returns self for method chaining.
        """
        if did is None:
            did = uuid()
        if did != self.did:
            self.add_change("did", self.did, did)
            self.did = did
        return self

    def set_editors(self, editors):
        """Set the list of editors.

        Args:
            editors: List of editor names. Defaults to empty list if None.

        Returns:
            self: Returns self for method chaining.
        """
        if editors is None:
            editors = []
        if editors != self.editors:
            self.add_change("editors", self.editors, editors)
            self.editors = editors
        return self

    def set_encoding(self, encoding=None):
        """Set the text encoding.

        Args:
            encoding: Encoding string (e.g., "utf-8"). Defaults to "utf-8" if None.

        Returns:
            self: Returns self for method chaining.
        """
        if encoding is None:
            encoding = "utf-8"
        if encoding != self.encoding:
            self.add_change("encoding", self.encoding, encoding)
            self.encoding = encoding
        return self

    def set_hash(self, hash_):
        """Set the content hash.

        Args:
            hash_: Hash string. Auto-generates from context if None.

        Returns:
            self: Returns self for method chaining.
        """
        if hash_ is None:
            hash_ = text_hashing_function(self.context)
        logma.info(f"Hash {hash_}")
        # TODO need to determine what parts get hased and when/where that happens
        if hash_ != self.hash:
            self.add_change("hash", self.hash, hash_)
            self.hash = hash_
        return self

    def set_location(self, location):
        """Set the document location.

        Args:
            location: Location string ("internal" or "external"). Defaults to "internal".

        Returns:
            self: Returns self for method chaining.
        """
        if location is None:
            location = "internal"
        if location != self.location:
            self.add_change("location", self.location, location)
            self.location = location
        return self

    def set_meta_data(self, meta_data):
        """Set metadata dictionary.

        Args:
            meta_data: Dictionary of metadata.

        Returns:
            self: Returns self for method chaining.
        """
        if meta_data != self.meta_data:
            self.add_change("meta_data", self.meta_data, meta_data)
            self.meta_data = meta_data
        return self

    def set_modon(self, modon=None):
        """Set the last modified timestamp.

        Args:
            modon: ISO datetime string. Defaults to current time if None.

        Returns:
            self: Returns self for method chaining.
        """
        if modon is None:
            if self.time is not None:
                modon = self.time.get_current_datetime_str()
            else:
                import datetime

                modon = datetime.datetime.now().isoformat()
        if modon != self.modon:
            self.add_change("modon", self.modon, modon)
            self.modon = modon
        return self

    def set_name(self, name):
        """Set the document name.

        Args:
            name: Name string. Defaults to did if None.

        Returns:
            self: Returns self for method chaining.
        """
        if name is None:
            name = self.did
        if name != self.name:
            self.add_change("name", self.name, name)
            self.name = name
        return self

    def set_path(self, path):
        """Set the file path.

        Args:
            path: File path string. Defaults to empty string if None.

        Returns:
            self: Returns self for method chaining.
        """
        if path is None:
            path = ""
        if path != self.path:
            self.add_change("path", self.path, path)
            self.path = path
        return self

    def set_redos(self, redos):
        """Set the redo stack.

        Args:
            redos: List of undone changes.

        Returns:
            self: Returns self for method chaining.
        """
        if redos != self.redos:
            self.add_change("redos", self.redos, redos)
            self.redos = redos
        return self

    def set_references(self, references):
        """Set the list of references.

        Args:
            references: List of reference dictionaries. Defaults to empty list.

        Returns:
            self: Returns self for method chaining.
        """
        if references is None:
            references = []
        if references != self.references:
            self.add_change("references", self.references, references)
            self.references = references
        return self

    def set_saved(self, saved):
        """Set the saved status.

        Args:
            saved: Boolean indicating if document is saved.

        Returns:
            self: Returns self for method chaining.
        """
        if saved != self.is_saved:
            self.add_change("saved", self.is_saved, saved)
            self.is_saved = saved
        return self

    def set_syntax(self, syntax):
        """Set the syntax/type for content.

        Args:
            syntax: Syntax string (e.g., "plain-text", "markdown"). Defaults to "plain-text".

        Returns:
            self: Returns self for method chaining.
        """
        if syntax is None:
            syntax = "plain-text"
        if syntax != self.syntax:
            self.add_change("syntax", self.syntax, syntax)
            self.syntax = syntax
        return self

    def set_tags(self, tags):
        """Set the list of tags.

        Args:
            tags: List of PyfficeTag objects. Defaults to empty list if None.

        Returns:
            self: Returns self for method chaining.
        """
        if tags is None:
            tags = []
        if tags != self.tags:
            self.add_change("tags", self.tags, tags)
            self.tags = tags
        return self

    def set_version(self, version):
        """Set the version number.

        Args:
            version: Integer version number. Defaults to 0 if None.

        Returns:
            self: Returns self for method chaining.
        """
        if version is None:
            version = 0
        if version != self.version:
            self.add_change("version", self.version, version)
            self.version = version
        return self

    def to_dict(self):
        """Convert the unit to a dictionary representation.

        Includes document ID, name, description, metadata (author, editors,
        encoding, hash, location, path, syntax), creation/modification timestamps,
        and content.

        Returns:
            dict: Dictionary representation of the unit.

        Note:
            Subclasses should override this method to include additional fields.
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
        doc["unit"] = {"content": self.content}
        return doc

    def to_html(self):
        """Convert the document to HTML format.

        Returns:
            str: HTML representation of the document, or None if not implemented.
        """
        return self.html

    def to_json_schema(self) -> dict:
        """Convert the document to JSON Schema format.

        Returns:
            dict: JSON Schema representation of the document.

        Example:
            >>> doc = PyfficeDocument()
            >>> doc.set_name("Test").set_content("Hello world")
            >>> schema = doc.to_json_schema()
            >>> print(schema["properties"]["name"]["default"])
            Test
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": self.name or "PyfficeDocument",
            "type": "object",
            "properties": {
                "did": {"type": "string", "default": self.did},
                "name": {"type": "string", "default": self.name},
                "description": {"type": "string", "default": self.description},
                "content": {"type": "string", "default": self.content},
                "author": {"type": "string", "default": self.author},
                "document_type": {"type": "string", "default": self.document_type},
                "file_path": {"type": "string", "default": self.file_path},
                "version": {"type": "integer", "default": self.version},
            },
            "required": [],
        }

    def to_string(self):
        """Convert the unit to a JSON string.

        Returns:
            str: JSON string representation of the unit.
        """
        return j.dumps(self.to_dict())

    def to_yaml_string(self):
        """Convert the unit to a YAML string.

        Returns:
            str: YAML string representation of the unit.
        """
        import yaml

        return yaml.dump(self.to_dict())

    @classmethod
    def from_yaml_string(cls, yaml_string):
        """Create a unit from a YAML string.

        Args:
            yaml_string: YAML string to parse.

        Returns:
            PyfficeUnit: New unit instance with loaded data.
        """
        import yaml

        data = yaml.safe_load(yaml_string)
        unit = cls()
        unit.load_unit(data)
        return unit

    def to_chunks(self, chunk_size: int = 512, overlap: int = 50) -> list[dict]:
        """Convert the document content into chunks for embedding/vector DB.

        Args:
            chunk_size: Maximum size of each chunk in characters. Default: 512.
            overlap: Number of overlapping characters between chunks. Default: 50.

        Returns:
            list[dict]: List of chunk dictionaries with 'text', 'start', 'end',
                       'chunk_index', and 'total_chunks' keys.

        Example:
            >>> doc = PyfficeDocument()
            >>> doc.set_content("Long content here...")
            >>> chunks = doc.to_chunks(chunk_size=256)
            >>> print(chunks[0]["text"])
            Long content here...
        """
        content = self.content or ""
        if not content:
            return []

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(content):
            end = start + chunk_size
            chunk_text = content[start:end]

            chunks.append(
                {
                    "text": chunk_text,
                    "start": start,
                    "end": min(end, len(content)),
                    "chunk_index": chunk_index,
                    "total_chunks": 0,  # Will be updated after counting
                    "did": self.did,
                    "name": self.name,
                }
            )

            start = end - overlap
            chunk_index += 1

        # Update total_chunks for all
        total = len(chunks)
        for chunk in chunks:
            chunk["total_chunks"] = total

        return chunks

    def to_summary(self, max_length: int = 200, format: str = "text") -> str | dict:
        """Generate a token-efficient summary of the document.

        Args:
            max_length: Maximum length of summary in characters. Default: 200.
            format: Output format - "text", "json", "yaml", or "md". Default: "text".

        Returns:
            str | dict: Summary in the requested format.

        Example:
            >>> doc = PyfficeDocument()
            >>> doc.set_content("Long document content...")
            >>> summary = doc.to_summary()
            >>> print(summary["summary"])
            Long document content...
            >>> md_summary = doc.to_summary(format="md")
            >>> print(md_summary)
            ## Summary

            - **Words**: 3
            - **Characters**: 22
            - **Document**: None
        """
        content = self.content or ""
        word_count = len(content.split()) if content else 0
        char_count = len(content)

        # Simple truncation for now - can be enhanced with LLM
        if len(content) <= max_length:
            summary_text = content
        else:
            # Try to end at a word boundary
            summary_text = content[:max_length]
            last_space = summary_text.rfind(" ")
            if last_space > max_length * 0.8:  # If we're past 80% of max
                summary_text = summary_text[:last_space]
            summary_text += "..."

        summary_dict = {
            "summary": summary_text,
            "word_count": word_count,
            "char_count": char_count,
            "has_full_content": len(content) <= max_length,
            "did": self.did,
            "name": self.name,
        }

        # Return in requested format
        if format == "json":
            return j.dumps(summary_dict, indent=2)
        elif format == "yaml":
            import yaml

            return yaml.dump(summary_dict)
        elif format == "md":
            md_lines = [
                "## Summary",
                "",
                f"**Summary**: {summary_dict['summary']}",
                "",
                f"- **Words**: {summary_dict['word_count']}",
                f"- **Characters**: {summary_dict['char_count']}",
                f"- **Has Full Content**: {summary_dict['has_full_content']}",
                f"- **Document ID**: {summary_dict['did']}",
                f"- **Name**: {summary_dict['name']}",
            ]
            return "\n".join(md_lines)
        else:
            # Default to dict for backward compatibility
            return summary_dict

    def to_md(self) -> str:
        """Convert the document to Markdown format.

        Returns:
            str: Markdown representation of the document.

        Example:
            >>> doc = PyfficeDocument()
            >>> doc.set_name("My Report").set_content("Hello world")
            >>> md = doc.to_md()
            >>> print(md)
            # My Report

            Hello world
        """
        lines = []

        # Title/Name
        if self.name:
            lines.append(f"# {self.name}")
            lines.append("")

        # Metadata section
        if self.author or self.description or self.version:
            lines.append("## Metadata")
            lines.append("")
            if self.author:
                lines.append(f"**Author**: {self.author}")
            if self.description:
                lines.append(f"**Description**: {self.description}")
            if self.version:
                lines.append(f"**Version**: {self.version}")
            if self.did:
                lines.append(f"**ID**: {self.did}")
            lines.append("")

        # Content
        if self.content:
            lines.append("## Content")
            lines.append("")
            lines.append(self.content)
            lines.append("")

        # Tags
        if self.tags and len(self.tags) > 0:
            lines.append("## Tags")
            lines.append("")
            for tag in self.tags:
                if hasattr(tag, "name"):
                    lines.append(f"- {tag.name}")
            lines.append("")

        return "\n".join(lines)

    def undo_change(self):
        """Undo the last change (pop from changes list, push to redos).

        Returns:
            self: Returns self for method chaining.

        Raises:
            IndexError: If there are no changes to undo.
        """
        last_change = self.changes.pop()
        self.redos.append(last_change)
        setattr(self, last_change["label"], last_change["value"])
        return self

    def update_unit_structure(self, unit):
        """Apply structural updates to the unit.

        Args:
            unit: Unit dictionary to update.

        Returns:
            dict: Updated unit dictionary.
        """
        unit = PyfficeUnitUpdate(unit).process()
        return unit


class PyfficeDocument(PyfficeUnit):
    """Document class for file-based documents.

    PyfficeDocument extends PyfficeUnit with file handling capabilities,
    document type management, and vector embedding support.

    Attributes:
        VERSION: Version string for the class format.
        cache: Document cache.
        compatibility: Compatibility mode (e.g., "pyffice").
        document_type: Type of document (text, spreadsheet, etc.).
        file_path: Path to the file on disk.
        file_type: File extension/type.
        vectors: Dictionary of text embeddings for semantic search.

    Example:
        >>> doc = PyfficeDocument()
        >>> doc.set_name("Report").set_document_type("text")
        >>> doc.set_content("Document content here")
        >>> doc.save("/path/to/report.pyffice")
    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """Initialize a new PyfficeDocument.

        Args:
            cfg: Optional configuration dictionary. Defaults to None.
        """
        super().__init__(cfg)
        self.config = cfg if cfg is not None else {}
        self.document = {}
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
        """Export the document to a file.

        Args:
            file_: File path to export to. Defaults to self.file_path.

        Returns:
            self: Returns self for method chaining.
        """
        return self

    def file_import(self, file_type):
        """Import a file into the document.

        Args:
            file_type: Type of file to import.

        Returns:
            self: Returns self for method chaining.
        """
        return self

    def file_open(self, file_path, open_=True):
        """Open and read a file into the document.

        Args:
            file_path: Path to the file to open.
            open_: Whether to read the file content. Defaults to True.

        Returns:
            str: File content if open_ is True, None otherwise.
        """
        if file_path is None:
            file_path = self.file_path
        self.file_path = file_path
        text = None
        if open_ is True:
            with open(str(self.file_path), "r") as f:
                text = f.read()
        return text

    def load_document(self, document=None):
        """Load document data from a dictionary or JSON string.

               Args:
                   document: Dictionary or JSON string containing document data. Defaults to None.

               Returns:
                   self: Returns self for method chaining.

               Raises:
        If document cannot be            ValueError: parsed as valid JSON.
        """
        logma.info(f"Load Document {document}")
        if isinstance(document, str):
            document = j.loads(document)
        document = self.document.override(document).dikt
        self.load_unit(document)
        self.set_content(document.get("data", {}).get("content", {}))
        self.set_compatibility(document.get("meta_data", {}).get("compatibility", "pyffice"))
        self.set_document_type(document.get("meta_data", {}).get("document_type", "text"))
        self.set_data(document.get("data", {}))
        self.set_file_path(document.get("path", None))
        self.set_version(document.get("version", None))
        return self

    def update_document_time(self):
        """Update the document's modification timestamp.

        Returns:
            self: Returns self for method chaining.
        """
        self.set_modon(self.time.get_current_datetime_str())
        return self

    def save(self, path=None, syntax=None, encrypt_key=None):
        """Save the document.

        Args:
            path: Optional path to save to. Defaults to current file_path.
            syntax: Optional syntax/type for the file. Defaults to None.
            encrypt_key: Optional encryption key. Defaults to None.

        Returns:
            self: Returns self for method chaining.
        """
        self.increment_version()
        return self

    def save_copy(self, path, syntax=None, encrypt_key=None):
        """Save a copy of the document to a new location.

        Args:
            path: Path to save the copy.
            syntax: Optional syntax/type for the file. Defaults to None.
            encrypt_key: Optional encryption key. Defaults to None.

        Returns:
            self: Returns self for method chaining.
        """
        self.save_as(path, False, syntax, encrypt_key)
        return self

    def save_pyffice(self, path, syntax, encrypt_key=None):
        """Save the document in pyffice format.

        Args:
            path: Path to save the file.
            syntax: Syntax/type for the file.
            encrypt_key: Optional encryption key. Defaults to None.

        Returns:
            self: Returns self for method chaining.
        """
        if encrypt_key:
            doc = encrypt256(self.to_string(), encrypt_key)
            txtonql.Doc(doc).write(path)
        else:
            doc = self.to_dict()
            open(path, "w").write(str(doc))
        return self

    def save_as(self, path, set_file_active=True, syntax=None, encrypt_key=None):
        """Save the document to a new path.

        Args:
            path: Path to save the file.
            set_file_active: Whether to set this as the active file. Defaults to True.
            syntax: Optional syntax/type for the file. Defaults to None.
            encrypt_key: Optional encryption key. Defaults to None.

        Returns:
            self: Returns self for method chaining.
        """
        if set_file_active:
            self.file_path = path
        self.save(path, syntax, encrypt_key)
        return self

    def search_document(self, term):
        """Search for a term in the document context.

        Args:
            term: Search term string.

        Returns:
            bool: True if term found in context, False otherwise.
        """
        if term in self.get_context():
            return True
        return False

    def search_vector(self):
        """Search using vector embeddings.

        Note:
            Requires sentence_transformers to be installed.

        Returns:
            dict: Vector search results, or empty dict if not available.
        """
        return {}

    def search_word(self, term):
        """Search for a word in the document.

        Args:
            term: Word to search for.

        Returns:
            bool: True if word found, False otherwise.
        """
        return self.search_document(term)

    def set_cache(self, cache):
        """Set the document cache.

        Args:
            cache: Cache object to use.

        Returns:
            self: Returns self for method chaining.
        """
        self.cache = {}
        self.cache.load(cache)
        return self

    def set_compatibility(self, compatibility):
        """Set the compatibility mode.

        Args:
            compatibility: Compatibility string (e.g., "pyffice").

        Returns:
            self: Returns self for method chaining.
        """
        if compatibility != self.compatibility:
            self.add_change("compatibility", self.compatibility, compatibility)
            self.compatibility = compatibility
        return self
        return self

    def set_content(self, content):
        """Set the document content.

        Args:
            content: Content string to set. Defaults to empty string if None.

        Returns:
            self: Returns self for method chaining.
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

    def set_context(self, content):
        """Set the document context for searching/embedding.

        Args:
            content: Context string to set. Defaults to empty string if None.

        Returns:
            self: Returns self for method chaining.
        """
        if content is None:
            content = ""
        if content != self.context:
            self.add_change("context", self.context, content)
            # self.vectorize(content)
            self.context = content
        return self

    def set_data(self, data):
        """Set arbitrary data on the document.

        Args:
            data: Data dictionary or JSON string to set. Defaults to empty dict if None.

        Returns:
            self: Returns self for method chaining.
        """
        if data is None:
            data = {}
        if isinstance(data, str):
            data = j.loads(data)
        self.data = data
        return self

    def set_document_type(self, document_type):
        """Set the document type.

        Args:
            document_type: Type string (e.g., "text", "spreadsheet", "presentation").

        Returns:
            self: Returns self for method chaining.
        """
        if document_type != self.document_type:
            self.add_change("document_type", self.document_type, document_type)
            self.document_type = document_type
        return self

    def set_file_path(self, file_path):
        """Set the file path for the document.

        Args:
            file_path: Path string to the file. Auto-detects from config if None.

        Returns:
            self: Returns self for method chaining.
        """
        if file_path is None:
            file_path = self.config.dikt.get("file_path", "")
        file_path = str(file_path)
        if exists(file_path):
            if file_path != self.file_path:
                self.add_change("file_path", self.file_path, file_path)
                self.file_path = file_path
                self.set_location("external")
        return self

    def set_file_type(self, file_type):
        """Set the file type/extension.

        Args:
            file_type: File extension string (e.g., "pyffice", "txt", "pdf").

        Returns:
            self: Returns self for method chaining.
        """
        if file_type != self.file_type:
            self.add_change("file_type", self.file_type, file_type)
            self.file_type = file_type
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["file_path"] = self.file_path
        doc["data"] = deepcopy(doc["unit"])
        del doc["unit"]
        return doc

    def update_document_structure(self, document):
        """"""
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
    """Manager class for handling multiple Pyffice documents.

    PyfficeDocumentManager extends PyfficeDocument to manage collections
    of documents with add, delete, search, and load capabilities.

    Attributes:
        documents: Dictionary of document name -> PyfficeDocument mappings.
        doc_types: List of supported document types.
        store: Internal storage for documents.
    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """Initialize a new PyfficeDocumentManager.

        Args:
            cfg: Optional configuration dictionary. Defaults to None.
        """
        super().__init__(cfg)
        self.config = {}
        self.store = {}

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
        doc["data"]["documents"] = []
        if self.documents is None:
            return doc
        for name, document in self.documents.items():
            doc["data"]["documents"].append({name: document.to_dict()})
        return doc


class PyfficeDeque(PyfficeDocument, deque):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        PyfficeDocument.__init__(self, self.config)
        self.config = {}
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

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["data"]["history"] = [x for x in self.history]
        doc["data"]["max_items"] = self.max_items
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
