from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/container/.

Coverage:
- PyfficeBinaryContainer construction (defaults, mode, custom_limits)
- PyfficeBinaryContainer setters: set_limit, add, get, list, info, remove
- PyfficeBinaryContainer get_limit / __len__
- Module helpers: get_limit_for_type, set_limit_for_type
- PyfficeZip / PyfficeTar / PyfficeRAR / Pyffice7Z subclass ArchiveHandler
- Each archive handler has EXTENSIONS and DEFAULT_LIMIT class attributes
"""

import pytest

from pyffice.container.binary import (
    PyfficeBinaryContainer,
    DEFAULT_LIMITS,
    get_limit_for_type,
    set_limit_for_type,
)
from pyffice.container.zip import PyfficeZip
from pyffice.container.tar import PyfficeTar
from pyffice.container.rar import PyfficeRAR
from pyffice.container.sevenzip import Pyffice7Z
from pyffice.io_helpers import ArchiveHandler


class TestPyfficeBinaryContainerConstruction:
    """PyfficeBinaryContainer() constructs with default attributes."""

    def test_constructs_no_args(self):
        logma.debug("TestPyfficeBinaryContainerConstruction test class")
        c = PyfficeBinaryContainer()
        assert c is not None
        assert c.mode == "auto"

    def test_default_documents_empty(self):
        c = PyfficeBinaryContainer()
        assert c._documents == {}
        assert len(c) == 0

    def test_default_limits_copied(self):
        c = PyfficeBinaryContainer()
        assert c.limits == DEFAULT_LIMITS
        # mutating instance limits should not mutate the module constant
        c.limits["zzz"] = 1
        assert "zzz" not in DEFAULT_LIMITS

    def test_constructs_with_mode(self):
        c = PyfficeBinaryContainer(mode="inline")
        assert c.mode == "inline"

    def test_constructs_with_custom_limits(self):
        c = PyfficeBinaryContainer(custom_limits={"png": 10})
        assert c.limits["png"] == 10
        # custom overrides default but keeps other defaults
        assert c.limits["zip"] == DEFAULT_LIMITS["zip"]


class TestPyfficeBinaryContainerGetLimit:
    """get_limit returns the per-extension byte limit."""

    def test_get_limit_known_ext(self):
        c = PyfficeBinaryContainer()
        assert c.get_limit("png") == DEFAULT_LIMITS["png"]

    def test_get_limit_strips_dot(self):
        c = PyfficeBinaryContainer()
        assert c.get_limit(".png") == DEFAULT_LIMITS["png"]

    def test_get_limit_unknown_ext_uses_default(self):
        c = PyfficeBinaryContainer()
        assert c.get_limit("unknownext") == DEFAULT_LIMITS["default"]


class TestPyfficeBinaryContainerSetLimit:
    """set_limit mutates the per-extension byte limit."""

    def test_set_limit(self):
        c = PyfficeBinaryContainer()
        c.set_limit("png", 5)
        assert c.limits["png"] == 5

    def test_set_limit_strips_dot(self):
        c = PyfficeBinaryContainer()
        c.set_limit(".jpg", 7)
        assert c.limits["jpg"] == 7


class TestPyfficeBinaryContainerListInfoRemove:
    """list / info / remove operate on the _documents dict."""

    def test_list_empty(self):
        logma.debug("TestPyfficeBinaryContainerListInfoRemove test class")
        c = PyfficeBinaryContainer()
        assert c.list() == []

    def test_info_missing_returns_none(self):
        c = PyfficeBinaryContainer()
        assert c.info("nope") is None

    def test_remove_missing_returns_false(self):
        c = PyfficeBinaryContainer()
        assert c.remove("nope") is False

    def test_remove_existing(self):
        c = PyfficeBinaryContainer()
        c._documents["x"] = {"mode": "inline", "data": "x", "ext": "txt", "size": 1}
        assert c.remove("x") is True
        assert "x" not in c._documents

    def test_get_missing_returns_none(self):
        c = PyfficeBinaryContainer()
        assert c.get("nope") is None


class TestPyfficeBinaryContainerAdd:
    """add() reads a real file from disk."""

    def test_add_missing_file_returns_false(self, tmp_path):
        logma.debug("TestPyfficeBinaryContainerAdd test class")
        c = PyfficeBinaryContainer()
        missing = str(tmp_path / "nope.png")
        assert c.add("doc", missing) is False
        assert len(c) == 0

    def test_add_inline_mode(self, tmp_path):
        f = tmp_path / "small.txt"
        f.write_bytes(b"hello")
        c = PyfficeBinaryContainer(mode="inline")
        assert c.add("doc", str(f)) is True
        info = c.info("doc")
        assert info["mode"] == "inline"
        assert info["ext"] == "txt"

    def test_add_path_mode(self, tmp_path):
        f = tmp_path / "small.txt"
        f.write_bytes(b"hello")
        c = PyfficeBinaryContainer(mode="path")
        assert c.add("doc", str(f)) is True
        info = c.info("doc")
        assert info["mode"] == "path"

    def test_add_auto_mode_small_file_inline(self, tmp_path):
        f = tmp_path / "small.txt"
        f.write_bytes(b"hello")
        c = PyfficeBinaryContainer(mode="auto")
        c.add("doc", str(f))
        assert c.info("doc")["mode"] == "inline"

    def test_add_raises_when_exceeds_limit(self, tmp_path):
        f = tmp_path / "big.txt"
        f.write_bytes(b"x" * 100)
        c = PyfficeBinaryContainer(custom_limits={"txt": 10})
        with pytest.raises(ValueError):
            c.add("doc", str(f))


class TestGetLimitForType:
    """Module-level get_limit_for_type reads from _limits_storage."""

    def test_known_type(self):
        assert get_limit_for_type("png") == DEFAULT_LIMITS["png"]

    def test_unknown_type_default(self):
        assert get_limit_for_type("zzz") == DEFAULT_LIMITS["default"]

    def test_strips_dot(self):
        assert get_limit_for_type(".png") == DEFAULT_LIMITS["png"]


class TestSetLimitForType:
    """Module-level set_limit_for_type writes to _limits_storage."""

    def test_set_and_get(self):
        set_limit_for_type("custom", 42)
        assert get_limit_for_type("custom") == 42


class TestPyfficeZip:
    """PyfficeZip subclasses ArchiveHandler and has format metadata."""

    def test_subclasses_archive_handler(self):
        logma.debug("TestPyfficeZip test class")
        assert issubclass(PyfficeZip, ArchiveHandler)

    def test_extensions(self):
        assert isinstance(PyfficeZip.EXTENSIONS, set)
        assert ".zip" in PyfficeZip.EXTENSIONS

    def test_default_limit(self):
        assert PyfficeZip.DEFAULT_LIMIT == 256 * 1024 * 1024

    def test_constructs_with_path(self):
        z = PyfficeZip("archive.zip")
        assert z is not None
        assert str(z.file_path).endswith("archive.zip")

    def test_size_limit_classmethod(self):
        assert PyfficeZip.size_limit("anything.zip") == PyfficeZip.DEFAULT_LIMIT


class TestPyfficeTar:
    """PyfficeTar subclasses ArchiveHandler and has format metadata."""

    def test_subclasses_archive_handler(self):
        assert issubclass(PyfficeTar, ArchiveHandler)

    def test_extensions(self):
        assert isinstance(PyfficeTar.EXTENSIONS, set)
        assert ".tar" in PyfficeTar.EXTENSIONS

    def test_default_limit(self):
        assert PyfficeTar.DEFAULT_LIMIT == 256 * 1024 * 1024

    def test_constructs_with_path(self):
        t = PyfficeTar("archive.tar")
        assert t is not None


class TestPyfficeRAR:
    """PyfficeRAR subclasses ArchiveHandler (stub implementation)."""

    def test_subclasses_archive_handler(self):
        assert issubclass(PyfficeRAR, ArchiveHandler)

    def test_extensions(self):
        assert isinstance(PyfficeRAR.EXTENSIONS, set)
        assert ".rar" in PyfficeRAR.EXTENSIONS

    def test_default_limit(self):
        assert PyfficeRAR.DEFAULT_LIMIT == 256 * 1024 * 1024

    def test_constructs_with_path(self):
        r = PyfficeRAR("archive.rar")
        assert r is not None


class TestPyffice7Z:
    """Pyffice7Z subclasses ArchiveHandler (stub implementation)."""

    def test_subclasses_archive_handler(self):
        assert issubclass(Pyffice7Z, ArchiveHandler)

    def test_extensions(self):
        assert isinstance(Pyffice7Z.EXTENSIONS, set)
        assert ".7z" in Pyffice7Z.EXTENSIONS

    def test_default_limit(self):
        assert Pyffice7Z.DEFAULT_LIMIT == 256 * 1024 * 1024

    def test_constructs_with_path(self):
        z = Pyffice7Z("archive.7z")
        assert z is not None
        assert z.mode == "r"
