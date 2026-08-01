"""Test DXF CAD round-trip via real captured bytes.

The dxf module exposes:
- PyfficeDXF(file_path, cfg) — class with read()/write(data) instance methods
- load(path) -> str — module-level read (returns text)
- read(path) -> str — alias for load
- write(data, path) — module-level write
- dump(data, path) — alias for write

Tests assert on the actual text bytes, not on log lines.
"""
import os
import tempfile

import pytest

from pyffice.cad import dxf as dxf_doc


@pytest.fixture
def tmp_path():
    d = tempfile.mkdtemp(prefix="dxf_test_")
    try:
        yield d
    finally:
        for root, dirs, files in os.walk(d, topdown=False):
            for f in files:
                os.unlink(os.path.join(root, f))
            for sub in dirs:
                os.rmdir(os.path.join(root, sub))
        os.rmdir(d)


# Minimal DXF structure — a single LINE entity
SAMPLE_DXF = """0
SECTION
2
ENTITIES
0
LINE
8
0
10
0.0
20
0.0
30
0.0
11
10.0
21
10.0
31
0.0
0
ENDSEC
0
EOF
"""


def test_load_read_return_text(tmp_path):
    """load(path) and read(path) return the file text content."""
    p = os.path.join(tmp_path, "line.dxf")
    with open(p, "w") as f:
        f.write(SAMPLE_DXF)
    text = dxf_doc.load(p)
    assert "SECTION" in text
    assert "LINE" in text
    assert dxf_doc.read(p) == text


def test_write_dump_roundtrip(tmp_path):
    """write(data, path) + dump(data, path) produce files with identical content."""
    payload = "PYFFICE_DXF_PAYLOAD_v1\n"
    p1 = os.path.join(tmp_path, "via_write.dxf")
    p2 = os.path.join(tmp_path, "via_dump.dxf")
    dxf_doc.write(payload, p1)
    dxf_doc.dump(payload, p2)
    assert os.path.getsize(p1) == len(payload)
    assert dxf_doc.read(p1) == dxf_doc.read(p2)


def test_pyffice_dxf_class_reads_text(tmp_path):
    """PyfficeDXF(path).read() returns the file text content."""
    p = os.path.join(tmp_path, "via_class.dxf")
    with open(p, "w") as f:
        f.write(SAMPLE_DXF)
    d = dxf_doc.PyfficeDXF(p)
    text = d.read()
    assert "ENTITIES" in text


def test_read_missing_file_raises(tmp_path):
    with pytest.raises((FileNotFoundError, OSError)):
        dxf_doc.read(os.path.join(tmp_path, "missing.dxf"))


def test_write_then_load_roundtrip(tmp_path):
    """Write payload, load it back, bytes match."""
    p = os.path.join(tmp_path, "roundtrip.dxf")
    payload = SAMPLE_DXF
    dxf_doc.write(payload, p)
    assert dxf_doc.load(p) == payload
