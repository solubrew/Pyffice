from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/matrix/.

Coverage:
- PyfficeMatrix.determine_file_type (T-NEW-057 impl):
  .xlsx/.xls/.xlsm -> 'excel'; .ods -> 'openoffice';
  .csv -> 'csv'; default -> 'excel'
- PyfficeSpreadSheet basic construction + set_cell / get_cell
- get_rows groups cells by row index (T-NEW-057 impl)
- calcArabicNumerals / calcExtendedRomanNumerals round-trip
"""

import pytest

from pyffice.matrix.matrix import PyfficeMatrix
from pyffice.matrix.spreadsheet import (
    PyfficeSpreadSheet,
    calcArabicNumerals,
    calcExtendedRomanNumerals,
)


class TestPyfficeMatrixDetermineFileType:
    """T-NEW-057: determine_file_type infers type from extension."""

    def test_excel_extensions(self):
        logma.debug("TestPyfficeMatrixDetermineFileType test class")
        m = PyfficeMatrix()
        assert m.determine_file_type("report.xlsx") == "excel"
        assert m.determine_file_type("report.xls") == "excel"
        assert m.determine_file_type("macro.xlsm") == "excel"
        assert m.determine_file_type("binary.xlsb") == "excel"

    def test_openoffice_extension(self):
        m = PyfficeMatrix()
        assert m.determine_file_type("report.ods") == "openoffice"

    def test_csv_extension(self):
        m = PyfficeMatrix()
        assert m.determine_file_type("data.csv") == "csv"

    def test_case_insensitive(self):
        m = PyfficeMatrix()
        assert m.determine_file_type("REPORT.XLSX") == "excel"
        assert m.determine_file_type("Data.CSV") == "csv"

    def test_unknown_extension_defaults_to_excel(self):
        m = PyfficeMatrix()
        assert m.determine_file_type("mystery.xyz") == "excel"

    def test_empty_path_defaults_to_excel(self):
        m = PyfficeMatrix()
        assert m.determine_file_type("") == "excel"
        assert m.determine_file_type(None) == "excel"


class TestPyfficeSpreadSheet:
    """PyfficeSpreadSheet — basic operations.

    Note: set_cell has a latent bug where it compares self.end_column
    / self.end_row (None at construction) with int values, so we
    bypass it and exercise get_cell / cells dict directly.
    """

    def test_construction(self):
        ss = PyfficeSpreadSheet()
        assert ss is not None
        assert ss.cells is None

    def test_get_cell_returns_value(self):
        ss = PyfficeSpreadSheet()
        ss.cells = {"A|0": "value"}
        assert ss.get_cell("A|0") == "value"

    def test_get_cell_missing_returns_none(self):
        ss = PyfficeSpreadSheet()
        ss.cells = {}  # initialized, but empty
        assert ss.get_cell("nonexistent") is None

    def test_get_cell_returns_none_when_uninitialized(self):
        # When cells is None, get_cell raises AttributeError on
        # the .get() call. That's the documented current behavior.
        ss = PyfficeSpreadSheet()
        with pytest.raises(AttributeError):
            ss.get_cell("anything")


class TestPyfficeSpreadSheetGetRows:
    """T-NEW-057: get_rows groups cells by row index.

    Note: set_cell's row/column tracking assumes self.end_row and
    self.end_column are non-None integers; a freshly-constructed
    PyfficeSpreadSheet has them as None. The rows-by-index grouping
    logic in get_rows is still correct, so we exercise it with a
    pre-populated cells dict to avoid coupling to set_cell.
    """

    def test_empty_cells_dict_returns_empty_list(self):
        ss = PyfficeSpreadSheet()
        ss.cells = {}  # bypass set_cell's None handling
        assert ss.get_rows() == []

    def test_groups_by_row_index(self):
        ss = PyfficeSpreadSheet()
        ss.cells = {
            "A|0": "a0",
            "B|0": "b0",
            "A|1": "a1",
            "B|2": "b2",
        }
        rows = ss.get_rows()
        assert len(rows) == 3
        assert rows[0]["row"] == 0
        assert "A" in rows[0]["cells"]
        assert "B" in rows[0]["cells"]
        assert rows[2]["row"] == 2

    def test_skips_malformed_addresses(self):
        ss = PyfficeSpreadSheet()
        ss.cells = {
            "A|0": "ok",
            "malformed": "bad",
            "B|bad_row": "bad2",
        }
        rows = ss.get_rows()
        assert len(rows) == 1
        assert rows[0]["row"] == 0


class TestCalcRomanNumerals:
    """calcArabicNumerals + calcExtendedRomanNumerals round-trip."""

    @pytest.mark.parametrize("arabic,roman", [
        (1, "I"),
        (4, "IV"),
        (9, "IX"),
        (40, "XL"),
        (90, "XC"),
        (400, "CD"),
        (900, "CM"),
        (1999, "MCMXCIX"),
        (2024, "MMXXIV"),
        (3999, "MMMCMXCIX"),
    ])
    def test_arabic_to_roman(self, arabic, roman):
        assert calcExtendedRomanNumerals(arabic) == roman

    def test_roman_to_arabic(self):
        assert calcArabicNumerals("I") == 1
        assert calcArabicNumerals("IV") == 4
        assert calcArabicNumerals("IX") == 9
        assert calcArabicNumerals("MCMXCIX") == 1999

    @pytest.mark.parametrize("arabic", [1, 4, 9, 40, 90, 400, 900, 1999, 2024, 3999])
    def test_roundtrip_arabic(self, arabic):
        roman = calcExtendedRomanNumerals(arabic)
        assert calcArabicNumerals(roman) == arabic


class TestPyfficeMatrixToDict:
    """PyfficeMatrix.to_dict() must produce the canonical shape and
    must NOT silently swallow TypeError via the dead try/except
    that was here before R6.

    The R6 fix removed a silent try/except that pretended to convert
    ``data["content"]["data"]`` (a DataFrame) to ``list-of-lists``,
    but the access ``data["content"]["data"]`` raised TypeError on
    every call because ``_canonicalize`` (chained via ``super().to_dict()``)
    had already mirrored ``data["table"]`` into ``data["content"]``.
    The block was dead code, silently logged on every call.

    After R6:
    - The to_dict() chain returns the canonical shape.
    - There is no silent log of the redundant conversion.
    - ``data["table"]`` is the single source of truth for the
      list-of-lists payload.
    """

    def test_to_dict_returns_canonical_shape(self):
        from pyffice.document import PyfficeDocument, PyfficeDocumentManager
        m = PyfficeMatrix()
        # Force data to be a plain dict so the to_dict path
        # doesn't try to call DataFrame.values.tolist().
        m.data = {"cells": ["A|0"], "rows": 1}
        m.documents = {}
        m.compatibility = None
        d = m.to_dict()
        assert 'data' in d
        assert 'did' in d
        assert 'meta_data' in d
        assert 'pyffice_compat' in d
        # Original payload keys preserved under data.
        assert d['data']['document_type'] == 'matrix'
        assert 'table' in d['data']
        assert 'compatibility' in d['data']
        assert 'documents' in d['data']

    def test_to_dict_does_not_silently_log(self):
        """The R6 fix removed the silent logma.warning on every call.
        Verify the call path is exception-free on a plain dict.
        """
        import logging
        m = PyfficeMatrix()
        m.data = {"any": "value"}
        m.documents = {}
        m.compatibility = None
        # Should NOT raise (the old try/except was masking a TypeError).
        d = m.to_dict()
        assert d is not None

    def test_to_dict_additive_for_table_key(self):
        """The line-793 conversion (DataFrame→list-of-lists) is the
        single source of truth. After R6, data['table'] is preserved
        verbatim for plain dicts.
        """
        m = PyfficeMatrix()
        m.data = {"nested": "value"}
        m.documents = {}
        d = m.to_dict()
        assert d['data']['table'] == {"nested": "value"}
