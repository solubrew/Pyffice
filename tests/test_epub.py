"""Test EPUB ebook generation and import."""
import pytest
from pyffice.ebook import epub as epub_doc


def test_create_epub():
    """Test EPUB creation."""
    doc = epub_doc.PyfficeEPUB()
    doc.create_epub("output.epub")
    assert True


def test_read_epub():
    """Test EPUB reading."""
    doc = epub_doc.PyfficeEPUB()
    doc.read_epub("input.epub")
    assert True


def test_add_chapter():
    """Test chapter addition."""
    doc = epub_doc.PyfficeEPUB()
    doc.add_chapter("Title", "Content")
    assert True
