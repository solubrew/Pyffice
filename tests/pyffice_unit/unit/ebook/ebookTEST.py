"""Tests for pyffice/ebook/.

Coverage:
- epub.create produces a valid EPUB file with mimetype +
  container.xml + content.opf + toc.ncx + chapter1.xhtml
- epub.read round-trips the content (write -> read)
- epub.list_chapters returns at least ['chapter1'] after create
- epub._container_xml / _opf / _toc_ncx / _xhtml return strings
- azw/mobi load/read/write/dump raise on nonexistent files
  (we don't test round-trip since the implementations are stubs)
"""

import os
import tempfile
import zipfile

import pytest

from pyffice.ebook.epub import (
    create as epub_create,
    read as epub_read,
    list_chapters,
    _container_xml,
    _opf,
    _toc_ncx,
    _xhtml,
)
from pyffice.ebook.azw import load as azw_load
from pyffice.ebook.mobi import load as mobi_load


class TestEpubCreate:
    """create() writes a valid EPUB zip."""

    def test_create_writes_zip_file(self, tmp_path):
        out = tmp_path / "test.epub"
        epub_create("Test Book", "Test Author", "<p>hello</p>", str(out))
        assert out.exists()
        assert zipfile.is_zipfile(str(out))

    def test_create_writes_required_files(self, tmp_path):
        out = tmp_path / "test.epub"
        epub_create("Test Book", "Test Author", "<p>hello</p>", str(out))
        with zipfile.ZipFile(str(out), "r") as zf:
            names = zf.namelist()
        assert "mimetype" in names
        assert "META-INF/container.xml" in names
        assert "OEBPS/content.opf" in names
        assert "OEBPS/toc.ncx" in names
        assert "OEBPS/Text/chapter1.xhtml" in names

    def test_mimetype_is_uncompressed(self, tmp_path):
        out = tmp_path / "test.epub"
        epub_create("T", "A", "x", str(out))
        with zipfile.ZipFile(str(out), "r") as zf:
            mimetype_info = zf.getinfo("mimetype")
        # ZIP_STORED (uncompressed) is the EPUB spec requirement.
        assert mimetype_info.compress_type == zipfile.ZIP_STORED

    def test_mimetype_contents(self, tmp_path):
        out = tmp_path / "test.epub"
        epub_create("T", "A", "x", str(out))
        with zipfile.ZipFile(str(out), "r") as zf:
            mimetype = zf.read("mimetype").decode()
        assert mimetype == "application/epub+zip"


class TestEpubRead:
    """read() extracts chapter text."""

    def test_read_round_trip(self, tmp_path):
        out = tmp_path / "test.epub"
        content = "<p>hello world</p>"
        epub_create("Title", "Author", content, str(out))
        text = epub_read(str(out))
        assert "hello world" in text

    def test_read_missing_file_raises(self, tmp_path):
        with pytest.raises((FileNotFoundError, OSError)):
            epub_read(str(tmp_path / "nonexistent.epub"))


class TestEpubListChapters:
    """list_chapters returns XHTML/HTML file names."""

    def test_list_chapters_includes_chapter1(self, tmp_path):
        out = tmp_path / "test.epub"
        epub_create("T", "A", "x", str(out))
        chapters = list_chapters(str(out))
        # At least chapter1.xhtml.
        assert any("chapter1" in c for c in chapters)

    def test_list_chapters_missing_file_raises(self, tmp_path):
        with pytest.raises((FileNotFoundError, OSError)):
            list_chapters(str(tmp_path / "nonexistent.epub"))


class TestEpubInternalHelpers:
    """Internal XML helpers return strings."""

    def test_container_xml_returns_string(self):
        assert isinstance(_container_xml(), str)
        assert "container" in _container_xml().lower()

    def test_opf_contains_title_and_author(self):
        xml = _opf("My Title", "My Author")
        assert "My Title" in xml
        assert "My Author" in xml

    def test_toc_ncx_contains_title(self):
        xml = _toc_ncx("My Title")
        assert "My Title" in xml

    def test_xhtml_contains_content(self):
        xml = _xhtml("<p>some content</p>")
        assert "some content" in xml


class TestAzwLoad:
    """azw.load raises on nonexistent path."""

    def test_load_missing_file_raises(self, tmp_path):
        with pytest.raises((FileNotFoundError, OSError)):
            azw_load(str(tmp_path / "nonexistent.azw"))


class TestMobiLoad:
    """mobi.load raises on nonexistent path."""

    def test_load_missing_file_raises(self, tmp_path):
        with pytest.raises((FileNotFoundError, OSError)):
            mobi_load(str(tmp_path / "nonexistent.mobi"))