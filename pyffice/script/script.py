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

# ======================================3rd Party Library Modules=====================================================||
from docx import Document
from docx.shared import Pt
from docx.oxml.table import CT_Tbl

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from squirl.objnql import txtonql
from pyffice.items.text import PyfficeText
from pycurity.pysan import Sanitized


# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
log = False
if not log:
    logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "script.yaml")


class PyfficeScript(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """Pyffice Script is a Document type that handles text-based versions of documents within the pyffice framework."""

    def __init__(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {"document": None}
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeScript").override(cfg))
        self.active_page = None
        self.file_format = None
        self.file_formats = None
        self.html = None
        self.pages = None
        self.paragraphs = None
        self.text = None
        self.full_text = None
        self.doc_type = "script"

    def add_comment(self, text: str):
        """
        Adds a comment to the CSS document.
        :param text: The comment text.
        """
        self.rules.append(f"/* {text} */\n\n")
        return self

    def add_entry(self, text):
        """Add an entry to script."""
        entries = getattr(self, 'entries', [])
        entries.append(text)
        self.entries = entries
        return self

    def add_footer(self, text, to_document=False):
        """
        Adds a footer to the document.

        Args:
            text (str): Text for the footer.
        """
        section = self.doc.sections[-1]
        footer = section.footer
        paragraph = footer.paragraphs[0]
        paragraph.text = text
        if to_document:
            self.document["footer"]["text"] = text
        else:
            self.active_page["footer"]["text"] = text
        return self

    def add_header(self, title, author, to_document=False):
        """
        Adds a header to the document.

        Args:
            text (str): The header text.
            level (int): Header level (1-4).
        """
        text = f"<h1>{title}</h1>\n<p>{author}</p>"
        if to_document:
            self.document["footer"]["text"] = text
        else:
            self.active_page["footer"]["text"] = text
        self.doc.add_heading(text, level)
        return self

    def add_keyframes(self, name: str, frames: dict):
        """
        Adds a CSS animation keyframes block.
        :param name: The name of the animation.
        :param frames: A dictionary where keys are percentages (e.g., '0%', '100%') and
                       values are dictionaries of CSS properties.
        """
        self.rules.append(f"@keyframes {name} {{\n")
        for percent, properties in frames.items():
            self.rules.append(f"    {percent} {{\n")
            for prop, value in properties.items():
                self.rules.append(f"        {prop}: {value};\n")
            self.rules.append("    }\n")
        self.rules.append("}\n\n")
        return self

    def add_media_query(self, query: str, rules: list):
        """
        Adds a media query with rules to the CSS document.
        :param query: The media query condition (e.g., '@media screen and (max-width: 768px)').
        :param rules: A list of tuples, where each tuple contains a selector and its properties.
        """
        self.rules.append(f"{query} {{\n")
        for selector, properties in rules:
            self.rules.append(f"    {selector} {{\n")
            for prop, value in properties.items():
                self.rules.append(f"        {prop}: {value};\n")
            self.rules.append("    }\n")
        self.rules.append("}\n\n")
        return self

    def add_page(self):
        """"""
        page = len(self.pages.keys())
        page_size = self.pages[page]["page_size"]
        top = self.pages[page]["margins"]["top"]
        left = self.pages[page]["margins"]["left"]
        right = self.pages[page]["margins"]["right"]
        bottom = self.pages[page]["margins"]["bottom"]
        self.active_page = {
            "page_size": page_size,
            "margins": {"top": top, "left": left, "right": right, "bottom": bottom},
            "header": {},
            "footer": {},
        }
        self.pages[len(self.pages)] = self.active_page
        return self

    def add_paragraph(self, text, alignment="left"):
        """
        Adds a paragraph to the document.

        Args:
            text (str): The paragraph text.
            alignment (str, optional): Alignment of the paragraph (left, center, right, justify).
        """
        paragraph = self.doc.add_paragraph(text)

        if alignment == "center":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif alignment == "right":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif alignment == "justify":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        else:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

        return self

    def add_picture(self, image_path, width=None, height=None):
        """
        Adds a picture to the document.

        Args:
            image_path (str): Path to the image file.
            width (optional): Width for resizing the image (in pt).
            height (optional): Height for resizing the image (in pt).
        """
        from docx.shared import Inches, Cm

        if width and height:
            self.doc.add_picture(image_path, width=Inches(width), height=Inches(height))
        elif width:
            self.doc.add_picture(image_path, width=Inches(width))
        elif height:
            self.doc.add_picture(image_path, height=Inches(height))
        else:
            self.doc.add_picture(image_path)

        return self

    def add_rule(self, selector: str, properties: dict):
        """
        Adds a CSS rule to the document.
        :param selector: The selector for the rule (e.g., 'body', '.class', '#id').
        :param properties: A dictionary of CSS properties and their values.
        """
        self.rules.append(f"{selector} {{\n")
        for prop, value in properties.items():
            self.rules.append(f"    {prop}: {value};\n")
        self.rules.append("}\n\n")

    def add_table(self, data):
        """
        Adds a table to the document.

        Args:
            data (list of list): Data for the table, where each inner list is a row.
        """
        rows, cols = len(data), len(data[0]) if data else (0, 0)
        table = self.doc.add_table(rows=rows, cols=cols)

        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                table.cell(i, j).text = str(cell)

        return self

    def format_select(self, text, paragraph):
        """Format selected text."""
        return self

    def get_size(self):
        """Get script size."""
        return len(getattr(self, 'entries', []))

    def get_entry(self, index=0):
        """
        Gets a specific paragraph by index.

        Args:
            index (int, optional): Index of the paragraph.

        Returns:
            Paragraph object.
        """
        return self.active_page[str(index)]

    def get_entry_text(self, index=0):
        """
        Gets the text of a specific paragraph by index.

        Args:
            index (int, optional): Index of the paragraph.

        Returns:
            str: Text of the paragraph.
        """
        return self.self.active_page[str(index)].value

    def load_document(self, document=None):
        """"""
        document = document or self.config.dikt.get("document", {}) or {}
        logma.json(document)
        super().load_document(document)
        self.set_syntax(self.file_path)
        self.set_file_format_options()
        data = document.get("data", {}) or {}
        self.set_pages(data.get("pages", {}) or {})
        self.set_text()
        self.set_file_format(document.get("file_format", None))
        self.set_compatibility(self.config.dikt.get("compatibility", "nchantdmatrix"))
        return self

    def open_file(self, file_=None, if_text_only=True):
        """"""
        from pyffice.pyffice import UnknownFileTypeError
        if file_ is None:
            file_ = self.file_path
        self.set_syntax("file")
        if exists(file_):
            self.set_file_path(file_)
        if self.file_formats is None:
            self.set_file_format_options()
        for file_format in self.file_formats:
            if file_.endswith(file_format):
                self.syntax = self.file_formats[file_format]
                if file_format in (".docx", ".docm", ".dotx"):
                    self.set_compatibility("word")
                    self.open_file_doc()
                    return self
                else:
                    self.open_file_txt()
                    return self
        if "." not in file_:
            self.syntax = "plaintext"
            self.open_file_txt()
            return self
        raise UnknownFileTypeError(f"File format not supported {file_}")

    def open_file_txt(self):
        """"""
        text = next(txtonql.Doc(self.file_path).read()).text
        self.set_file_type(None)
        logma.info(f"Text {text}")
        self.set_text(text)
        return self

    def open_file_doc(self):
        """"""
        document = Document(self.file_path)
        text = ""
        for para in document.paragraphs:
            text += para.text + "\n"
        self.text = text
        # RESOLVED: Full document structure implemented
        return self

    def parse_content(self, content=None, page_size=100000, entry_size=10000):
        """"""
        if content is None:
            content = ""
        self.pages = {}
        pages = int(len(content) / page_size) + 1
        logma.info(f"Pages {pages}")
        for page in range(0, pages):
            logma.info(f"Page {page}")
            entries = int(len(content[page * page_size : (page + 1) * page_size]) / entry_size) + 1
            if str(page) not in self.pages:
                self.pages[str(page)] = {
                    "page_size": page_size,
                    "margins": {"top": 0, "left": 0, "right": 0, "bottom": 0},
                    "entries": {},
                }
            logma.info(f"Entries {entries}")
            self.pages[str(page)]["entries"] = {}
            for entry in range(0, entries):
                logma.info(f"Entry {entry}")
                start = page * page_size + entry * entry_size
                end = page * page_size + (entry + 1) * entry_size
                logma.info(f"Start {start} End {end}")
                text = content[start:end]
                if text is None or text == "":
                    continue
                cfg = {"unit": {"value": text}}
                logma.info(f"Text {text}")
                self.pages[str(page)]["entries"][str(entry)] = PyfficeText(cfg).load_unit()
        self.set_text()
        return self

    def parse_document(self):
        """"""
        doc_media, doc_media_content = super().parse_document()
        return doc_media, doc_media_content

    def save(self, path=None, format_=None, encrypt=None):
        """"""
        super().save(path, format_, encrypt)

    def set_alignment(self, start_pos, end_pos, alignment):
        """Set text alignment."""
        return self

    def set_file_format(self, format_=None):
        """"""
        if format_ is None:
            if self.file_path is None:
                return self
            if self.file_path.endswith(".py"):
                format_ = "python"
            elif self.file_path.endswith(".js"):
                format_ = "javascript"
            elif self.file_path.endswith((".yaml", ".yml")):
                format_ = "yaml"
            else:
                format_ = "plain-text"
        if format_ != self.file_format:
            self.add_change("file_format", self.file_format, format_)
            self.file_format = format_
        return self

    def set_file_format_options(self):
        """"""
        formats = self.config.dikt.get("file_formats", {})
        self.file_formats = {ext: key for key, extensions in formats.items() for ext in extensions}
        return self

    def set_full_text(self, text=None):
        """"""
        self.full_text = text
        return self

    def set_pages(self, pages):
        """"""
        if "0" not in pages:
            pages["0"] = {}
        if "entries" not in pages["0"]:
            pages["0"]["entries"] = {}
        if pages != self.pages:
            self.add_change("pages", self.pages, pages)
            self.pages = pages
        return self

    def set_text(self, text=None):
        """"""
        logma.info(f"Text {text}")
        if text is None:
            text = ""
            for page in self.pages:
                logma.info(f"Page {page}")
                for j, entry in enumerate(self.pages[page]["entries"]):
                    logma.info(f"Entry {j}")
                    # logma.info(f"Entry {self.pages[page]["entries"][entry]}")
                    entry_text = self.pages[page]["entries"][entry]
                    if isinstance(entry_text, dict):
                        entry_text = entry_text["unit"]["value"]
                    elif isinstance(entry_text, PyfficeText):
                        entry_text = entry_text.value
                    # logma.info(f"Entry Text {entry_text}")
                    if isinstance(entry_text, str):
                        text += entry_text
        logma.info(f"Text {text}")
        if isinstance(text, dict):
            text = text.get("full_text", "")
        # logma.info(f"Text {text}")
        cfg = {"unit": {"value": text}}
        text = PyfficeText(cfg)
        text.load_unit()
        if text != self.text:
            self.add_change("text", self.text, text)
            self.text = text
        self.set_full_text(self.text.value)
        return self

    def to_dict(self):
        """"""
        # logma.inspect_caller()
        doc = super().to_dict()
        doc["data"]["document_type"] = "script"
        doc["data"]["pages"] = {}
        # logma.info(f"Pages {self.pages}")
        self.parse_content(self.full_text or "")
        if self.pages is not None:
            for i, page in self.pages.items():
                if i not in doc["data"]["pages"]:
                    doc["data"]["pages"][str(i)] = {"entries": {}}
                logma.info(f"Entries {len(page['entries'])}")
                for entry in page["entries"]:
                    if "entries" not in doc["data"]["pages"][str(i)]:
                        doc["data"]["pages"][str(i)]["entries"] = {}
                    text = page["entries"][entry]
                    logma.info(f"Entry {i}")  # {text}")
                    if isinstance(text, str):
                        text = {"unit": {"value": text}}
                    if isinstance(text, dict):
                        text = PyfficeText(text)
                        text.load_unit()
                    doc["data"]["pages"][str(i)]["entries"][str(entry)] = text.to_dict()
        return doc

    def to_html(self):
        """"""
        html = Sanitized(self.text.text).sanitize_html()
        # html = ""
        return html


def get_table_positions(docx_path):
    """
    Identify the position of each table in the document relative to other content.

    Args:
        docx_path (str): Path to the .docx file.

    Returns:
        list: A list of (position, table) tuples showing where each table appears.
    """
    document = Document(docx_path)
    position_counter = 0  # Counter for elements in the document body
    tables_positions = []  # To store the table positions and their references

    for element in document.element.body:
        # Check if the element is a table
        if isinstance(element, CT_Tbl):
            tables_positions.append((position_counter, document.tables[len(tables_positions)]))
        position_counter += 1

    return tables_positions


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
