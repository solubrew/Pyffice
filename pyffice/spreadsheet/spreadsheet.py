# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
__all__ = ["PyfficeSpreadSheet", "PyfficeMatrix", "calcArabicNumerals", "calcExtendedRomanNumerals"]

from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||
from pandas import read_csv, read_excel, DataFrame

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.items.cells import PyfficeCell

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "spreadsheet.yaml")


class PyfficeSpreadSheet(PyfficeDocument):
    """Pyffice SpreadSheet is a single page spreadsheet that can be included in a Pyffice Matrix to create a workbook"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeSpreadSheet").override(cfg))
        self.cells = None
        self.charts = None  # a Dictionary of Chart objects
        self.column_labels = None
        self.data = None  # a DataFrame table
        self.images = None
        self.num_cols = None
        self.num_rows = None
        self.start_column = None
        self.start_row = None
        self.end_column = None
        self.end_row = None
        self.shapes = None
        self.tables = None

    def add_cell(self, address, cfg):
        """"""
        if address in self.cells:
            self.set_cell(address, cfg["value"], cfg["format"], cfg["formula"])
        self.add_change("cells", None, cfg, "assign", {"address": address})
        self.cells[address] = PyfficeCell(cfg)
        return self

    def convert_column(self, column, syntax="arabic"):
        """"""
        if syntax == "arabic":
            column = calcArabicNumerals(column)
        elif syntax == "roman":
            column = calcExtendedRomanNumerals(column)
        else:
            raise Exception(f"Unknown Syntax {syntax}")
        return column

    def evaluate(self, address):
        """"""
        self.cells[address] = self.cells[address].evaluate()
        return self

    def get_cell(self, address):
        """"""
        return self.cells.get(address, None)

    def get_columns(self, count=None):
        """"""
        columns = []
        for column in range(1, count + 1):
            columns.append(self.convert_column(column))
        return columns

    def get_data(self, filters=None, return_format="table"):
        """return a dictionary or table of data"""
        data = self.data
        if return_format == "table":
            return data
        elif return_format == "dict":
            return self.cells
        else:
            raise Exception(f"Unknown Return Format {return_format}")

    def get_end_column(self, plus=0, minus=0):
        """"""
        end_column = self.convert_column(self.end_column, "arabic")
        return self.convert_column(end_column + plus - minus, "roman")

    def get_end_row(self, plus=0, minus=0):
        """"""
        return self.end_row + plus - minus

    def get_formula(self, address):
        """"""
        return self.cells[address].get_formula()

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.cells = {}
        self.set_name(document.get("name", None))
        self.set_data(document.get("data", None))
        self.set_size(document.get("size", None))
        return self

    def set_cell(self, address, value, format=None, formula=None):
        """"""
        if address not in self.cells:
            column = address.split("|")[0]
            if self.convert_column(column, "arabic") > self.end_column:
                self.end_column = self.convert_column(column, "arabic")
            row = address.split("|")[1]
            if int(row) > self.end_row:
                self.end_row = int(row)
            self.set_size([self.end_row, self.end_column])
        cfg = {"value": value, "format": format, "formula": formula}
        cell = PyfficeCell(cfg)
        if cell != self.cells.get(address, None):
            self.add_change("cells", cell, self.cells.get(address, None), "assign", address)
        self.cells[address] = cell
        return self

    def set_column_labels(self, labels=None, widths=None):
        """"""
        if widths is None:
            widths = {}
        if labels != self.column_labels:
            self.add_change("column_labels", self.column_labels, labels)
        self.column_labels = {x: widths.get(x, 30) for x in labels}
        return self

    def set_column_width(self, column, width):
        """"""
        if column not in self.column_labels:
            raise Exception(f"Column {column} not found")
        if int(width) != self.column_labels[column]:
            self.add_change("column_labels", self.column_labels[column], int(width), "assign", {"key": column})
        self.column_labels[column] = int(width)
        return self

    def set_data(self, data):
        """"""
        if data is None:
            data = {}
        row = 0
        rows = []
        data_ = []
        self.cells = data
        for address, value in data.items():
            if row != address.split("|")[1]:
                row = address.split("|")[1]
                if len(data) > 0 and len(rows) < len(data[0]):
                    rows += [None] * (len(data[0]) - len(rows))
                data_.append(rows)
                rows = [value]
            else:
                rows.append(value)
        self.data = DataFrame(data_, columns=self.get_columns())
        return self

    def set_objects(self, objects):
        """"""
        return self

    def set_row_labels(self, labels=None):
        """"""
        if labels != self.row_labels:
            self.add_change("row_labels", self.row_labels, labels)
        self.row_labels = labels
        return self

    def set_size(self, size):
        """"""
        if size is None:
            size = (50, 20)
        num_rows = size[0]
        num_cols = size[1]
        if self.data is not None and len(self.data) > 0:
            self.num_rows = len(self.data) if len(self.data) > num_rows else num_rows
            self.num_cols = len(self.data[0]) if len(self.data[0]) > num_cols else num_cols
            self.end_row = self.get_end_row(plus=self.num_rows)
            self.end_column = self.get_end_column(plus=self.num_cols)
        else:
            self.num_rows = num_rows
            self.num_cols = num_cols
            row = [None] * num_cols
            self.data = DataFrame([row] * num_rows, columns=self.get_columns(count=self.num_cols))
            self.end_row = self.get_end_row(plus=num_rows)
            self.end_column = self.get_end_column(plus=num_cols)
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"]["cells"] = {x: cell.to_dict() for x, cell in self.cells.items()}
        doc["document"]["objects"] = {
            "tables": [x.to_dict() for x in self.tables],
            "charts": [x.to_dict() for x in self.charts],
            "images": [x.to_dict() for x in self.images],
        }
        self.document["document"] = {
            "data": self.data,
            "objects": {"tables": self.tables, "charts": self.charts, "images": self.images, "shapes": self.shapes},
        }
        self.load_document(self.document["document"])
        return doc

    def to_json_schema(self) -> dict:
        """Convert the spreadsheet to JSON Schema format.

        Returns:
            dict: JSON Schema representation of the spreadsheet.
        """
        schema = super().to_json_schema()
        schema["title"] = self.name or "PyfficeSpreadSheet"
        schema["properties"].update(
            {
                "cells": {
                    "type": "object",
                    "description": "Dictionary of cell addresses to cell values",
                },
                "num_rows": {"type": "integer", "default": self.num_rows},
                "num_cols": {"type": "integer", "default": self.num_cols},
                "column_labels": {"type": "object", "description": "Column width settings"},
                "data": {"type": "object", "description": "Pandas DataFrame representation"},
            }
        )
        return schema

    def _sanitize_sheet_name(self, name):
        """"""
        subs = ["[", "]", "/"]
        for sub in subs:
            if sub in name:
                name = name.replace(sub, "")
        return name


def calcArabicNumerals(input_):
    """"""
    # Roman numeral to Arabic numeral mapping
    numerals = condor.Instruct(pxcfg).select("extended_roman_numerals").dikt
    numerals = dict(zip(numerals.values(), numerals.keys()))
    arabic_value = 0
    prev_value = 0
    # Loop through the Roman numerals in reverse order
    for char in reversed(input_):
        current_value = int(numerals[char])
        if current_value < prev_value:
            arabic_value -= current_value
        else:
            arabic_value += current_value
        prev_value = current_value
    return arabic_value


def calcExtendedRomanNumerals(input_):
    """Calculate the Extended Roman Numeral Symbol from Arabic Numeral"""
    numerals = condor.Instruct(pxcfg).select("extended_roman_numerals").dikt
    logma.info(f"Numerals: {numerals}")
    keys = [int(x) for x in numerals.keys()]
    keys.sort()
    ern = ""
    while input_ != 0:
        for val in reversed(keys):
            calc = input_ - val
            if calc < 0:
                continue
            input_ = calc
            ern += numerals[str(val)]
            break
    return ern


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
