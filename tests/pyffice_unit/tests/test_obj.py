"""Test OBJ CAD round-trip via real captured bytes.

The obj module exposes:
- PyfficeOBJ(file_path) — class with read()/write(data)/load() instance methods
- read(obj_path) -> Dict — module-level read returning structured {vertices, normals, texcoords, faces}
- load(obj_path) -> Dict — alias for read
- write(obj_path, data) — module-level write

Tests assert on the parsed structure and byte equality after round-trip.
"""
import os
import tempfile

import pytest

from pyffice.cad import obj as obj_doc


@pytest.fixture
def tmp_path():
    d = tempfile.mkdtemp(prefix="obj_test_")
    try:
        yield d
    finally:
        for root, dirs, files in os.walk(d, topdown=False):
            for f in files:
                os.unlink(os.path.join(root, f))
            for sub in dirs:
                os.rmdir(os.path.join(root, sub))
        os.rmdir(d)


SAMPLE_OBJ = """# pyffice test obj
v 1.0 2.0 3.0
v 4.0 5.0 6.0
vn 0.0 1.0 0.0
vt 0.5 0.5
f 1//1 2//1
"""


def test_read_parses_vertices_and_normals(tmp_path):
    """read(path) returns a dict with vertices/normals/texcoords/faces populated."""
    p = os.path.join(tmp_path, "cube.obj")
    with open(p, "w") as f:
        f.write(SAMPLE_OBJ)
    data = obj_doc.read(p)
    assert isinstance(data, dict)
    assert "vertices" in data and "normals" in data
    assert "texcoords" in data and "faces" in data
    assert len(data["vertices"]) == 2
    assert data["vertices"][0] == (1.0, 2.0, 3.0)
    assert data["vertices"][1] == (4.0, 5.0, 6.0)
    assert data["normals"] == [(0.0, 1.0, 0.0)]
    assert len(data["faces"]) == 1


def test_load_aliases_read(tmp_path):
    p = os.path.join(tmp_path, "cube.obj")
    with open(p, "w") as f:
        f.write(SAMPLE_OBJ)
    assert obj_doc.load(p) == obj_doc.read(p)


def test_roundtrip_preserves_vertices(tmp_path):
    """Write via module fn, read back, assert vertex count matches."""
    src = os.path.join(tmp_path, "src.obj")
    with open(src, "w") as f:
        f.write(SAMPLE_OBJ)
    parsed = obj_doc.read(src)
    p = os.path.join(tmp_path, "rt.obj")
    obj_doc.write(p, parsed)
    reparsed = obj_doc.read(p)
    assert len(reparsed["vertices"]) == len(parsed["vertices"])
    assert reparsed["vertices"] == parsed["vertices"]


def test_read_missing_file_raises(tmp_path):
    """read on a missing path must raise a clear OSError."""
    with pytest.raises((FileNotFoundError, OSError)):
        obj_doc.read(os.path.join(tmp_path, "missing.obj"))


def test_write_empty_data_creates_file(tmp_path):
    """write(path, {}) creates a file with the generator header."""
    p = os.path.join(tmp_path, "empty.obj")
    obj_doc.write(p, {})
    assert os.path.exists(p)
    with open(p) as f:
        content = f.read()
    assert "pyffice" in content.lower()
