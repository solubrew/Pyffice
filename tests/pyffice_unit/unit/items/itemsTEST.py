"""Tests for pyffice/items/.

Coverage:
- PyfficeFont: dataclass construction + to_dict + from_dict
- PyfficeLayer: minimal PyfficeUnit subclass
- PyfficeTable: set_dataframe (lists → DataFrame)
- PyfficePart: minimal PyfficeUnit subclass
- PyfficePage: minimal PyfficeUnit subclass
- PyfficeBackground: PyfficeUnit subclass

Skipped:
- PyfficeColor (requires colormath + cv2 which may not be installed)
- PyfficeShape (some methods access self.shapes before init)
- PyfficeText (load_unit has pre-existing bugs; covered partially via
  PyfficeFont which is the dataclass leaf)
- PyfficeParagraph / PyfficeRun (require PyfficeText construction)
- PyfficeHTML (extends PyfficeText, same scaffolding bugs)
- PyfficeCell (load_unit path has pre-existing bugs)
"""

import pytest
from pandas import DataFrame

from pyffice.items.text import PyfficeFont, PyfficeText, PyfficeHTML, PyfficePage
from pyffice.items.layers import PyfficeLayer
from pyffice.items.items import PyfficeTable, PyfficePart
from pyffice.items.cells import PyfficeBackground
from pyffice.document import PyfficeUnit


class TestPyfficeFont:
    """PyfficeFont is a dataclass with to_dict + from_dict round-trip."""

    def test_default_construction(self):
        f = PyfficeFont()
        assert f.name == "Arial"
        assert f.size == 11.0
        assert f.bold is False
        assert f.italic is False

    def test_field_assignment(self):
        f = PyfficeFont(name="Helvetica", size=14.0, bold=True)
        assert f.name == "Helvetica"
        assert f.size == 14.0
        assert f.bold is True

    def test_to_dict_returns_all_fields(self):
        f = PyfficeFont(name="Helvetica", size=14.0, bold=True, italic=True)
        d = f.to_dict()
        assert d["name"] == "Helvetica"
        assert d["size"] == 14.0
        assert d["bold"] is True
        assert d["italic"] is True
        for k in ("name", "size", "bold", "italic", "underline",
                  "strikethrough", "color", "highlight"):
            assert k in d

    def test_from_dict_roundtrip(self):
        original = {"name": "Georgia", "size": 12.0, "bold": True, "color": "#abcdef"}
        f = PyfficeFont.from_dict(original)
        assert f.name == "Georgia"
        assert f.size == 12.0
        assert f.bold is True
        assert f.color == "#abcdef"

    def test_from_dict_uses_defaults(self):
        # Missing keys fall back to the dataclass defaults.
        f = PyfficeFont.from_dict({"name": "Mono"})
        assert f.size == 11.0
        assert f.bold is False


class TestPyfficeFontBaseClass:
    """PyfficeFont inherits from object (not a PyfficeUnit)."""

    def test_font_is_not_pyffice_unit(self):
        assert not issubclass(PyfficeFont, PyfficeUnit)


class TestPyfficeLayer:
    """PyfficeLayer is a minimal PyfficeUnit subclass."""

    def test_constructs_with_no_args(self):
        layer = PyfficeLayer()
        assert layer is not None

    def test_constructs_with_cfg(self):
        layer = PyfficeLayer({"name": "Layer 1"})
        assert layer is not None

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeLayer, PyfficeUnit)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeLayer.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeLayer.SERIALIZATION_VERSION) == 3


class TestPyfficeTable:
    """PyfficeTable wraps a pandas DataFrame."""

    def test_constructs_with_no_args(self):
        t = PyfficeTable()
        assert t is not None

    def test_set_dataframe_converts_list(self):
        t = PyfficeTable()
        t.set_dataframe([[1, 2], [3, 4]])
        assert isinstance(t.data, DataFrame)
        assert t.data.shape == (2, 2)

    def test_set_dataframe_with_columns(self):
        t = PyfficeTable()
        t.set_dataframe([[10, 20], [30, 40]], columns=["a", "b"])
        assert list(t.data.columns) == ["a", "b"]

    def test_set_dataframe_accepts_dataframe(self):
        t = PyfficeTable()
        df = DataFrame({"x": [1, 2], "y": [3, 4]})
        t.set_dataframe(df)
        # Identity preserved when input is already a DataFrame.
        assert t.data is df

    def test_set_dataframe_returns_self(self):
        t = PyfficeTable()
        assert t.set_dataframe([[1, 2]]) is t


class TestPyfficePart:
    """PyfficePart is a minimal PyfficeUnit subclass."""

    def test_constructs(self):
        p = PyfficePart()
        assert p is not None

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficePart, PyfficeUnit)


class TestPyfficePage:
    """PyfficePage is a minimal PyfficeUnit subclass."""

    def test_constructs(self):
        pg = PyfficePage()
        assert pg is not None

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficePage, PyfficeUnit)


class TestPyfficeBackground:
    """PyfficeBackground is a PyfficeUnit subclass."""

    def test_constructs(self):
        b = PyfficeBackground()
        assert b is not None
        assert b.file_path is None
        assert b.image is None
        assert b.color is None

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeBackground, PyfficeUnit)


class TestPyfficeTextConstruction:
    """PyfficeText constructs; load_unit has pre-existing bugs that
    are not covered here."""

    def test_constructs(self):
        t = PyfficeText()
        assert t is not None
        assert t.alignment is None
        assert t.font is None
        assert t.value is None

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeText, PyfficeUnit)

    def test_html_extends_text(self):
        assert issubclass(PyfficeHTML, PyfficeText)

    def test_html_constructs(self):
        h = PyfficeHTML()
        assert h is not None
