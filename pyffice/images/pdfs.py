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
        self.reader = None
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
        # self.set_file_path(self.config.dikt.get("file_path", None))
        self.set_content(document.get("content", None))
        if self.content is not None:
            stream = io.BytesIO(self.content)
            self.open_file(stream)
        return self

    def load_pdf_pages(self):
        """Render PDF pages as images to display."""
        for page_num in range(len(self.reader)):
            page = self.reader.load_page(page_num)  # Load page securely
            pix = page.get_pixmap()  # Render the page into a pixmap
            # # Convert the pixmap to a QImage and display
            # image = pyqt.QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            # label = pyqt.QLabel(self)
            # label.setPixmap(pyqt.QPixmap.fromImage(image))
            # self.layout.addWidget(label)
        return self

    def open_file(self, file_=None):
        """"""
        if file_ is None:
            file_ = self.file_path
        self.set_file_path(file_)
        if self.is_safest:
            self.open_file_no_javascript(file_)
        else:  # this ensures that PDF is opened without running any javascript
            self.open_file_full_feature(file_)
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

    def read(self):
        """
        Read all pages of the PDF and print their text content.

        :return: self
        """
        for page_n, page in enumerate(self.reader.pages):
            print(f"Page {page_n + 1}:")
            print(page.extract_text())
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

    def save(self, output_path):
        """
        Save changes to a new file.

        :param output_path: Path to save the modified PDF.
        :return: self
        """
        self.initialize_writer()
        with open(output_path, "wb") as f:
            self.writer.write(f)
        return self

    def set_content(self, content):
        """"""
        if content != self.content:
            self.add_change("content", self.content, content)
            self.content = content
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"]["path"] = self.file_path
        doc["document"]["content"] = self._get_bytes()
        return doc

    def _get_bytes(self):
        """"""
        with open(self.file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        return pdf_bytes

    # def _get_bytes(self):
    #     """"""
    #     self.initialize_writer()
    #     for page in self.reader.pages():
    #         self.writer.add_page(page)
    #     bytes_stream = io.BytesIO()
    #     # self.writer.write(bytes_stream)
    #     logma.info(f"PDF bytes saved to {bytes_stream.getvalue()}")
    #     return bytes_stream.getvalue()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
