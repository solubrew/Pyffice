from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/notebooks/.

Coverage:
- PyfficeNotebook construction (defaults, cfg)
- PyfficeNotebook inheritance from PyfficeDocument
- SERIALIZATION_VERSION tuple
- add_cell, clear_cell, clear_cells, del_cell, set_pinned methods
- set_notebook / set_cells change tracking
"""

import pytest

from pyffice.document import PyfficeDocument
from pyffice.notebooks.notebooks import PyfficeNotebook


class TestPyfficeNotebookConstruction:
    """PyfficeNotebook() constructs with empty cells and None notebook."""

    def test_constructs_no_args(self):
        nb = PyfficeNotebook()
        assert nb is not None
        assert nb.cells == []
        assert nb.notebook is None

    def test_constructs_with_cfg(self):
        nb = PyfficeNotebook({"name": "lab"})
        assert nb is not None


class TestPyfficeNotebookInheritance:
    """PyfficeNotebook extends PyfficeDocument."""

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeNotebook, PyfficeDocument)


class TestPyfficeNotebookVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_serialization_version_tuple(self):
        assert hasattr(PyfficeNotebook, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeNotebook.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeNotebook.SERIALIZATION_VERSION) == 3


class TestPyfficeNotebookCellManagement:
    """add_cell / clear_cell / clear_cells / del_cell are fluent."""

    def test_add_cell_returns_self(self):
        logma.debug("TestPyfficeNotebookCellManagement test class")
        nb = PyfficeNotebook()
        cell = {"cell_type": "code", "outputs": []}
        assert nb.add_cell(cell) is nb
        assert nb.cells == [cell]

    def test_add_multiple_cells(self):
        nb = PyfficeNotebook()
        nb.add_cell({"cell_type": "code", "outputs": [1]})
        nb.add_cell({"cell_type": "markdown", "outputs": [2]})
        assert len(nb.cells) == 2

    def test_clear_cell_returns_self(self):
        nb = PyfficeNotebook()
        nb.add_cell({"cell_type": "code", "outputs": [1, 2]})
        assert nb.clear_cell(0) is nb
        assert nb.cells[0]["outputs"] == []

    def test_clear_cells_returns_self(self):
        nb = PyfficeNotebook()
        nb.add_cell({"cell_type": "code", "outputs": [1]})
        nb.add_cell({"cell_type": "md", "outputs": [2]})
        assert nb.clear_cells() is nb
        assert all(c["outputs"] == [] for c in nb.cells)

    def test_del_cell_returns_self(self):
        nb = PyfficeNotebook()
        nb.add_cell({"cell_type": "code"})
        nb.add_cell({"cell_type": "md"})
        assert nb.del_cell(0) is nb
        assert len(nb.cells) == 1
        assert nb.cells[0]["cell_type"] == "md"


class TestPyfficeNotebookSetters:
    """set_notebook / set_cells / set_pinned are fluent and track changes."""

    def test_set_pinned_returns_self(self):
        logma.debug("TestPyfficeNotebookSetters test class")
        nb = PyfficeNotebook()
        assert nb.set_pinned(True) is nb
        assert nb.pinned is True

    def test_set_notebook_returns_self(self):
        nb = PyfficeNotebook()
        nb_def = {"cells": []}
        assert nb.set_notebook(nb_def) is nb
        assert nb.notebook == nb_def

    def test_set_notebook_default_when_none(self):
        nb = PyfficeNotebook()
        nb.set_notebook(None)
        assert nb.notebook == {"cells": []}

    def test_set_cells_returns_self(self):
        nb = PyfficeNotebook()
        cells = [{"cell_type": "code"}]
        assert nb.set_cells(cells) is nb
        assert nb.cells == cells

    def test_set_notebook_records_change(self):
        nb = PyfficeNotebook()
        nb.set_notebook({"cells": []})
        # add_change should have been called
        assert nb.changes is not None
        assert len(nb.changes) > 0
