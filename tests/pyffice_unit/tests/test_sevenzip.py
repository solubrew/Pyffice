"""Test 7-Zip archive module.

The sevenzip module exposes:
- Pyffice7Z(file_path, mode) — stub class (real 7z requires py7zr lib)
- load/read/write/dump — module-level bytes helpers
- compress_7z(source_path, archive_path) — stub (writes empty archive)
- extract_7z(archive_path, dest_path) — stub (no-op)

Tests assert on the byte-level behavior of the actual implementations.
Full 7z compression is out of scope until a third-party library is integrated.
"""
import os
import tempfile

import pytest

from pyffice.container import sevenzip as sevenzip_doc


@pytest.fixture
def tmp_path():
    d = tempfile.mkdtemp(prefix="sevenzip_test_")
    try:
        yield d
    finally:
        for root, dirs, files in os.walk(d, topdown=False):
            for f in files:
                os.unlink(os.path.join(root, f))
            for sub in dirs:
                os.rmdir(os.path.join(root, sub))
        os.rmdir(d)


def test_load_read_write_bytes_roundtrip(tmp_path):
    payload = b"PYFFICE_7Z_TEST_v1\x00\x01"
    out = os.path.join(tmp_path, "data.7z")
    sevenzip_doc.write(payload, out)
    assert os.path.getsize(out) == len(payload)
    assert sevenzip_doc.read(out) == payload
    assert sevenzip_doc.load(out) == sevenzip_doc.read(out)


def test_pyffice_7z_class_records_file_path_and_mode():
    h = sevenzip_doc.Pyffice7Z("/tmp/foo.7z", "w")
    assert h.file_path == "/tmp/foo.7z"
    assert h.mode == "w"


def test_pyffice_7z_read_write_bytes_methods(tmp_path):
    """Pyffice7Z has read_bytes() / write_bytes_to() thin wrappers around module fns."""
    payload = b"PYFFICE_7Z_BYTES_VIA_CLASS"
    out = os.path.join(tmp_path, "via_class.7z")
    h = sevenzip_doc.Pyffice7Z(out, "w")
    h.write_bytes_to(payload)
    assert sevenzip_doc.Pyffice7Z(out, "r").read_bytes() == payload


def test_compress_7z_stub_writes_empty(tmp_path):
    """compress_7z is a documented stub that writes an empty archive (no real compression)."""
    src = os.path.join(tmp_path, "src.bin")
    arc = os.path.join(tmp_path, "out.7z")
    sevenzip_doc.write(b"PYFFICE_7Z_COMPRESS_INPUT", src)
    sevenzip_doc.compress_7z(src, arc)
    assert os.path.exists(arc)
    # Stub: archive is empty (0 bytes) — actual compression is out of scope
    assert os.path.getsize(arc) == 0


def test_extract_7z_stub_is_noop(tmp_path):
    """extract_7z is a documented stub (no-op until py7zr lib is integrated)."""
    arc = os.path.join(tmp_path, "fake.7z")
    dest = os.path.join(tmp_path, "dest_dir")
    sevenzip_doc.write(b"x", arc)
    assert not os.path.exists(dest)
    sevenzip_doc.extract_7z(arc, dest)
    # Stub behavior: dest does NOT get created (no-op)
    assert not os.path.exists(dest)
