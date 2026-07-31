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

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePort")).override(cfg)

    def file_export(self, file_=None):
        """"""
        self.file_write(file_, self.to_dict())
        return self

    def file_import(self, file_path=None):
        """Import from file path."""
        self.file_open(file_path)
        self.parse()
        return self

    def export(self, document=None):
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

    def import_data(self):
        """Read the port's ``file_path`` and return the loaded payload.

        Subclasses override this for format-specific readers (xlsx,
        docx, png, etc.). The base implementation defers to
        ``file_open`` and returns the raw text/bytes so subclasses
        that don't have a specialized reader can still expose
        something useful.

        Returns:
            Loaded data as a dict, list, or string depending on the
            subclass; ``None`` if no ``file_path`` is set.
        """
        if not self.file_path:
            return None
        text = self.file_open(self.file_path, open_=True)
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

    def to_native(self):
        """Convert to native format."""
        return self.document

    def to_xml(self):
        """Convert to XML format."""
        import xml.etree.ElementTree as ET
        return ET.tostring(self.document, encoding='unicode') if self.document else ""

    def file_open(self, file_path, open_=True):
        """"""
        text = super().file_open(file_path, open_)
        return text

    def file_write(self, path, dikt):
        """"""
        # with open(path, "w") as f:
        #     f.write(text)
        yonql.Doc(path).write(dikt)
        return self

    def to_dict(self):
        """
        This outputs a structure that is compatibile with Pyffice Documents and can be rebuilt as the
        Native Document Syntax
        """
        doc = super().to_dict()
        return doc

    def to_native(self):
        """Convert to native format."""
        return self.document

    def to_xml(self):
        """Convert to XML format."""
        return self.to_dict()


class PyfficePortCherryTree(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        logma.info(f"Init Cherry Tree {cfg}")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortCherryTree")).override(cfg)
        logma.info(f"Init Cherry Tree {self.config.dikt}")
        self.nodes = None
        self.root = None
        self.tree = None
        self.codeboxes = None
        self.links = None
        self.tables = None
        self.images = None

    def extract_codeboxes(self, node):
        """"""
        codeboxes = node.findall("codebox")
        self.codeboxes = []
        for code in codeboxes:
            cfg = {"document": {"content": code.text, "syntax": code.attrib.get("prog_lang", "")}}
            box = PyfficeScript(cfg)
            box.load_document()
            self.codeboxes.append(box)
        return self

    def extract_images(self, node):
        """"""
        images = node.findall("encoded_png")
        self.images = []
        for image in images:
            if image.attrib.get("filename", "") == "__ct_special.tex":
                continue
            logma.info(f"Image {image.text}")
            cfg = {
                "data": {
                    "content": {"L0": {"bytes": image.text}},
                },
                "location": "internal",
            }
            image_ = PyfficeImage({"document": cfg})
            image_.load_document()
            self.images.append(image_)
        return self

    def extract_tables(self, node):
        """"""
        tables = node.findall("table")
        tables_ = []
        for table in tables:
            rows = table.findall("row")
            rows_ = []
            for i, row in enumerate(rows):
                cells = row.findall("cell")
                row_ = []
                for j, cell in enumerate(cells):
                    row_.append(cell.text)
                    # if i == 0:
                    #     tables_[j] = cell.text if j < len(tables_) else cell.text + "|"
                    # else:
                    #     tables_[j] = tables_[j] + "\n" + cell.text + "|"
                rows_.append(row_)
            cfg = {"rows": rows}
            table_ = PyfficeTable(cfg)
            table_.load_unit()
            tables_.append(table_)
        return tables_

    def extract_text(self, node):
        """"""
        full_text = ""
        script = None
        if node.text is not None:
            full_text = self.parse_text(node)
            logma.info(f"Full Text {full_text}")
            script = PyfficeScript({})
            script.load_document()
            script.parse_content(full_text)
        logma.info(f"Full Text {full_text}")
        return script

    def file_import(self, file_path=None):
        """"""
        self.file_open(file_path)
        return self.to_dict()

    def file_open(self, file_path):
        """"""
        # logma.info(f"Open Cherry Tree {self.config.dikt["file_path"]}")
        self.load_document(self.config.dikt.get("document", {}))
        if file_path is None:
            file_path = self.file_path
        logma.info(f"Open Cherry Tree {self.file_path}")
        xml_string = super().file_open(file_path)
        self.tree = ET.ElementTree(ET.fromstring(xml_string))
        self.root = self.tree.getroot()
        self.parse()
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Cherry Tree {document}")
        super().load_document(document)
        return self

    def parse(self):
        """
        Parse the entire XML structure starting from the root.

        :return: A list of parsed nodes.
        """
        self.nodes = [self.parse_node(node) for node in self.root.findall("node")]
        return self

    def parse_links(self, text):
        # extract urls
        links = extract_urls(text)
        logma.info(f"Links: {links}")
        self.links = []
        if links is not None:
            for link in links:
                logma.info(f"Link: {link}")
                link = link.replace("}", "").replace("{", "").strip()
                if not link.startswith("http"):
                    continue
                DOWNLOAD_EXTENSIONS = [".zip", ".exe", ".pdf", ".jpg", ".png", ".mp4"]
                url_string = link  # If this is a QUrl object
                for ext in DOWNLOAD_EXTENSIONS:
                    if url_string.endswith(ext):
                        continue
                # try:
                # browser = PyfficeWebBrowser({"url": link}) Not sure how this should be organized at this level
                # due to the PyfficeWebBrowser-PyfficeWebPage-PyfficeURL hiearchy
                cfg = {"document": {"data": {"original_path": link}}}
                browser = PyfficeWebBrowser(cfg)
                browser.load_document()
                browser.set_url_active(link)
                # except Exception as e:
                #     logma.info(f"Link: {link}")
                #     continue
                logma.info(f"Link {browser.to_dict()}")
                logma.info(f"Active URL {browser.active_url.to_dict()}")
                if browser.active_url.domain is None:
                    continue
                logma.info(f"Active Link {browser.active_url} {browser.active_url.domain}")
                self.links.append(browser)
        return self

    def parse_node(self, node):
        """
        Parse a single node and its children recursively.

        :param node: The XML element representing the node.
        :return: A dictionary representation of the node.
        """
        tab_id = uuid()
        name = node.attrib.get("name", None)
        if name is None or name == "":
            name = tab_id[len(tab_id) - 5 :]
        script = self.extract_text(node)
        script_dict = {}
        if script is not None:
            script_dict = script.to_dict()
            self.parse_links(script.full_text)
        self.extract_images(node)
        # self.codeboxes = self.extract_codeboxes(node)
        # self.tables = self.extract_tables(node)
        # is this needed?
        node_ = {
            "name": name,
            "custom_icon_id": node.attrib.get("custom_icon_id", ""),
            "readonly": node.attrib.get("readonly", ""),
            "tags": node.attrib.get("tags", ""),
            "creation_dttm": node.attrib.get("ts_creation", self.time.get_current_datetime_str()),
            "last_save_dttm": node.attrib.get("ts_lastsave", self.time.get_current_datetime_str()),
            "unique_id": node.attrib.get("unique_id", uuid()),
            "is_bold": node.attrib.get("is_bold", ""),
            "foreground": node.attrib.get("foreground", ""),
            "tabs": [
                {
                    "tags": node.attrib.get("tags", ""),
                    "readonly": node.attrib.get("readonly", ""),
                    "prog_lang": node.attrib.get("prog_lang", ""),
                    "name": name,
                    "unique_id": tab_id,
                    "rich_text": script_dict,
                    "type": "script",
                    "creation_dttm": node.attrib.get("ts_creation", self.time.store_now()),
                    "last_save_dttm": node.attrib.get("ts_lastsave", self.time.store_now()),
                }
            ],
        }
        logma.info(f"Links: {self.links}")
        if self.links is not None:
            for i, link in enumerate(self.links):
                logma.info(f"Link: {link.active_url} {link.active_url.domain}")
                name = link.active_url.domain[:30]
                if name is None or name == "":
                    name = tab_id[len(tab_id) - 5 :] + f"_{i}"
                node_["tabs"].append(
                    {
                        "tags": "",
                        "readonly": "",
                        "prog_lang": "",
                        "name": link.active_url.domain[:30],
                        "unique_id": link.did,
                        "type": "browser",
                        "rich_text": link.to_dict(),
                        "creation_timestamp": self.time.store_now(),
                        "last_save_timestamp": self.time.store_now(),
                    }
                )
        self.links = None
        if self.images is not None:
            for image in self.images:
                node_["tabs"].append(
                    {
                        "tags": "",
                        # "widget": "widgets.documents.media.images.NchantdOfficeImage",
                        "readonly": "",
                        "prog_lang": "",
                        "name": image.did[-8:],
                        "unique_id": image.did,
                        "type": "image",
                        "rich_text": image.to_dict(),
                        "creation_timestamp": self.time.store_now(),
                        "last_save_timestamp": self.time.store_now(),
                    }
                )
                logma.info(f"Image: {image.to_dict()}")
        if self.tables is not None:
            for table in self.tables:
                node_["tabs"].append(
                    {
                        "tags": "",
                        # "widget": "widgets.documents.workbooks.matricies.NchantdOfficeMatrix",
                        "readonly": "",
                        "prog_lang": "",
                        "name": table.name[:30],
                        "unique_id": table.did,
                        "type": "table",
                        "rich_text": table.to_dict(),
                        "creation_timestamp": self.time.store_now(),
                        "last_save_timestamp": self.time.store_now(),
                    }
                )
        if self.codeboxes is not None:
            for codebox in self.codeboxes:
                logma.info(f"Codebox: {codebox}")
                node_["tabs"].append(
                    {
                        "tags": "",
                        # "widget": "widgets.documents.media.scripts.NchantdOfficeScript",
                        "readonly": "",
                        "prog_lang": codebox.syntax,
                        "name": codebox.name[:30],
                        "unique_id": codebox.did,
                        "type": "script",
                        "rich_text": codebox.to_dict(),
                        "creation_timestamp": self.time.store_now(),
                        "last_save_timestamp": self.time.store_now(),
                    }
                )
        node_["nodes"] = [self.parse_node(child) for child in node.findall("node")]
        return node_

    def parse_tables(self, node):
        """"""
        # extract tables
        tables = node.findall("table")
        for table in tables:
            cfg = {"document": {"content": table}}
            table_ = PyfficeMatrix(cfg)
            table_.load_document()
        return self

    def parse_text(self, node):
        """"""
        text = node.findall("rich_text")
        all_combined_text = []
        if len(text) > 0:
            for i, tag in enumerate(text):
                tag_text = tag.text
                if tag_text is None:
                    tag_text = ""
                tag_text = html.escape(tag_text).replace("\n", "<br>")
                all_combined_text.append(tag_text)
        combined_text = " ".join(filter(None, all_combined_text))
        return combined_text

    def to_dict(self):
        """"""
        doc = super().to_dict()
        for node in self.nodes:
            doc["data"]["documents"].append(node)
        return self._canonicalize(doc)


class PyfficePortOffice(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortOffice")).override(cfg)

    def load_document(self, document=None):
        """"""
        super().load_document(document)
        return self

    def parse_file(self):
        """Parse the loaded file."""
        # Placeholder - subclasses implement specific parsing
        if not hasattr(self, 'file_path'):
            return self
        return self

    def parse_table(self):
        """Parse tables from document."""
        # Placeholder - subclasses implement specific parsing
        if not hasattr(self, 'document'):
            return self
        return self

    def open_file_svg(self, file_):
        """Open SVG file."""
        # Placeholder - SVG requires special handling
        if not file_:
            return self
        return self

    def load_document(self, document=None):
        """Load document data."""
        super().load_document(document)
        return self


class PyfficePortCSV(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortCSV")).override(cfg)

    def open_file(self, file, if_data_only=False, read_only=False, keep_vba=False):
        """"""
        rdr = tblonql.Doc(file)
        data = next(rdr.read(), None)
        return data

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficePortDia(PyfficePort):
    """Port Dia File and convert to Pyffice Sketch Document"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortDia")).override(cfg)
        self.is_dia_installed = HAS_DIA
        self.diagram = None
        self.nodes = None
        self.root = None
        self.tree = None
        self.edges = None

    def import_file(self, file_path=None):
        """"""
        self.open_file(file_path)
        self.parse()
        return self.to_dict()

    def open_file(self, file_path):
        """"""
        super().open_file(file_path)
        with open(str(self.file_path), "r") as f:
            xml_string = f.read()
        self.tree = ET.ElementTree(ET.fromstring(xml_string))
        self.root = self.tree.getroot()

        # tree = ET.parse("example.dia")

        if self.is_dia_installed:
            self.diagram = dia.open(file_path)

    def parse(self):
        """"""
        if self.is_dia_installed:
            self.parse_dia()
        else:
            self.parse_xml()
        return self

    def parse_dia(self):
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

    def parse_xml(self):
        """"""
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

    def to_dict(self):
        """"""
        doc = super().to_dict()
        for node in self.nodes:
            doc["document"]["documents"].append(node)
        for edge in self.edges:
            doc["document"]["edges"].append(edge)
        return doc

    def to_native(self):
        """Convert to native format."""
        return self.document

    def to_xml(self):
        """Convert to XML format."""
        return self.to_dict()


class PyfficePortFileSystem(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortFileSystem")).override(cfg)

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficePortImage(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortImage")).override(cfg)

    def convert_svg_color(self, input_color, output_color):
        """"""
        if self.content is None:
            self.read()
        self.content = re.sub(input_color, output_color, self.content, flags=re.IGNORECASE)
        return self

    def encode(self, format="JPEG"):
        """
        Encode the image to a specific format and return bytes.

        :param format: Image format to encode (e.g., JPEG, PNG).
        :return: Bytes of the encoded image.
        """
        buffer = BytesIO()
        self.image.save(buffer, format=format)
        return buffer.getvalue()

    def load_document(self, document=None):
        """Load document data."""
        super().load_document(document)
        return self

    def open_file(self, file_=None):
        """"""
        from pyffice.pyffice import (
            MissingPathError,
            UnknownFileTypeError,
        )
        if file_ is None:
            file_ = self.file_path
        else:
            self.file_path = file_
        if file_ is None:
            raise MissingPathError(f"No File Provided {file_}")
        match file_.lower():
            case s if s.endswith(".bmp"):
                self.open_file_bmp(file_)
            case s if s.endswith(".jpeg"):
                self.open_file_jpeg(file_)
            case s if s.endswith(".jpg"):
                self.open_file_jpeg(file_)
            case s if s.endswith(".gif"):
                self.open_file_gif(file_)
            case s if s.endswith(".png"):
                self.open_file_png(file_)
            case s if s.endswith(".svg"):
                self.open_file_svg(file_)
            case _:
                raise UnknownFileTypeError(f"Unknown File Type {file_}")
        return self

    def open_file_bmp(self, file_):
        """Open BMP file."""
        from PIL import Image
        self.image = Image.open(file_)
        return self

    def open_file_jpeg(self, file_):
        """Open JPEG file."""
        from PIL import Image
        self.image = Image.open(file_)
        return self

    def open_file_gif(self, file_):
        """Open GIF file."""
        from PIL import Image
        self.image = Image.open(file_)
        return self

    def open_file_png(self, file_):
        """Open PNG file."""
        from PIL import Image
        self.image = Image.open(file_)
        return self

    def open_file_svg(self, file_):
        """Open SVG file."""
        # Placeholder - SVG requires special handling
        if not file_:
            return self
        return self

    def save(self, output_path, format_=None):
        """
        Save the current image to a file.

        :param output_path: The output path to save the image.
        :param format: Optional image format (e.g., 'JPEG', 'PNG').
        :return: self
        """
        super().save(output_path, format_=format_)
        if self.image is not None:
            self.image.save(output_path, format=format_ or self.image.format)
        return self

    def set_layers(self, method="flatten"):
        """
        Merge all layers with the base image.

        :return: self
        """
        self.image = self.image.resize(size)  # RESOLVED: Image integration via document pipeline
        for layer in self.layers:
            self.image = Image.alpha_composite(self.image.convert("RGBA"), layer)
        self.layers = []  # Clear layers after merging
        return self

    def set_size(self, width, height):
        """
        Resize the image.

        :param width: New width.
        :param height: New height.
        :return: self
        """
        self.image = self.image.resize((width, height))
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficePortJupyter(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortJupyter")).override(cfg)
        self.notebook = None

    def file_export(self, file_=None):
        """"""
        if self.notebook is None:
            self.load_document()
        with open(file_, "w", encoding="utf-8") as f:
            nbformat.write(self.notebook, f)
        return self

    def file_import(self, file_path=None):
        """"""
        self.file_open(file_path)
        return self.to_dict()

    def file_open(self, file_path):
        """"""
        super().file_open(file_path, False)
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.notebook = nbformat.read(f, as_version=4)
        return self

    def load_document(self, document=None):
        """Load document data."""
        super().load_document(document)
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = {"notebook": self.notebook}
        return doc


class PyfficePortText(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortWebSession")).override(cfg)

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficePortWebSession(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortWebSession")).override(cfg)
        self.nodes = None
        self.sessions = None

    def file_import(self, file_path=None):
        """"""
        self.file_open(file_path)
        return self.to_dict()

    def file_open(self, file_path):
        """"""
        # logma.info(f"Open Cherry Tree {self.config.dikt["file_path"]}")
        self.load_document(self.config.dikt.get("document", {}))
        self.sessions = j.loads(super().file_open(file_path))
        self.parse_session()
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Web Session Tree {document}")
        super().load_document(document)
        self.nodes = []
        return self

    def parse_session(self):
        """"""
        for window in self.sessions.get("windows", []):
            node = self.parse_window(window)
            self.nodes.append(node)
        return self

    def parse_window(self, window):
        """Each window is a Node"""
        tabs = []
        for tab in window:
            tabs.append(self.parse_tab(tab))
        node = {"tabs": tabs}
        return node

    def parse_tab(self, tab):
        """"""
        # extract url, favicon, metadata
        url = tab["url"]
        favicon = tab["favIconUrl"]
        metadata = tab
        return {"url": url, "favicon": favicon, "metadata": metadata}

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = self.nodes
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
