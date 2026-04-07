"""
Pyffice Text Ports - External format converters for text documents.
"""
from pyffice.text.text import PyfficeText
from pyffice.ports.ports import PyfficePort


class MarkdownPort(PyfficePort):
    """Port for Markdown (.md) format."""

    def read(self, file_path: str) -> PyfficeText:
        """Read Markdown file and convert to PyfficeText."""
        pass

    def write(self, text: PyfficeText, file_path: str) -> None:
        """Write PyfficeText to Markdown file."""
        pass


class HTMLPort(PyfficePort):
    """Port for HTML (.html, .htm) format."""

    def read(self, file_path: str) -> PyfficeText:
        """Read HTML file and convert to PyfficeText."""
        pass

    def write(self, text: PyfficeText, file_path: str) -> None:
        """Write PyfficeText to HTML file."""
        pass


class LaTeXPort(PyfficePort):
    """Port for LaTeX (.tex) format."""

    def read(self, file_path: str) -> PyfficeText:
        """Read LaTeX file and convert to PyfficeText."""
        pass

    def write(self, text: PyfficeText, file_path: str) -> None:
        """Write PyfficeText to LaTeX file."""
        pass


class PlainTextPort(PyfficePort):
    """Port for Plain Text (.txt) format."""

    def read(self, file_path: str) -> PyfficeText:
        """Read plain text file and convert to PyfficeText."""
        pass

    def write(self, text: PyfficeText, file_path: str) -> None:
        """Write PyfficeText to plain text file."""
        pass


class RTFPort(PyfficePort):
    """Port for Rich Text Format (.rtf) format."""

    def read(self, file_path: str) -> PyfficeText:
        """Read RTF file and convert to PyfficeText."""
        pass

    def write(self, text: PyfficeText, file_path: str) -> None:
        """Write PyfficeText to RTF file."""
        pass
