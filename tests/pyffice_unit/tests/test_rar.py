"""Test RAR archive module.

The rar module exposes:
- PyfficeRAR(file_path, mode) — stub class (real RAR requires external rarfile lib)
- load/read/write/dump — module-level bytes helpers
- compress_rar(source_path, archive_path) — stub (copies source to archive)
- extract_rar(archive_path, dest_path) — stub (no-op)

Tests assert on the byte-level behavior of the actual implementations.
The stub behavior is documented in pyffice/container/rar.py and tested
as-is; full RAR compression is out of scope until a third-party library
is integrated.
"""
import os
import tempfile

import pytest

from pyffice.container import rar as rar_doc


@pytest.fixture
def tmp_path():
    d = tempfile.mkdtemp(prefix="rar_test_")
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
    """load/read/write are thin byte I/O wrappers — round-trip must be lossless."""
    payload = b"PYFFICE_RAR_TEST_v1\x00\x01"
    out = os.path.join(tmp_path, "data.rar")
    rar_doc.write(payload, out)
    assert os.path.getsize(out) == len(payload)
    assert rar_doc.read(out) == payload
    assert rar_doc.load(out) == rar_doc.read(out)
    assert rar_doc.dump is rar_doc.write or rar_doc.dump  # dump exists


def test_pyffice_rar_class_records_file_path():
    """PyfficeRAR(file_path, mode) stores the path on the instance."""
    h = rar_doc.PyfficeRAR("/tmp/foo.rar", "r")
    assert h.file_path == "/tmp/foo.rar"


def test_pyffice_rar_inline_size_check(tmp_path):
    """PyfficeRAR.inline(path) returns True for small files, False for >DEFAULT_LIMIT."""
    # Tiny file -> inline True
    small = os.path.join(tmp_path, "small.rar")
    rar_doc.write(b"x", small)
    assert rar_doc.PyfficeRAR.inline(small) is True
    # Missing path -> OSError (size check requires real file)
    missing = os.path.join(tmp_path, "missing.rar")
    with pytest.raises((FileNotFoundError, OSError)):
        rar_doc.PyfficeRAR.inline(missing)


def test_compress_rar_stub_copies_bytes(tmp_path):
    """compress_rar is a documented stub that copies source->archive (no real compression)."""
    src = os.path.join(tmp_path, "src.bin")
    arc = os.path.join(tmp_path, "out.rar")
    payload = b"PYFFICE_RAR_COMPRESS_STUB"
    rar_doc.write(payload, src)
    rar_doc.compress_rar(src, arc)
    assert os.path.exists(arc)
    assert rar_doc.read(arc) == payload


def test_extract_rar_stub_is_noop(tmp_path):
    """extract_rar is a documented stub (no-op until rarfile lib is integrated)."""
    # Pre-condition: dest doesn't exist
    arc = os.path.join(tmp_path, "fake.rar")
    dest = os.path.join(tmp_path, "dest_dir")
    rar_doc.write(b"x", arc)
    assert not os.path.exists(dest)
    # Stub call must not raise, even though it doesn't actually extract
    rar_doc.extract_rar(arc, dest)
    # Stub behavior: dest does NOT get created (no-op)
    assert not os.path.exists(dest)
