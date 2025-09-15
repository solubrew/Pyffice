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
import io
import base64

# ======================================3rd Party Library Modules=====================================================||
from PyPDF2 import PdfReader, PdfWriter, PageObject
import fitz

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "pdfs.yaml")


class PyfficePDF(PyfficeDocument):
    """
    A class to work with PDF files using PyPDF2, supporting
    annotations, embedded media, and encryption.
    """

    def __init__(self, cfg=None):
        """
        Initialize with a given PDF file path and optional configuration.

        :param path: Path to the PDF file to read.
        :param cfg: Configuration object (optional).
        """
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficePDF").override(cfg))
        self.file_path = None
        self.is_safest = False
        self.doc_type = "pdf"
        self.content = None
        self.pdf_fitz = None
        self.reader = None
        self.storage = "external"
        self.writer = None

    def add_page(self, new_page=None):
        """
        Add a blank page or an existing page to the PDF.

        :param new_page: A PDF page object to add (optional).
        :return: self
        """
        if new_page:
            self.writer.add_page(new_page)
        else:
            self.writer.add_blank_page(width=8.5 * 72, height=11 * 72)  # Default 8.5x11 inches
        return self

    def add_annotation(self, page_n, annotation_text, coords):
        """
        Add an annotation (like a comment or text highlight) to a specific page.

        :param page_n: Page number to add the annotation to.
        :param annotation_text: The text of the annotation.
        :param coords: Tuple (x1, y1, x2, y2) for the annotation's bounding box.
        :return: self
        """
        page = self.writer.pages[page_n]
        annotation = {
            "/Type": "/Annot",
            "/Subtype": "/Text",
            "/Contents": annotation_text,
            "/Rect": list(coords),
        }
        page.add_annotation(annotation)
        return self

    def edit(self):
        """"""

        # Initialize writer with all existing PDF pages
        for page in self.reader.pages:
            self.writer.add_page(page)
        return self

    def embed_media(self, media_path, page_n=0, rect=(100, 500, 200, 600)):
        """
        Embed media (like audio or video) into a specific page.

        :param media_path: Path to the media file.
        :param page_n: Page on which the media will be placed (default: 0).
        :param rect: Tuple (x1, y1, x2, y2) defining the media's bounding box.
        :return: self
        """
        # Read and encode media file
        with open(media_path, "rb") as media_file:
            media_data = base64.b64encode(media_file.read()).decode("utf-8")
        # Define media annotation
        annotation = {
            "/Type": "/Annot",
            "/Subtype": "/FileAttachment",
            "/Contents": "(Embedded Media)",
            "/Rect": rect,
            "/FS": {
                "/Type": "/Filespec",
                "/F": media_path.split("/")[-1],  # Extract file name from path
                "/EF": {"/F": media_data},  # Encoded media data
            },
        }
        # Add media annotation to the specific page
        page = self.writer.pages[page_n]
        page.add_annotation(annotation)
        return self

    def encrypt(self, owner_password, user_password=None):
        """
        Encrypt the PDF with a password, allowing controlled access.

        :param owner_password: The owner password to set permissions.
        :param user_password: The user password for opening the PDF (optional).
        :return: self
        """
        user_password = user_password or ""
        self.writer.encrypt(user_password=user_password, owner_password=owner_password)
        return self

    def extract_text(self, page_n=0):
        """Extract the text from a specific page."""
        mat = fitz.Matrix(self.scale, self.scale)
        pix = page.get_pixmap(matrix=mat)

    def get_binary(self):
        """"""

    def get_page_size(self, page_n=0):
        """
        Get the size (width and height) of a specific page.

        :param page_n: Page number (starting from 0).
        :return: Tuple with (width, height) in points.
        """
        page = self.reader.pages[page_n]
        media_box = page.mediabox
        return float(media_box.width), float(media_box.height)

    def get_page_text(self, page_n=0):
        """
        Extract the text from a specific page.

        :param page_n: Page number to extract text from (default: 0).
        :return: The text extracted from the page.
        """
        page = self.reader.pages[page_n]
        return page.extract_text()

    def initialize_writer(self):
        """"""
        if self.writer is None:
            self.writer = PdfWriter()  # For writing to new PDFs
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
        if document is None:
            document = {}
        super().load_document(document)
        content = document.get("data", {}).get("content", {})
        if content is None:
            content = {}
            self.set_content(content)
        self.set_file_path(content.get("file_path", None))
        return self

    def load_pdf_pages(self):
        """Render PDF pages as images to display."""
        for page_num in range(len(self.reader)):
            page = self.reader.load_page(page_num)  # Load page securely
            pix = page.get_pixmap()  # Render the page into a pixmap
        return self

    def open_file(self, file_=None):
        """"""
        if file_ is None:
            file_ = self.file_path
        if exists(file_):
            self.set_file_path(file_)
            if self.is_safest:
                self.open_file_no_javascript(file_)
            else:  # this ensures that PDF is opened without running any javascript
                self.open_file_full_feature(file_)
        self.pdf_fitz = fitz.open(file_)
        return self

    def open_file_full_feature(self, file_):
        """"""
        self.reader = PdfReader(file_)  # For reading PDF content
        return self

    def open_file_no_javascript(self, file_):
        """"""
        self.reader = fitz.open(file_)
        self.load_pdf_pages()
        return self

    def remove_page(self, page_n):
        """
        Remove a specific page from the PDF.

        :param page_n: Page number to remove (starting from 0).
        :return: self
        """
        self.initialize_writer()
        for i, page in enumerate(self.reader.pages):
            if i != page_n:  # Skip the page to be removed
                self.writer.add_page(page)
        return self

    def save(self, path=None, syntax=None, encrypt_key=None):
        """
        Save changes to a new file.

        :param output_path: Path to save the modified PDF.
        :return: self
        """
        super().save(path, syntax, encrypt_key)
        return self

    def set_content(self, content):
        """"""
        logma.info(f"Content {content}")
        if self.location is None:
            self.set_location(None)
        if self.location == "internal":
            content = self._get_bytes()
        elif self.location == "external":
            if content is not None:
                self.set_file_path(content.get("file_path", None))
                content = {"file_path": self.file_path}
            else:
                raise Exception(f"Unknown Location {self.location}")
        if content is None:
            content = {}
        if content != self.content:
            self.add_change("content", self.content, content)
            self.content = content
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["data"]["path"] = self.file_path
        doc["data"]["content"] = self.content
        return doc

    def _get_bytes(self):
        """"""
        if self.file_path is not None and self.file_path != "":
            with open(self.file_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
            return pdf_bytes
        return None


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
