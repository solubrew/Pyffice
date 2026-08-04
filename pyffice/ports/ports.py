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
from io import BytesIO
import json as j

# ======================================3rd Party Library Modules=====================================================||
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import nbformat
import html
from pyffice.items.items import PyfficeTable
from pyffice.web.web import PyfficeWebBrowser
from typing import Any
from typing_extensions import Self

try:
    import dia

    HAS_DIA = True
except ImportError:
    HAS_DIA = False
    pass
# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from subtrix.utilities import uuid
from kahndor.logma import Logma
from pyffice.document import PyfficeDocumentManager
from pyffice.script.script import PyfficeScript
from pyffice.images.images import PyfficeImage
from pyffice.web.url import PyfficeURL
from pyffice.items.text import PyfficeText
from pycurity.pymatch import extract_urls
from pycurity.pyhash import decode64
from squirl.objnql import tblonql
from squirl.orgnql import yonql

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
# logma.off()

# ====================================================================================================================||
pxcfg = join(here, "../config/_data_", ".yaml")


class PyfficePort(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficePort.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePort")).override(cfg)

    def file_export(self, file_=None) -> Self:
        """File export.

        Args:
            file_: Parameter.

        Returns:
            Self for chaining.
        """
        self.file_write(file_, self.to_dict())
        return self

    def file_import(self, file_path=None) -> Self:
        """Import from file path."""
        self.open_file(file_path)
        self.parse()
        return self

    def export(self, document=None) -> Self:
        """Export a Pyffice document out to the port's native format.

        Subclasses override this for format-specific writers (xlsx,
        docx, png, etc.). The base implementation falls back to a
        YAML serialization via :meth:`file_write`, which keeps the
        round-trip-lossless path available for ports that don't have
        a native exporter yet.

        Args:
            document: Optional Pyffice document to serialize. If
                None, ``self.to_dict()`` is used.

        Returns:
            ``self`` for chaining.
        """
        if document is not None and hasattr(document, "to_dict"):
            payload = document.to_dict()
        else:
            payload = self.to_dict()
        if self.file_path:
            self.file_write(self.file_path, payload)
        return self

    def import_data(self) -> Any:
        """Read the port's ``file_path`` and return the loaded payload.

        Subclasses override this for format-specific readers (xlsx,
        docx, png, etc.). The base implementation defers to
        ``open_file`` and returns the raw text/bytes so subclasses
        that don't have a specialized reader can still expose
        something useful.

        Returns:
            Loaded data as a dict, list, or string depending on the
            subclass; ``None`` if no ``file_path`` is set.
        """
        if not self.file_path:
            return None
        text = self.open_file(self.file_path, open_=True)
        if text is None:
            return None
        # YAML is the canonical interchange format; default to it
        # if text parses cleanly, else return the raw string.
        try:
            import yaml

            return yaml.safe_load(text)
        except ImportError:
            return {"text": text}
        except (ValueError, TypeError):
            return {"text": text}

    def to_native(self) -> Any:
        """Convert to native format."""
        return self.document

    def to_xml(self) -> Any:
        """Convert to XML format."""
        import xml.etree.ElementTree as ET

        return ET.tostring(self.document, encoding="unicode") if self.document else ""

    def open_file(self, file_path, open_=True) -> Any:
        """File open.

        Args:
            file_path: Parameter.
            open_: Parameter.

        Returns:
            Self for chaining.
        """
        text = super().open_file(file_path, open_)
        return text

    def file_write(self, path, dikt) -> Self:
        """File write.

        Args:
            path: Parameter.
            dikt: Parameter.

        Returns:
            Self for chaining.
        """
        # with open(path, "w") as f:
        #     f.write(text)
        yonql.Doc(path).write(dikt)
        return self


class PyfficePortOffice(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortOffice")).override(cfg)

    def parse_file(self) -> Self:
        """Parse the loaded file."""
        # Placeholder - subclasses implement specific parsing
        if not hasattr(self, "file_path"):
            return self
        return self

    def parse_table(self) -> Self:
        """Parse tables from document."""
        # Placeholder - subclasses implement specific parsing
        if not hasattr(self, "document"):
            return self
        return self

    def open_file_svg(self, file_) -> Self:
        """Open SVG file."""
        # Placeholder - SVG requires special handling
        if not file_:
            return self
        return self


class PyfficePortCSV(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortCSV")).override(cfg)

    def open_file(self, file, if_data_only=False, read_only=False, keep_vba=False) -> Any:
        """Open file.

        Args:
            file: Parameter.
            if_data_only: Parameter.
            read_only: Parameter.
            keep_vba: Parameter.

        Returns:
            Self for chaining.
        """
        rdr = tblonql.Doc(file)
        data = next(rdr.read(), None)
        return data


class PyfficePortDia(PyfficePort):
    """Port Dia File and convert to Pyffice Sketch Document"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficePortDia.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortDia")).override(cfg)
        self.is_dia_installed = HAS_DIA
        self.diagram = None
        self.nodes = None
        self.root = None
        self.tree = None
        self.edges = None

    def import_file(self, file_path=None) -> Self:
        """Import file.

        Args:
            file_path: Parameter.

        Returns:
            Self for chaining.
        """
        self.open_file(file_path)
        self.parse()
        return self.to_dict()

    def open_file(self, file_path) -> None:
        """Open file.

        Args:
            file_path: Parameter.

        Returns:
            Self for chaining.
        """
        super().open_file(file_path)
        with open(str(self.file_path), "r") as f:
            xml_string = f.read()
        self.tree = ET.ElementTree(ET.fromstring(xml_string))
        self.root = self.tree.getroot()

        # tree = ET.parse("example.dia")

        if self.is_dia_installed:
            self.diagram = dia.open(file_path)

    def parse(self) -> Self:
        """Parse .

        Returns:
            Self for chaining.
        """
        if self.is_dia_installed:
            self.parse_dia()
        else:
            self.parse_xml()
        return self

    def parse_dia(self) -> Self:
        """
        Parse the entire XML structure starting from the root.

        :return: A list of parsed nodes.
        """
        for layer in self.diagram.data.layers:
            for obj in layer.objects:
                for attr_name, attr_value in obj.properties.items():
                    if attr_name == "name":
                        obj.name = attr_value
        return self

    def parse_xml(self) -> None:
        """Parse xml.

        Returns:
            Self for chaining.
        """
        # Open and parse the .dia file (it's an XML file)
        # Dia's XML namespaces
        namespace = {"dia": "http://www.lysator.liu.se/~alla/dia/"}

        # Diagramdata
        # paper
        # grid
        # color
        # display

        # Background
        #

        # Iterate through objects in the Dia file
        for obj in self.root.findall(".//dia:object", namespace):
            obj_type = obj.get("type", "Unknown")
            # Extract attributes
            for attr in obj.findall("dia:attribute", namespace):
                attr_name = attr.get("name", "Unknown")


class PyfficePortFileSystem(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortFileSystem")).override(cfg)


class PyfficePortJupyter(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortJupyter")).override(cfg)
        self.notebook = None

    def file_export(self, file_=None) -> Self:
        """File export.

        Args:
            file_: Parameter.

        Returns:
            Self for chaining.
        """
        if self.notebook is None:
            self.load_document()
        with open(file_, "w", encoding="utf-8") as f:
            nbformat.write(self.notebook, f)
        return self

    def file_import(self, file_path=None) -> Self:
        """File import.

        Args:
            file_path: Parameter.

        Returns:
            Self for chaining.
        """
        self.open_file(file_path)
        return self.to_dict()

    def open_file(self, file_path) -> Self:
        """File open.

        Args:
            file_path: Parameter.

        Returns:
            Self for chaining.
        """
        super().open_file(file_path, False)
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.notebook = nbformat.read(f, as_version=4)
        return self


class PyfficePortText(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortWebSession")).override(cfg)


class PyfficePortWebSession(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortWebSession")).override(cfg)
        self.nodes = None
        self.sessions = None

    def file_import(self, file_path=None) -> Self:
        """File import.

        Args:
            file_path: Parameter.

        Returns:
            Self for chaining.
        """
        self.open_file(file_path)
        return self.to_dict()

    def open_file(self, file_path) -> Self:
        """File open.

        Args:
            file_path: Parameter.

        Returns:
            Self for chaining.
        """
        # logma.info(f"Open Cherry Tree {self.config.dikt["file_path"]}")
        self.load_document(self.config.dikt.get("document", {}))
        self.sessions = j.loads(super().open_file(file_path))
        self.parse_session()
        return self

    def load_document(self, document=None) -> Self:
        """Load document into this document.

        Args:
            document: Parameter.

        Returns:
            Self for chaining.
        """
        logma.info(f"Load Web Session Tree {document}")
        super().load_document(document)
        self.nodes = []
        return self

    def parse_session(self) -> Self:
        """Parse session.

        Returns:
            Self for chaining.
        """
        for window in self.sessions.get("windows", []):
            node = self.parse_window(window)
            self.nodes.append(node)
        return self

    def parse_window(self, window) -> Any:
        """Each window is a Node"""
        tabs = []
        for tab in window:
            tabs.append(self.parse_tab(tab))
        node = {"tabs": tabs}
        return node

    def parse_tab(self, tab) -> Any:
        """Parse tab.

        Args:
            tab: Parameter.

        Returns:
            Self for chaining.
        """
        # extract url, favicon, metadata
        url = tab["url"]
        favicon = tab["favIconUrl"]
        metadata = tab
        return {"url": url, "favicon": favicon, "metadata": metadata}


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
