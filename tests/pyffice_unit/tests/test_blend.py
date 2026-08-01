"""Test BLEND (Blender) module — class exists as PyfficeBLEND.

The blend module exposes:
- PyfficeBLEND(file_path, cfg) — class with read()/write(data) instance methods
- load(path) -> bytes, read(path) -> bytes, write(data, path), dump(data, path)

Tests assert on real bytes (BLEND is a binary format; we treat it as
opaque payload for round-trip purposes).
"""
import os
import tempfile

import pytest

from pyffice.cad import blend


@pytest.fixture
def tmp_path():
    d = tempfile.mkdtemp(prefix="blend_test_")
    try:
        yield d
    finally:
        for root, dirs, files in os.walk(d, topdown=False):
            for f in files:
                os.unlink(os.path.join(root, f))
            for sub in dirs:
                os.rmdir(os.path.join(root, sub))
        os.rmdir(d)


def test_blend_module_imports():
    """The blend module is importable."""
    assert blend is not None


def test_pyffice_blend_class_exists():
    """PyfficeBLEND is the documented class name (not 'BlendFile')."""
    assert hasattr(blend, "PyfficeBLEND")


def test_load_read_write_bytes_roundtrip(tmp_path):
    payload = b"PYFFICE_BLEND_TEST_v1\x00\x01"
    out = os.path.join(tmp_path, "data.blend")
    blend.write(payload, out)
    assert os.path.getsize(out) == len(payload)
    assert blend.read(out) == payload
    assert blend.load(out) == blend.read(out)


def test_pyffice_blend_class_roundtrip(tmp_path):
    """PyfficeBLEND(path).read() and .write(data) round-trip via the class API."""
    payload = b"PYFFICE_BLEND_CLASS_ROUNDTRIP_v1"
    out = os.path.join(tmp_path, "via_class.blend")
    h = blend.PyfficeBLEND(out)
    h.write(payload)
    h2 = blend.PyfficeBLEND(out)
    assert h2.read() == payload


def test_read_missing_file_raises(tmp_path):
    with pytest.raises((FileNotFoundError, OSError)):
        blend.read(os.path.join(tmp_path, "missing.blend"))
