"""Test TAR archive round-trip via real captured bytes.

The tar module exposes:
- PyfficeTar(file_path) — class implementing ArchiveHandler hooks
- read(tar_path) -> List[Dict] — list member metadata
- load(tar_path) -> List[Dict] — alias for read
- write(tar_path, files: Dict[str, str], compression='gz') — create archive
- extract/extract_file — module-level extract helpers

Tests assert on the real tar contents, not on log lines.
"""
import os
import tarfile
import tempfile

import pytest

from pyffice.container import tar as tar_doc


@pytest.fixture
def tmp_path():
    d = tempfile.mkdtemp(prefix="tar_test_")
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
    """Two small text files keyed by arcname."""
    src1 = os.path.join(tmp_path, "src1.txt")
    src2 = os.path.join(tmp_path, "src2.txt")
    payload1 = b"PYFFICE_TAR_FILE_ONE\n"
    payload2 = b"PYFFICE_TAR_FILE_TWO\n"
    with open(src1, "wb") as f:
        f.write(payload1)
    with open(src2, "wb") as f:
        f.write(payload2)
    return {"file1.txt": src1, "file2.txt": src2}, payload1, payload2


def test_write_creates_archive_with_members(sample_files, tmp_path):
    """write(path, files) must produce a readable tar archive containing the given members."""
    files, _, _ = sample_files
    arc = os.path.join(tmp_path, "out.tar")
    tar_doc.write(arc, files)
    assert os.path.exists(arc)
    assert os.path.getsize(arc) > 0
    with tarfile.open(arc, "r:*") as tf:
        names = sorted(tf.getnames())
    assert set(names) == set(files.keys())


def test_read_lists_member_metadata(sample_files, tmp_path):
    """read(path) returns a list of dicts (name/size/type) per member."""
    files, _, _ = sample_files
    arc = os.path.join(tmp_path, "out.tar")
    tar_doc.write(arc, files)
    members = tar_doc.read(arc)
    assert isinstance(members, list)
    assert len(members) == len(files)
    assert {m["name"] for m in members} == set(files.keys())
    assert all(m["size"] > 0 for m in members)


def test_load_aliases_read(sample_files, tmp_path):
    """load(path) returns identical results to read(path)."""
    files, _, _ = sample_files
    arc = os.path.join(tmp_path, "out.tar")
    tar_doc.write(arc, files)
    assert tar_doc.load(arc) == tar_doc.read(arc)


def test_roundtrip_preserves_bytes(sample_files, tmp_path):
    """Write via tar_doc, extract via stdlib tarfile, assert byte equality."""
    files, payload1, payload2 = sample_files
    arc = os.path.join(tmp_path, "roundtrip.tar")
    tar_doc.write(arc, files)
    with tarfile.open(arc, "r:*") as tf:
        extracted1 = tf.extractfile("file1.txt").read()
        extracted2 = tf.extractfile("file2.txt").read()
    assert extracted1 == payload1
    assert extracted2 == payload2


def test_write_with_gz_compression(sample_files, tmp_path):
    """Default compression='gz' produces a gzipped tar — verify by extension sniff."""
    files, _, _ = sample_files
    arc = os.path.join(tmp_path, "out.tar.gz")
    tar_doc.write(arc, files, compression="gz")
    with open(arc, "rb") as f:
        magic = f.read(2)
    assert magic == b"\x1f\x8b"  # gzip magic number


def test_read_missing_file_raises(tmp_path):
    """read on a missing path must raise a clear error."""
    with pytest.raises((FileNotFoundError, OSError)):
        tar_doc.read(os.path.join(tmp_path, "missing.tar"))
