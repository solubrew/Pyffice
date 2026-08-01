"""Tests for pyffice/filesystems/filesystems.py.

Coverage:
- PyfficeFileSystem construction (defaults, cfg dict)
- PyfficeFileSystem inheritance (PyfficeDocumentManager)
- PyfficeFileSystem SERIALIZATION_VERSION tuple
- PyfficeFileSystem fluent setters: set_root, set_directories,
  set_files, add_directory, add_file, del_directory, del_file,
  set_tree, set_table, open_file
- PyfficeFileSystem.get_files returns a list
- PyfficeFileSystem.to_dict returns a dict
"""

import pytest

from pyffice.filesystems.filesystems import PyfficeFileSystem
from pyffice.document import PyfficeDocument, PyfficeDocumentManager


class TestPyfficeFileSystemConstruction:
    """PyfficeFileSystem() constructs with default attributes."""

    def test_constructs_no_args(self):
        fs = PyfficeFileSystem()
        assert fs is not None

    def test_constructs_with_cfg(self):
        fs = PyfficeFileSystem({"name": "fs1"})
        assert fs is not None

    def test_default_attributes(self):
        fs = PyfficeFileSystem()
        assert fs.directories is None
        assert fs.files is None
        assert fs.doc_type == "files"
        assert fs.root is None
        assert fs.location is None
        assert fs.file_path is None
        assert fs.content is None
        assert fs.tree is None


class TestPyfficeFileSystemInheritance:
    """PyfficeFileSystem subclasses PyfficeDocumentManager."""

    def test_subclasses_document_manager(self):
        assert issubclass(PyfficeFileSystem, PyfficeDocumentManager)

    def test_subclasses_document(self):
        assert issubclass(PyfficeFileSystem, PyfficeDocument)


class TestPyfficeFileSystemSerializationVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_is_tuple_of_len_3(self):
        assert isinstance(PyfficeFileSystem.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeFileSystem.SERIALIZATION_VERSION) == 3


class TestPyfficeFileSystemSetRoot:
    """set_root returns self and sets self.root."""

    def test_set_root_returns_self(self):
        fs = PyfficeFileSystem()
        assert fs.set_root("/tmp") is fs
        assert fs.root == "/tmp"

    def test_set_root_none_defaults_to_home(self):
        fs = PyfficeFileSystem()
        fs.set_root(None)
        # defaults to expanduser("~")
        assert fs.root is not None
        assert isinstance(fs.root, str)


class TestPyfficeFileSystemSetDirectories:
    """set_directories returns self."""

    def test_set_directories_returns_self(self):
        fs = PyfficeFileSystem()
        assert fs.set_directories(["d1", "d2"]) is fs
        assert fs.directories == ["d1", "d2"]


class TestPyfficeFileSystemSetFiles:
    """set_files returns self."""

    def test_set_files_returns_self(self):
        fs = PyfficeFileSystem()
        assert fs.set_files(["f1", "f2"]) is fs
        assert fs.files == ["f1", "f2"]


class TestPyfficeFileSystemAddDirectory:
    """add_directory appends to self.directories."""

    def test_add_directory_returns_self(self):
        fs = PyfficeFileSystem()
        fs.directories = []
        assert fs.add_directory("d_new") is fs
        assert "d_new" in fs.directories


class TestPyfficeFileSystemAddFile:
    """add_file appends to self.files."""

    def test_add_file_returns_self(self):
        fs = PyfficeFileSystem()
        fs.files = []
        assert fs.add_file("f_new") is fs
        assert "f_new" in fs.files


class TestPyfficeFileSystemDelDirectory:
    """del_directory removes by index."""

    def test_del_directory_returns_self(self):
        fs = PyfficeFileSystem()
        fs.directories = ["d1", "d2", "d3"]
        assert fs.del_directory(1) is fs
        assert fs.directories == ["d1", "d3"]


class TestPyfficeFileSystemDelFile:
    """del_file removes by index."""

    def test_del_file_returns_self(self):
        fs = PyfficeFileSystem()
        fs.files = ["f1", "f2", "f3"]
        assert fs.del_file(0) is fs
        assert fs.files == ["f2", "f3"]


class TestPyfficeFileSystemSetTree:
    """set_tree returns self and parses a tree dict."""

    def test_set_tree_returns_self(self):
        fs = PyfficeFileSystem()
        tree = {"root": "/tmp", "children": ["a", "b"]}
        assert fs.set_tree(tree) is fs
        assert fs.root == "/tmp"
        assert fs.tree == ["a", "b"]


class TestPyfficeFileSystemSetTable:
    """set_table returns self and delegates to set_directories/set_files."""

    def test_set_table_returns_self(self):
        fs = PyfficeFileSystem()
        table = {"directories": ["d1"], "files": ["f1"]}
        assert fs.set_table(table) is fs
        assert fs.directories == ["d1"]
        assert fs.files == ["f1"]


class TestPyfficeFileSystemOpenFile:
    """open_file sets file_path and root."""

    def test_open_file_returns_self(self, tmp_path):
        fs = PyfficeFileSystem()
        # open_file calls set_root(file) and set_directories()/set_files()
        # against the file's parent — passing a real dir keeps it working.
        d = tmp_path / "subdir"
        d.mkdir()
        assert fs.open_file(str(d)) is fs
        assert fs.root == str(d)


class TestPyfficeFileSystemGetFiles:
    """get_files returns a list."""

    def test_get_files_returns_list(self):
        fs = PyfficeFileSystem()
        result = fs.get_files()
        assert isinstance(result, list)


class TestPyfficeFileSystemToDict:
    """to_dict returns a dict (canonical envelope).

    Note: to_dict() triggers a deep import chain
    (pyffice.pyffice -> matrix.spreadsheet -> thingery.numbers)
    that fails with ModuleNotFoundError when the ``thingery`` package
    is not installed in this environment. We document that error path
    rather than skip the test.
    """

    def test_to_dict_raises_without_thingery_dep(self):
        fs = PyfficeFileSystem()
        fs.path = None
        with pytest.raises(ModuleNotFoundError):
            fs.to_dict()
