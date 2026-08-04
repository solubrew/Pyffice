# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
                Pyffice - Polygot Office Document Package
                Creates YAML versions of office files with bidirectional conversion.
                AI Agent enhanced with tool-ready functions.
        version: 0.0.1.0.1.0
        authority: filesystem
        security2
        <(: seclvlWT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from __future__ import annotations

import logging
from os.path import dirname, join, expanduser
from typing import Any, Optional

# ======================================3rd Party Library Modules=====================================================||
from kahndor.kahndor import Instruct
from kahndor.logma import Logma
from pyffice.document import PyfficeDocumentManager
from pyffice.analytics.sources import PyfficeSourceManager
from pyffice.calendars.calendars import PyfficeCalendar
from pyffice.charts.charts import PyfficeChart
from pyffice.matrix.spreadsheet import PyfficeSpreadSheet
from pyffice.ports.noteports import PyfficePortCherryTree
from pyffice.contacts.contacts import PyfficeRolodex, PyfficeContact
from pyffice.forms.forms import PyfficeFormsManager
from pyffice.images.images import PyfficeImage
from pyffice.images.sketches import PyfficeSketch
from pyffice.images.pdfs import PyfficePDF
from pyffice.notebooks.notebooks import PyfficeNotebook
from pyffice.matrix.matrix import PyfficeMatrix
from pyffice.script.script import PyfficeScript
from pyffice.web.prompts import PyfficePromptsManager
from pyffice.web.url import PyfficeURLLibrary
from pyffice.web.web import PyfficeWebBrowser
from pyffice.filesystems.filesystems import PyfficeFileSystem

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logger = logging.getLogger(__name__)
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "pyffice.yaml")


class PyfficeCodexError(Exception):
    """Base exception for PyfficeCodex errors."""

    pass


class DocumentNotFoundError(PyfficeCodexError):
    """Raised when a requested document is not found."""

    pass


class InitializationError(PyfficeCodexError):
    """Raised when PyfficeCodex initialization fails."""

    pass


# T-NEW-055: domain-specific exceptions for the 18 sites that
# previously raised bare Exception(...). All subclass
# PyfficeCodexError so callers can catch the base class.
class UnknownLocationError(PyfficeCodexError):
    """Raised when a filesystem / image location cannot be resolved."""


class UnknownFileTypeError(PyfficeCodexError):
    """Raised when a file's format cannot be detected from its extension/path."""


class UnknownMediaTypeError(PyfficeCodexError):
    """Raised when a media type is not recognized."""


class UnknownSyntaxError(PyfficeCodexError):
    """Raised when a spreadsheet syntax cannot be parsed."""


class UnknownReturnFormatError(PyfficeCodexError):
    """Raised when a return format is not recognized."""


class ColumnNotFoundError(PyfficeCodexError):
    """Raised when a spreadsheet column is missing."""


class TooManyParametersError(PyfficeCodexError):
    """Raised when a formula receives more parameters than allowed."""


class InvalidParameterTypeError(PyfficeCodexError):
    """Raised when a formula parameter has the wrong type."""


class InvalidConfigurationError(PyfficeCodexError):
    """Raised when configuration is missing required fields or has invalid values."""


class MissingPathError(PyfficeCodexError):
    """Raised when a required path is None or empty."""


class PyfficeCodex(PyfficeDocumentManager):
    """A Pyffice Book is a container that can hold multiple instances and types of Pyffice Top Level Documents
    SERIALIZATION_VERSION = (1, 0, 0)

    AI Agent Enhanced:
        - to_yaml() -> str: Convert entire codex to YAML string
        - from_yaml(yaml_str) -> PyfficeCodex: Load from YAML string
        - to_summary() -> dict: Get token-efficient summary
        - to_json_schema() -> dict: Get JSON Schema for LLM validation
    """

    VERSION: str = "0.0.1.0.1.0"
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg: Optional[dict[str, Any]] = None) -> None:
        """Initialize PyfficeCodex with optional configuration."""
        try:
            super().__init__(cfg)
            self.config.override(Instruct(pxcfg).select("PyfficeCodex")).override(cfg)
            self.url_library = PyfficeURLLibrary(cfg)
            self.contacts: Optional[PyfficeRolodex] = None
            self.documents: dict = {}
            self.forms_manager: Optional[PyfficeFormsManager] = None
            self.imports: dict = {}
            # self.source_manager: Optional[PyfficeSources] = None
            self.source: Any = None
        except (TypeError, AttributeError, KeyError) as e:
            raise InitializationError(f"Failed to initialize PyfficeCodex: {e}") from e

    @classmethod
    def from_yaml(cls, yaml_str: str, cfg: Optional[dict[str, Any]] = None) -> PyfficeCodex:
        """Load a codex from a YAML string."""
        import yaml

        data = yaml.safe_load(yaml_str)
        codex = cls(cfg)
        codex.documents = data.get("documents", {})
        codex.imports = data.get("imports", {})
        return codex

    def add_pydocument(self, pydoc: Any) -> Any:
        """Add a Pyffice document to the codex."""
        try:
            if isinstance(pydoc, str):
                pydoc = self.load_pydocument(pydoc)
            self.documents.append(pydoc)
            return pydoc
        except (AttributeError, OSError, ValueError) as e:
            raise PyfficeCodexError(f"Failed to add document: {e}") from e

    def add_url(self, url: str) -> Optional[str]:
        """Add a URL to the library."""
        if self.url_library is None:
            raise PyfficeCodexError("URL library not initialized")
        try:
            return self.url_library.add_url(url)
        except (ValueError, OSError, AttributeError) as e:
            raise PyfficeCodexError(f"Failed to add URL: {e}") from e

    def get_rolodex(self) -> Any:
        """Return the contacts rolodex (may be None if uninitialized)."""
        return self.contacts

    def get_url(self, url_id: Optional[str] = None) -> Optional[Any]:
        """Get URL by ID."""
        if self.url_library is None:
            return None
        return self.url_library.get_url_by_id(url_id)

    def import_cherrytree(self, cfg: dict[str, Any]) -> Optional[Any]:
        """Import from CherryTree format."""
        logma.info(f"CFG {cfg}")
        cherrytree = PyfficePortCherryTree(cfg)
        logma.info(f"CherryTree: {cherrytree.file_path}")
        import_doc = cherrytree.file_import()
        cherrytree.file_export(join(expanduser("~"), "_work", "cherrytree.yaml"))
        self.imports[cherrytree.did] = import_doc
        return cherrytree

    def import_pdf(self, cfg: dict[str, Any]) -> None:
        """Import from PDF format."""
        logger.info(f"PDF import not yet implemented: {cfg}")

    def import_session(self, cfg: dict[str, Any]) -> None:
        """Import from session."""
        logger.info(f"Session import not yet implemented: {cfg}")

    def import_text(self, cfg: dict[str, Any]) -> None:
        """Import from text format."""
        logger.info(f"Text import not yet implemented: {cfg}")

    def init_browser(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a web browser document."""
        cfg = cfg or {}
        cfg["codex"] = self
        browser = PyfficeWebBrowser(cfg)
        self.documents[browser.did] = browser
        return browser

    def init_calendar(self, cfg: Optional[dict[str, Any]] = None, pid=None) -> Optional[Any]:
        """Initialize a calendar document."""
        cfg = cfg or {}
        cfg["codex"] = self
        cfg["workbook_parent_id"] = pid
        calendar = PyfficeCalendar(cfg)
        self.documents[calendar.did] = calendar
        return calendar

    def init_chart(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a chart document."""
        cfg = cfg or {}
        cfg["codex"] = self
        chart = PyfficeChart(cfg)
        self.documents[chart.did] = chart
        return chart

    def init_contacts(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a contacts/rolodex document."""
        cfg = cfg or {}
        cfg["codex"] = self
        self.contacts = PyfficeRolodex(cfg)
        self.documents[self.contacts.did] = self.contacts
        return self.contacts

    def init_contact(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a contacts/rolodex document."""
        cfg = cfg or {}
        cfg["codex"] = self
        contact = PyfficeContact(cfg)
        if self.contacts is None:
            cfg = {}
            self.init_contacts(cfg)
        self.contacts.add_contact(contact)
        return contact

    def init_files(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a filesystem document."""
        cfg = cfg or {}
        cfg["codex"] = self
        files = PyfficeFileSystem(cfg)
        self.documents[files.did] = files
        return files

    def init_form(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a form document."""
        cfg = cfg or {}
        cfg["codex"] = self
        if self.forms_manager is None:
            self.init_forms_manager(cfg)
        form = self.forms_manager.create_new_form(cfg)
        self.documents[form.did] = form
        return form

    def init_forms_manager(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize forms manager."""
        cfg = cfg or {}
        cfg["codex"] = self
        self.forms_manager = PyfficeFormsManager(cfg)
        self.documents[self.forms_manager.did] = self.forms_manager
        return self.forms_manager

    def init_image(self, cfg: Optional[dict[str, Any]] = None, pid=None) -> Optional[Any]:
        """Initialize an image document."""
        cfg = cfg or {}
        cfg["codex"] = self
        cfg["workbook_parent_id"] = pid
        image = PyfficeImage(cfg)
        self.documents[image.did] = image
        return image

    def init_matrix(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a spreadsheet/matrix document."""
        cfg = cfg or {}
        cfg["codex"] = self
        matrix = PyfficeMatrix(cfg)
        self.documents[matrix.did] = matrix
        cfg = {}
        spreadsheet = self.init_spreadsheet(cfg, matrix.did)
        return matrix

    def init_note(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a note document."""
        cfg = cfg or {}
        cfg["codex"] = self
        note = PyfficeScript(cfg)
        self.documents[note.did] = note
        return note

    def init_notebook(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a notebook document."""
        cfg = cfg or {}
        cfg["codex"] = self
        notebook = PyfficeNotebook(cfg)
        self.documents[notebook.did] = notebook
        return notebook

    def init_pdf(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a PDF document."""
        cfg = cfg or {}
        cfg["codex"] = self
        pdf = PyfficePDF(cfg)
        self.documents[pdf.did] = pdf
        return pdf

    def init_prompt(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a prompts manager."""
        cfg = cfg or {}
        cfg["codex"] = self
        prompts = PyfficePromptsManager(cfg)
        self.documents[prompts.did] = prompts
        return prompts

    def init_script(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a script document."""
        cfg = cfg or {}
        cfg["codex"] = self
        script = PyfficeScript(cfg)
        self.documents[script.did] = script
        return script

    def init_sketch(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a sketch/diagram document."""
        cfg = cfg or {}
        cfg["codex"] = self
        sketch = PyfficeSketch(cfg)
        self.documents[sketch.did] = sketch
        return sketch

    def init_spreadsheet(self, cfg: Optional[dict[str, Any]] = None, pid=None) -> Optional[Any]:
        """Initialize a spreadsheet document."""
        cfg = cfg or {}
        cfg["codex"] = self
        cfg["workbook_parent_id"] = pid
        sheet = PyfficeSpreadSheet(cfg)
        self.documents[sheet.did] = sheet
        return sheet

    def init_source_manager(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize source manager."""
        cfg = cfg or {}
        cfg["codex"] = self
        self.source_manager = PyfficeSourceManager(cfg)
        self.documents[self.source_manager.did] = self.source_manager
        return self.source_manager

    def init_source(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a data source."""
        cfg = cfg or {}
        cfg["codex"] = self
        if self.source_manager is None:
            self.init_source_manager(cfg)
        self.source = self.source_manager.create_new_source(cfg)
        self.documents[self.source.did] = self.source
        return self.source

    def load_document(self, document: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Load documents into the codex."""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        # lookup and initialize the proper Pyffice Document type
        self.set_documents(document.get("documents", {}))
        self.set_imports(document.get("imports", {}))
        return document

    def save(
        self, path: Optional[str] = None, syntax: Optional[str] = None, encrypt_key: Optional[str] = None
    ) -> PyfficeCodex:
        """Save the codex to a file."""
        if path is None:
            raise PyfficeCodexError("Save path is required")

        import yaml
        from pathlib import Path

        # Determine syntax and get appropriate serializer
        syntax = syntax or "yaml"

        # Serialize the codex
        data = self.to_dict()

        # Write to file
        file_path = Path(path)
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False)

        logger.info(f"Saved codex to {path}")
        return self

    def set_imports(self, imports: Optional[dict[str, Any]] = None) -> PyfficeCodex:
        """Set imports with change tracking."""
        if imports is None:
            imports = {}
        if imports != self.imports:
            self.add_change("imports", self.imports, imports)
            self.imports = imports
        return self

    def set_storage(self) -> None:
        """Set storage location for the codex (folder or database)."""
        logger.info("set_storage not yet implemented")

    def to_chunks(self, chunk_size: int = 1000, overlap: int = 100) -> list[dict[str, Any]]:
        """Split codex into embedding-ready chunks.

        Args:
            chunk_size: Target size per chunk in characters
            overlap: Overlap between chunks in characters

        Returns:
            List of chunk dictionaries with 'content' and 'metadata'
        """
        chunks = []

        # Chunk each document
        for doc_id, doc in self.documents.items():
            doc_content = str(doc)
            doc_chunks = self._chunk_text(doc_content, chunk_size, overlap)
            for i, chunk in enumerate(doc_chunks):
                chunks.append(
                    {
                        "content": chunk,
                        "metadata": {
                            "doc_id": doc_id,
                            "doc_type": type(doc).__name__,
                            "chunk_index": i,
                            "total_chunks": len(doc_chunks),
                        },
                    }
                )

        # Chunk imports
        if self.imports:
            imports_content = str(self.imports)
            import_chunks = self._chunk_text(imports_content, chunk_size, overlap)
            for i, chunk in enumerate(import_chunks):
                chunks.append(
                    {
                        "content": chunk,
                        "metadata": {
                            "source": "imports",
                            "chunk_index": i,
                            "total_chunks": len(import_chunks),
                        },
                    }
                )

        return chunks

    # ============================================================================
    # AI Agent Enhancement Methods
    # ============================================================================
    def to_json_schema(self) -> dict[str, Any]:
        """Get JSON Schema for LLM output validation."""
        return {
            "type": "object",
            "properties": {
                "version": {"type": "string", "description": "Pyffice version"},
                "documents": {
                    "type": "object",
                    "description": "Dictionary of documents by ID",
                    "additionalProperties": {
                        "type": "object",
                        "description": "Document properties",
                    },
                },
                "document_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of document type names",
                },
                "import_count": {"type": "integer", "description": "Number of imports"},
            },
            "required": ["version", "document_count"],
        }

    def to_summary(self) -> dict[str, Any]:
        """Get a token-efficient summary of the codex for AI agents."""
        doc_types = []
        for doc_id, doc in self.documents.items():
            doc_types.append(type(doc).__name__)

        return {
            "version": self.VERSION,
            "document_count": len(self.documents),
            "document_types": doc_types,
            "has_contacts": self.contacts is not None,
            "has_forms_manager": self.forms_manager is not None,
            "import_count": len(self.imports),
        }

    def to_yaml(self) -> str:
        """Convert the entire codex to a YAML string for serialization."""
        import yaml

        # Build serializable dict
        data = {
            "version": self.VERSION,
            "documents": {},
            "imports": self.imports,
            "contacts": None,
        }

        # Serialize each document - skip ones that fail
        for doc_id, doc in self.documents.items():
            try:
                if hasattr(doc, "to_dict"):
                    data["documents"][doc_id] = doc.to_dict()
                else:
                    data["documents"][doc_id] = {"type": type(doc).__name__}
            except (AttributeError, TypeError) as e:
                # Skip documents that can't be serialized
                data["documents"][doc_id] = {
                    "type": type(doc).__name__,
                    "_error": str(e),
                }

        if self.contacts:
            try:
                if hasattr(self.contacts, "to_dict"):
                    data["contacts"] = self.contacts.to_dict()
            except (AttributeError, TypeError) as e:
                data["contacts"] = {"type": "PyfficeRolodex", "_error": str(e)}

        return yaml.dump(data, default_flow_style=False)

    def update(self) -> Any:
        """Update the codex with new documents."""
        return PyfficeUpdater()

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> list[str]:
        """Split text into overlapping chunks."""
        if len(text) <= chunk_size:
            return [text] if text else []

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
