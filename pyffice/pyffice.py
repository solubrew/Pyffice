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
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from __future__ import annotations

import logging
from os.path import abspath, dirname, join, expanduser
from typing import Any, Optional
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||
# (Add imports as needed)

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor, utils
from ogma.logma import Logma
from squirl.objnql import txtonql
from squirl.orgnql import conql, yonql

# Import with error handling for optional/AI modules
try:
    from pyffice.analytics.sources import PyfficeDataSet, PyfficeDataView, PyfficeSources
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.analytics.sources' not available: {e}")
    PyfficeDataSet = PyfficeDataView = PyfficeSources = None

try:
    from pyffice.calendars.calendars import PyfficeCalendar
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.calendars' not available: {e}")
    PyfficeCalendar = None

try:
    from pyffice.charts.charts import PyfficeChart
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.charts' not available: {e}")
    PyfficeChart = None

try:
    from pyffice.config.ports import PyfficePortCherryTree
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.config.ports' not available: {e}")
    PyfficePortCherryTree = None

try:
    from pyffice.contacts.contacts import PyfficeRolodex
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.contacts' not available: {e}")
    PyfficeRolodex = None

try:
    from pyffice.document import PyfficeDocument, PyfficeDocumentManager
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.document' not available: {e}")
    PyfficeDocument = PyfficeDocumentManager = None

try:
    from pyffice.forms.forms import PyfficeForm, PyfficeFormsManager
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.forms' not available: {e}")
    PyfficeForm = PyfficeFormsManager = None

try:
    from pyffice.images.images import PyfficeImage
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.images' not available: {e}")
    PyfficeImage = None

try:
    from pyffice.diagrams.diagrams import PyfficeSketch
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.diagrams' not available: {e}")
    PyfficeSketch = None

try:
    from pyffice.images.pdfs import PyfficePDF
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.images.pdfs' not available: {e}")
    PyfficePDF = None

try:
    from pyffice.notebooks.notebooks import PyfficeNotebook
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.notebooks' not available: {e}")
    PyfficeNotebook = None

try:
    from pyffice.spreadsheet.spreadsheet import PyfficeMatrix
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.spreadsheet' not available: {e}")
    PyfficeMatrix = None

try:
    from pyffice.text.text import PyfficeScript
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.text' not available: {e}")
    PyfficeScript = None

try:
    from pyffice.web.prompts import PyfficePromptsManager
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.web.prompts' not available: {e}")
    PyfficePromptsManager = None

try:
    from pyffice.web.url import PyfficeURLLibrary
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.web.url' not available: {e}")
    PyfficeURLLibrary = None

try:
    from pyffice.web.web import PyfficeWebBrowser, PyfficeWebPage
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.web.web' not available: {e}")
    PyfficeWebBrowser = PyfficeWebPage = None

try:
    from pyffice.filesystems.filesystems import PyfficeFileSystem
except ImportError as e:
    logging.warning(f"Optional module 'pyffice.filesystems' not available: {e}")
    PyfficeFileSystem = None

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logger = logging.getLogger(__name__)
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "pyffice.yaml")


class PyfficeCodex(PyfficeDocumentManager):
    """A Pyffice Book is a container that can hold multiple instances and types of Pyffice Top Level Documents

    AI Agent Enhanced:
        - to_yaml() -> str: Convert entire codex to YAML string
        - from_yaml(yaml_str) -> PyfficeCodex: Load from YAML string
        - to_summary() -> dict: Get token-efficient summary
        - to_json_schema() -> dict: Get JSON Schema for LLM validation
    """

    VERSION: str = "0.0.1.0.1.0"

    def __init__(self, cfg: Optional[dict[str, Any]] = None) -> None:
        """Initialize PyfficeCodex with optional configuration."""
        super().__init__(cfg)
        try:
            self.config.override(condor.Instruct(pxcfg).select("PyfficeCodex")).override(cfg)
        except Exception as e:
            logger.warning(f"Could not load config from {pxcfg}: {e}")
            # Continue with minimal config
            pass
        
        cfg = cfg or {}
        try:
            self.url_library = PyfficeURLLibrary(cfg)
        except Exception as e:
            logger.warning(f"Could not initialize URL library: {e}")
            self.url_library = None
        
        self.contacts: Optional[PyfficeRolodex] = None
        self.documents: dict = {}
        self.forms_manager: Optional[PyfficeFormsManager] = None
        self.imports: dict = {}
        self.source_manager: Optional[PyfficeSources] = None
        self.source: Any = None

    def add_pydocument(self, pydoc: Any) -> Any:
        """Add a Pyffice document to the codex."""
        try:
            if isinstance(pydoc, str):
                pydoc = self.load_pydocument(pydoc)
            self.documents.append(pydoc)
            return pydoc
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            raise

    def add_url(self, url: str) -> Optional[str]:
        """Add a URL to the library."""
        try:
            if self.url_library is None:
                raise ValueError("URL library not initialized")
            return self.url_library.add_url(url)
        except Exception as e:
            logger.error(f"Failed to add URL {url}: {e}")
            return None

    def get_url(self, url_id: Optional[str] = None) -> Optional[Any]:
        """Get URL by ID."""
        try:
            if self.url_library is None:
                return None
            return self.url_library.get_url_by_id(url_id)
        except Exception as e:
            logger.error(f"Failed to get URL {url_id}: {e}")
            return None

    def import_cherrytree(self, cfg: dict[str, Any]) -> Optional[Any]:
        """Import from CherryTree format."""
        try:
            if PyfficePortCherryTree is None:
                raise ImportError("CherryTree import not available")
            logma.info(f"CFG {cfg}")
            cherrytree = PyfficePortCherryTree(cfg)
            logma.info(f"CherryTree: {cherrytree.file_path}")
            import_doc = cherrytree.file_import()
            cherrytree.file_export(join(expanduser("~"), "_work", "cherrytree.yaml"))
            self.imports[cherrytree.did] = import_doc
            return cherrytree
        except Exception as e:
            logger.error(f"Failed to import CherryTree: {e}")
            return None

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
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeWebBrowser is None:
                raise ImportError("Web browser not available")
            browser = PyfficeWebBrowser(cfg)
            self.documents[browser.did] = browser
            return browser
        except Exception as e:
            logger.error(f"Failed to init browser: {e}")
            return None

    def init_calendar(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a calendar document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeCalendar is None:
                raise ImportError("Calendar not available")
            calendar = PyfficeCalendar(cfg)
            self.documents[calendar.did] = calendar
            return calendar
        except Exception as e:
            logger.error(f"Failed to init calendar: {e}")
            return None

    def init_chart(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a chart document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeChart is None:
                raise ImportError("Chart not available")
            chart = PyfficeChart(cfg)
            self.documents[chart.did] = chart
            return chart
        except Exception as e:
            logger.error(f"Failed to init chart: {e}")
            return None

    def init_contacts(self, cfg: Optional[dict[str, Any]] = None) -> Optional[PyfficeRolodex]:
        """Initialize a contacts/rolodex document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeRolodex is None:
                raise ImportError("Contacts not available")
            self.contacts = PyfficeRolodex(cfg)
            self.documents[self.contacts.did] = self.contacts
            return self.contacts
        except Exception as e:
            logger.error(f"Failed to init contacts: {e}")
            return None

    def init_files(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a filesystem document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeFileSystem is None:
                raise ImportError("FileSystem not available")
            files = PyfficeFileSystem(cfg)
            self.documents[files.did] = files
            return files
        except Exception as e:
            logger.error(f"Failed to init files: {e}")
            return None

    def init_form(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a form document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if self.forms_manager is None:
                self.init_forms_manager(cfg)
            if self.forms_manager is None:
                raise RuntimeError("Forms manager not available")
            form = self.forms_manager.create_new_form(cfg)
            self.documents[form.did] = form
            return form
        except Exception as e:
            logger.error(f"Failed to init form: {e}")
            return None

    def init_forms_manager(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize forms manager."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeFormsManager is None:
                raise ImportError("Forms not available")
            self.forms_manager = PyfficeFormsManager(cfg)
            self.documents[self.forms_manager.did] = self.forms_manager
            return self.forms_manager
        except Exception as e:
            logger.error(f"Failed to init forms manager: {e}")
            return None

    def init_image(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize an image document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeImage is None:
                raise ImportError("Image not available")
            image = PyfficeImage(cfg)
            self.documents[image.did] = image
            return image
        except Exception as e:
            logger.error(f"Failed to init image: {e}")
            return None

    def init_matrix(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a spreadsheet/matrix document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeMatrix is None:
                raise ImportError("Spreadsheet not available")
            matrix = PyfficeMatrix(cfg)
            self.documents[matrix.did] = matrix
            return matrix
        except Exception as e:
            logger.error(f"Failed to init matrix: {e}")
            return None

    def init_note(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a note document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeScript is None:
                raise ImportError("Note/Script not available")
            note = PyfficeScript(cfg)
            self.documents[note.did] = note
            return note
        except Exception as e:
            logger.error(f"Failed to init note: {e}")
            return None

    def init_notebook(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a notebook document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeNotebook is None:
                raise ImportError("Notebook not available")
            notebook = PyfficeNotebook(cfg)
            self.documents[notebook.did] = notebook
            return notebook
        except Exception as e:
            logger.error(f"Failed to init notebook: {e}")
            return None

    def init_pdf(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a PDF document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficePDF is None:
                raise ImportError("PDF not available")
            pdf = PyfficePDF(cfg)
            self.documents[pdf.did] = pdf
            return pdf
        except Exception as e:
            logger.error(f"Failed to init PDF: {e}")
            return None

    def init_prompt(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a prompts manager."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficePromptsManager is None:
                raise ImportError("Prompts not available")
            prompts = PyfficePromptsManager(cfg)
            self.documents[prompts.did] = prompts
            return prompts
        except Exception as e:
            logger.error(f"Failed to init prompts: {e}")
            return None

    def init_script(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a script document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeScript is None:
                raise ImportError("Script not available")
            script = PyfficeScript(cfg)
            self.documents[script.did] = script
            return script
        except Exception as e:
            logger.error(f"Failed to init script: {e}")
            return None

    def init_sketch(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a sketch/diagram document."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeSketch is None:
                raise ImportError("Sketch not available")
            sketch = PyfficeSketch(cfg)
            self.documents[sketch.did] = sketch
            return sketch
        except Exception as e:
            logger.error(f"Failed to init sketch: {e}")
            return None

    def init_source_manager(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize source manager."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if PyfficeSources is None:
                raise ImportError("Sources not available")
            self.source_manager = PyfficeSources(cfg)
            self.documents[self.source_manager.did] = self.source_manager
            return self.source_manager
        except Exception as e:
            logger.error(f"Failed to init source manager: {e}")
            return None

    def init_source(self, cfg: Optional[dict[str, Any]] = None) -> Optional[Any]:
        """Initialize a data source."""
        try:
            cfg = cfg or {}
            cfg["codex"] = self
            if self.source_manager is None:
                self.init_source_manager(cfg)
            if self.source_manager is None:
                raise RuntimeError("Source manager not available")
            self.source = self.source_manager.create_new_source(cfg)
            self.documents[self.source.did] = self.source
            return self.source
        except Exception as e:
            logger.error(f"Failed to init source: {e}")
            return None

    def load_document(self, document: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Load documents into the codex."""
        try:
            logma.info(f"Load Document {document}")
            if document is None:
                document = self.config.dikt.get("document", {})
                if document is None:
                    document = {}
            # lookup and initialize the proper Pyffice Document type
            self.set_documents(document.get("documents", {}))
            self.set_imports(document.get("imports", {}))
            return document
        except Exception as e:
            logger.error(f"Failed to load document: {e}")
            return {}

    def save(self, path: Optional[str] = None, syntax: Optional[str] = None, 
             encrypt_key: Optional[str] = None) -> "PyfficeCodex":
        """Save the codex to a file."""
        try:
            # TODO: Implement actual save logic
            logger.info(f"Saving to {path}")
            return self
        except Exception as e:
            logger.error(f"Failed to save: {e}")
            return self

    def set_imports(self, imports: Optional[dict[str, Any]] = None) -> "PyfficeCodex":
        """Set imports with change tracking."""
        try:
            if imports is None:
                imports = {}
            if imports != self.imports:
                self.add_change("imports", self.imports, imports)
                self.imports = imports
            return self
        except Exception as e:
            logger.error(f"Failed to set imports: {e}")
            return self

    def set_storage(self) -> None:
        """Set storage location for the codex (folder or database)."""
        logger.info("set_storage not yet implemented")

    # ============================================================================
    # AI Agent Enhancement Methods
    # ============================================================================
    
    def to_yaml(self) -> str:
        """Convert the entire codex to a YAML string for serialization."""
        try:
            import yaml
            data = {
                "version": self.VERSION,
                "documents": self.documents,
                "imports": self.imports,
                "contacts": self.contacts,
            }
            return yaml.dump(data, default_flow_style=False)
        except Exception as e:
            logger.error(f"Failed to convert to YAML: {e}")
            return ""

    @classmethod
    def from_yaml(cls, yaml_str: str, cfg: Optional[dict[str, Any]] = None) -> "PyfficeCodex":
        """Load a codex from a YAML string."""
        try:
            import yaml
            data = yaml.safe_load(yaml_str)
            codex = cls(cfg)
            codex.documents = data.get("documents", {})
            codex.imports = data.get("imports", {})
            return codex
        except Exception as e:
            logger.error(f"Failed to load from YAML: {e}")
            return cls(cfg)

    def to_summary(self) -> dict[str, Any]:
        """Get a token-efficient summary of the codex for AI agents."""
        return {
            "version": self.VERSION,
            "document_count": len(self.documents),
            "document_types": list(self.documents.keys()),
            "has_contacts": self.contacts is not None,
            "has_forms_manager": self.forms_manager is not None,
            "import_count": len(self.imports),
        }

    def to_json_schema(self) -> dict[str, Any]:
        """Get JSON Schema for LLM output validation."""
        return {
            "type": "object",
            "properties": {
                "version": {"type": "string"},
                "documents": {"type": "object"},
                "imports": {"type": "object"},
            },
            "required": ["version"],
        }


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
