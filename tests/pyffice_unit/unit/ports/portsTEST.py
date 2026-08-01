from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/ports/.

Coverage:
- PyfficePort: construction + SERIALIZATION_VERSION + to_dict
- Subclass hierarchy: all port classes subclass PyfficePort
- PyfficePortCherryTree: VERSION attribute
- PyfficePortOffice / CSV / Dia / FileSystem / Image / Jupyter /
  Text / WebSession all construct
- PyfficePortExcel / Word (msports)
- PyfficePortGoogleDocs / Forms / Sheets (gports)
"""

import pytest

from pyffice.ports.ports import (
    PyfficePort,
    PyfficePortCherryTree,
    PyfficePortOffice,
    PyfficePortCSV,
    PyfficePortDia,
    PyfficePortFileSystem,
    PyfficePortImage,
    PyfficePortJupyter,
    PyfficePortText,
    PyfficePortWebSession,
)
from pyffice.ports.msports import PyfficePortExcel, PyfficePortWord, read_docx_tables
from pyffice.ports.gports import (
    PyfficePortGoogleDocs,
    PyfficePortGoogleForms,
    PyfficePortGoogleSheets,
)


class TestPyfficePort:
    """PyfficePort is the abstract base for all port classes."""

    def test_serialization_version(self):
        assert isinstance(PyfficePort.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePort.SERIALIZATION_VERSION) == 3

    def test_constructs(self):
        p = PyfficePort()
        assert p is not None

    def test_to_dict_returns_dict(self):
        p = PyfficePort()
        d = p.to_dict()
        assert isinstance(d, dict)


class TestPyfficePortCherryTree:
    """PyfficePortCherryTree is the cherrytree-importer port."""

    def test_subclasses_pyffice_port(self):
        assert issubclass(PyfficePortCherryTree, PyfficePort)

    def test_constructs(self):
        p = PyfficePortCherryTree()
        assert p is not None

    def test_version_attribute(self):
        assert hasattr(PyfficePortCherryTree, "VERSION")
        assert isinstance(PyfficePortCherryTree.VERSION, str)


class TestStandardPorts:
    """All standard format-specific ports construct."""

    @pytest.mark.parametrize("port_class", [
        PyfficePortOffice,
        PyfficePortCSV,
        PyfficePortDia,
        PyfficePortFileSystem,
        PyfficePortImage,
        PyfficePortJupyter,
        PyfficePortText,
        PyfficePortWebSession,
    ])
    def test_subclasses_pyffice_port(self, port_class):
        assert issubclass(port_class, PyfficePort)

    @pytest.mark.parametrize("port_class", [
        PyfficePortOffice,
        PyfficePortCSV,
        PyfficePortDia,
        PyfficePortFileSystem,
        PyfficePortImage,
        PyfficePortJupyter,
        PyfficePortText,
        PyfficePortWebSession,
    ])
    def test_constructs(self, port_class):
        instance = port_class()
        assert instance is not None


class TestMicrosoftPorts:
    """Microsoft Office format ports (Excel, Word)."""

    def test_pyffice_port_excel_subclasses(self):
        logma.debug("TestMicrosoftPorts test class")
        assert issubclass(PyfficePortExcel, PyfficePort)

    def test_pyffice_port_word_subclasses(self):
        assert issubclass(PyfficePortWord, PyfficePort)

    def test_pyffice_port_excel_constructs(self):
        p = PyfficePortExcel()
        assert p is not None

    def test_pyffice_port_word_constructs(self):
        p = PyfficePortWord()
        assert p is not None

    def test_read_docx_tables_missing_file_raises(self, tmp_path):
        # Function takes a path; nonexistent file should error.
        with pytest.raises((FileNotFoundError, OSError, Exception)):
            read_docx_tables(str(tmp_path / "nonexistent.docx"))


class TestGooglePorts:
    """Google Docs/Forms/Sheets ports."""

    @pytest.mark.parametrize("port_class", [
        PyfficePortGoogleDocs,
        PyfficePortGoogleForms,
        PyfficePortGoogleSheets,
    ])
    def test_subclasses_pyffice_port(self, port_class):
        assert issubclass(port_class, PyfficePort)

    @pytest.mark.parametrize("port_class", [
        PyfficePortGoogleDocs,
        PyfficePortGoogleForms,
        PyfficePortGoogleSheets,
    ])
    def test_constructs(self, port_class):
        instance = port_class()
        assert instance is not None