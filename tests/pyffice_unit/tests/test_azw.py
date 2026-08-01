"""Test AZW ebook round-trip via real captured bytes.

The azw module exposes module-level helpers (load/read/write/dump) that
wrap ``pyffice.io_helpers.load_bytes`` / ``write_bytes``. Tests assert
on the bytes that come back, not on log lines.
"""
import os
import tempfile

import pytest

from pyffice.ebook import azw as azw_doc


@pytest.fixture
def tmp_path():
    """Per-test scratch directory that gets cleaned up."""
    d = tempfile.mkdtemp(prefix="azw_test_")
    try:
        yield d
    finally:
        for root, dirs, files in os.walk(d, topdown=False):
            for f in files:
                os.unlink(os.path.join(root, f))
            for sub in dirs:
                os.rmdir(os.path.join(root, sub))
        os.rmdir(d)


def test_read_write_roundtrip(tmp_path):
    """Write a known byte payload, read it back, assert equality."""
    payload = b"PYFFICE_AZW_TEST_v1\x00\x01\x02"
    out_path = os.path.join(tmp_path, "roundtrip.azw")
    azw_doc.write(payload, out_path)
    assert os.path.exists(out_path)
    assert os.path.getsize(out_path) == len(payload)
    recovered = azw_doc.read(out_path)
    assert recovered == payload


def test_dump_is_alias_for_write(tmp_path):
    """dump(data, path) and write(data, path) must produce identical bytes."""
    payload = b"PYFFICE_AZW_DUMP_v1"
    p1 = os.path.join(tmp_path, "via_write.azw")
    p2 = os.path.join(tmp_path, "via_dump.azw")
    azw_doc.write(payload, p1)
    azw_doc.dump(payload, p2)
    assert azw_doc.read(p1) == azw_doc.read(p2)


def test_load_matches_read(tmp_path):
    """load(path) and read(path) are documented aliases — bytes must match."""
    payload = b"PYFFICE_AZW_LOAD_v1"
    out_path = os.path.join(tmp_path, "load.azw")
    azw_doc.write(payload, out_path)
    assert azw_doc.load(out_path) == azw_doc.read(out_path)


def test_read_missing_file_raises(tmp_path):
    """Reading a non-existent file must surface a clear OSError (not silently return None)."""
    missing = os.path.join(tmp_path, "does_not_exist.azw")
    with pytest.raises((FileNotFoundError, OSError)):
        azw_doc.read(missing)
