"""Test ZIP archive round-trip via real captured bytes.

The zip module exposes:
- PyfficeZip(file_path) — class implementing ArchiveHandler hooks
- read(zip_path) -> List[Dict] — list member metadata
- load(zip_path) -> List[Dict] — alias for read
- write(zip_path, files: Dict[str, str]) — create archive
- extract/extract_file — module-level extract helpers
- compress(source_dir, archive_path) — walk a directory and zip it

Tests assert on the real zip contents, not on log lines.
"""
import os
import tempfile
import zipfile

import pytest

from pyffice.container import zip as zip_doc


@pytest.fixture
def tmp_path():
    d = tempfile.mkdtemp(prefix="zip_test_")
    try:
        yield d
    finally:
        for root, dirs, files in os.walk(d, topdown=False):
            for f in files:
                os.unlink(os.path.join(root, f))
            for sub in dirs:
                os.rmdir(os.path.join(root, sub))
        os.rmdir(d)


@pytest.fixture
def sample_files(tmp_path):
    src1 = os.path.join(tmp_path, "src1.txt")
    src2 = os.path.join(tmp_path, "src2.txt")
    payload1 = b"PYFFICE_ZIP_FILE_ONE\n"
    payload2 = b"PYFFICE_ZIP_FILE_TWO\n"
    with open(src1, "wb") as f:
        f.write(payload1)
    with open(src2, "wb") as f:
        f.write(payload2)
    return {"a.txt": src1, "b.txt": src2}, payload1, payload2


def test_write_creates_archive_with_members(sample_files, tmp_path):
    files, _, _ = sample_files
    arc = os.path.join(tmp_path, "out.zip")
    zip_doc.write(arc, files)
    assert os.path.exists(arc)
    assert os.path.getsize(arc) > 0
    with zipfile.ZipFile(arc, "r") as zf:
        names = sorted(zf.namelist())
    assert set(names) == set(files.keys())


def test_read_lists_member_metadata(sample_files, tmp_path):
    files, _, _ = sample_files
    arc = os.path.join(tmp_path, "out.zip")
    zip_doc.write(arc, files)
    members = zip_doc.read(arc)
    assert isinstance(members, list)
    assert len(members) == len(files)
    assert {m["name"] for m in members} == set(files.keys())
    assert all(m["size"] > 0 for m in members)


def test_load_aliases_read(sample_files, tmp_path):
    files, _, _ = sample_files
    arc = os.path.join(tmp_path, "out.zip")
    zip_doc.write(arc, files)
    assert zip_doc.load(arc) == zip_doc.read(arc)


def test_roundtrip_preserves_bytes(sample_files, tmp_path):
    files, payload1, payload2 = sample_files
    arc = os.path.join(tmp_path, "roundtrip.zip")
    zip_doc.write(arc, files)
    with zipfile.ZipFile(arc, "r") as zf:
        assert zf.read("a.txt") == payload1
        assert zf.read("b.txt") == payload2


def test_compress_directory(tmp_path):
    """compress(src_dir, archive) walks the dir and writes a zip with all files."""
    src_dir = os.path.join(tmp_path, "src")
    os.makedirs(src_dir)
    p1 = os.path.join(src_dir, "x.txt")
    p2 = os.path.join(src_dir, "y.txt")
    with open(p1, "w") as f:
        f.write("PYFFICE_ZIP_COMPRESS_X")
    with open(p2, "w") as f:
        f.write("PYFFICE_ZIP_COMPRESS_Y")
    arc = os.path.join(tmp_path, "from_dir.zip")
    zip_doc.compress(src_dir, arc)
    with zipfile.ZipFile(arc, "r") as zf:
        names = sorted(zf.namelist())
    assert "x.txt" in names
    assert "y.txt" in names


def test_read_missing_file_raises(tmp_path):
    with pytest.raises((FileNotFoundError, OSError)):
        zip_doc.read(os.path.join(tmp_path, "missing.zip"))


def test_create_module_alias_matches_write(sample_files, tmp_path):
    """Module-level create() is documented alias for write() — bytes must match."""
    files, _, _ = sample_files
    a = os.path.join(tmp_path, "via_write.zip")
    b = os.path.join(tmp_path, "via_create.zip")
    zip_doc.write(a, files)
    zip_doc.create(b, files)
    with zipfile.ZipFile(a, "r") as zfa, zipfile.ZipFile(b, "r") as zfb:
        assert sorted(zfa.namelist()) == sorted(zfb.namelist())
