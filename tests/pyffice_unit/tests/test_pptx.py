"""Test PPTX round-trip via real captured bytes.

The pptx module exposes module-level helpers (load/read/write/dump) that
wrap ``pyffice.io_helpers.load_bytes`` / ``write_bytes``. Tests assert
on the bytes that come back, not on log lines.
"""

import os
import tempfile

import pytest

from pyffice.ports import pptx as pptx_doc


@pytest.fixture
def tmp_path():
    d = tempfile.mkdtemp(prefix="pptx_test_")
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
    payload = b"PYFFICE_PPTX_TEST_v1\x00\x01\x02"
    out_path = os.path.join(tmp_path, "roundtrip.pptx")
    pptx_doc.write(payload, out_path)
    assert os.path.exists(out_path)
    assert os.path.getsize(out_path) == len(payload)
    recovered = pptx_doc.read(out_path)
    assert recovered == payload


def test_dump_is_alias_for_write(tmp_path):
    payload = b"PYFFICE_PPTX_DUMP_v1"
    p1 = os.path.join(tmp_path, "via_write.pptx")
    p2 = os.path.join(tmp_path, "via_dump.pptx")
    pptx_doc.write(payload, p1)
    pptx_doc.dump(payload, p2)
    assert pptx_doc.read(p1) == pptx_doc.read(p2)


def test_load_matches_read(tmp_path):
    payload = b"PYFFICE_PPTX_LOAD_v1"
    out_path = os.path.join(tmp_path, "load.pptx")
    pptx_doc.write(payload, out_path)
    assert pptx_doc.load(out_path) == pptx_doc.read(out_path)


def test_read_missing_file_raises(tmp_path):
    with pytest.raises((FileNotFoundError, OSError)):
        pptx_doc.read(os.path.join(tmp_path, "does_not_exist.pptx"))
