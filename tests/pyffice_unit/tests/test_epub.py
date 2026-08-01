"""Test EPUB ebook round-trip via real captured bytes.

The epub module exposes module-level functions:
- create(title, author, content, output) — writes a complete EPUB zip
- read(epub_path) -> str — extracts concatenated chapter text
- list_chapters(epub_path) -> List[str] — names of xhtml chapters

Tests assert on the actual content produced, not on log lines.
"""
import os
import tempfile

import pytest

from pyffice.ebook import epub as epub_doc


@pytest.fixture
def tmp_path():
    d = tempfile.mkdtemp(prefix="epub_test_")
    try:
        yield d
    finally:
        for root, dirs, files in os.walk(d, topdown=False):
            for f in files:
                os.unlink(os.path.join(root, f))
            for sub in dirs:
                os.rmdir(os.path.join(root, sub))
        os.rmdir(d)


def test_create_produces_valid_epub(tmp_path):
    """create() must produce a non-empty file at the requested path."""
    out = os.path.join(tmp_path, "book.epub")
    epub_doc.create(
        title="Test Book",
        author="Pyffice",
        content="Chapter 1 body text.\nSecond paragraph.",
        output=out,
    )
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0


def test_create_then_list_chapters(tmp_path):
    """list_chapters must return at least one xhtml chapter for a fresh EPUB."""
    out = os.path.join(tmp_path, "book.epub")
    epub_doc.create(title="T", author="A", content="Body", output=out)
    chapters = epub_doc.list_chapters(out)
    assert isinstance(chapters, list)
    assert len(chapters) >= 1
    assert any(name.endswith(".xhtml") for name in chapters)


def test_create_then_read_returns_chapter_text(tmp_path):
    """read() must surface the chapter text we wrote."""
    content = "PYFFICE_EPUB_BODY_MARKER_XYZ123"
    out = os.path.join(tmp_path, "book.epub")
    epub_doc.create(title="T", author="A", content=content, output=out)
    text = epub_doc.read(out)
    assert isinstance(text, str)
    assert "PYFFICE_EPUB_BODY_MARKER_XYZ123" in text


def test_create_then_read_aliases(tmp_path):
    """Module-level load/write aliases must round-trip identically to create/read."""
    out = os.path.join(tmp_path, "aliases.epub")
    epub_doc.create(title="T", author="A", content="alias body", output=out)
    # load is documented alias for read
    assert epub_doc.load(out) == epub_doc.read(out)


def test_list_chapters_missing_file_raises(tmp_path):
    """list_chapters on a missing path must raise a clear error, not return []."""
    missing = os.path.join(tmp_path, "nope.epub")
    with pytest.raises((FileNotFoundError, OSError)):
        epub_doc.list_chapters(missing)
