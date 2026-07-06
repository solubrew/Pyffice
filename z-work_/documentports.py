"""
Pyffice Document Ports - External format converters for generic documents.
"""
from pyffice.document import PyfficeDocument
from pyffice.ports.ports import PyfficePort


class PDFPort(PyfficePort):
    """Port for PDF (.pdf) format."""

    def read(self, file_path: str) -> PyfficeDocument:
        """Read PDF file and convert to PyfficeDocument."""
        pass

    def write(self, doc: PyfficeDocument, file_path: str) -> None:
        """Write PyfficeDocument to PDF file."""
        pass


class RTFPort(PyfficePort):
    """Port for Rich Text Format (.rtf) format."""

    def read(self, file_path: str) -> PyfficeDocument:
        """Read RTF file and convert to PyfficeDocument."""
        pass

    def write(self, doc: PyfficeDocument, file_path: str) -> None:
        """Write PyfficeDocument to RTF file."""
        pass


class TXTSPort(PyfficePort):
    """Port for Plain Text (.txt) format."""

    def read(self, file_path: str) -> PyfficeDocument:
        """Read text file and convert to PyfficeDocument."""
        pass

    def write(self, doc: PyfficeDocument, file_path: str) -> None:
        """Write PyfficeDocument to text file."""
        pass


class DOCXPort(PyfficePort):
    """Port for Microsoft Word (.docx) format."""

    def read(self, file_path: str) -> PyfficeDocument:
        """Read DOCX file and convert to PyfficeDocument."""
        pass

    def write(self, doc: PyfficeDocument, file_path: str) -> None:
        """Write PyfficeDocument to DOCX file."""
        pass


class ODTPort(PyfficePort):
    """Port for OpenDocument Text (.odt) format."""

    def read(self, file_path: str) -> PyfficeDocument:
        """Read ODT file and convert to PyfficeDocument."""
        pass

    def write(self, doc: PyfficeDocument, file_path: str) -> None:
        """Write PyfficeDocument to ODT file."""
        pass
