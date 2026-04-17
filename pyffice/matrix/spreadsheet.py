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
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||
from pycel.excelcompiler import ExcelCompiler
from pandas import read_csv, read_excel, DataFrame

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.ports.gports import PyfficePortGoogleSheets
from pyffice.ports.msports import PyfficePortExcel
from pyffice.ports.ports import PyfficePortCSV
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.items.cells import PyfficeCell
from pyffice.images.images import PyfficeImage
from pyffice.charts.charts import PyfficeChart
from pyffice.items.items import PyfficeTable
from pyffice.items.shapes import PyfficeShape
from pyffice.workflows.formulas import PyfficeFormulasLibrary
from thingery.numbers.numerals import calcExtendedRomanNumerals, calcArabicNumerals

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
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeSpreadSheet").override(cfg))
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
            self.add_change(
                "column_labels",
                self.column_labels[column],
                int(width),
                "assign",
                {"key": column},
            )
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
            "objects": {
                "tables": self.tables,
                "charts": self.charts,
                "images": self.images,
                "shapes": self.shapes,
            },
        }
        self.load_document(self.document["document"])
        return doc

    def _sanitize_sheet_name(self, name):
        """"""
        subs = ["[", "]", "/"]
        for sub in subs:
            if sub in name:
                name = name.replace(sub, "")
        return name


class PyfficeMatrix(PyfficeDocumentManager):
    """A Pyffice Matrix is a top level pyffice document type that can be included in a Pyffice Book"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeMatrix").override(cfg))
        self.active_worksheet = None
        self.charts = None
        self.compatibility = None
        self.file_path = None
        self.formula_library = None
        self.objects = None
        self.sheets = None

    def add_chart(self, chart):
        """"""
        cfg = {}
        chart = PyfficeChart(cfg)
        self.add_change("charts", self.charts, chart, "add")
        self.charts.append(chart)
        return self

    def add_object(self, object_type, data=None, cfg=None):
        """"""
        match object_type:
            case "shape":
                object_ = PyfficeShape(cfg)
            case "table":
                object_ = PyfficeTable(cfg)
            case "image":
                object_ = PyfficeImage(cfg)
        self.add_change("objects", self.objects, object_, "add")
        self.objects.append(object_)
        return self

    def add_charts(self, charts):
        """"""
        for chart in charts:
            self.add_chart(chart)
        return self

    def add_objects(self, objects):
        """"""
        for object_ in objects:
            self.add_object(object_["type"], object_["data"], object_["cfg"])
        return self

    def add_worksheet(self, name=None, cfg=None, tabn=None):
        """"""
        if tabn is None:
            tabn = len(self.sheets) + 1
        if name is None:
            name = f"wk{tabn}"
        cfg["name"] = name
        cfg["tab_int"] = tabn
        sheet = PyfficeSpreadSheet(cfg)
        self.active_worksheet = sheet
        self.add_change("sheets", self.sheets, sheet, "assign", {"key", name})
        self.sheets[name] = sheet
        return self

    def add_worksheets(self, sheets):
        """"""
        for sheet in sheets:
            self.add_worksheet(sheet["name"], sheet)
        return self

    def file_import(self, file_=None, if_data_only=False, read_only=False, keep_vba=False):
        """"""
        super().file_import()
        if file_ is None:
            file_ = self.file_path
        else:
            self.file_path = file_
        if file_ is None:
            raise Exception(f"No File Provided {file_}")
        if ".csv" == file_[-4:]:
            data = self.file_import_csv(file_, if_data_only=if_data_only, read_only=read_only, keep_vba=keep_vba)
        elif ".xlsx" == file_[-5:]:
            data = self.file_import_excel(file_, if_data_only=if_data_only, read_only=read_only, keep_vba=keep_vba)
        elif ".gsheet" == file_[-7:]:
            data = self.file_import_gsheet(file_, if_data_only=if_data_only, read_only=read_only, keep_vba=keep_vba)
        else:
            raise Exception(f"File Type Unknown {file_}")
        name = file_.split("/")[-1].split(".")[0]
        cfg = {
            "name": name,
            "parent": self,
            "file_format": self.file_format,
            "data": data,
        }
        self.add_worksheets(name, cfg)
        return self

    def file_import_csv(self, path, if_data_only=False, read_only=False, keep_vba=False):
        """"""
        self.file_format = ".csv"
        cfg = {}
        importer = PyfficePortCSV(cfg)
        data = importer.open_file(path, if_data_only, read_only, keep_vba)
        return data

    def file_import_excel(self, path, if_data_only=False, read_only=False, keep_vba=False):
        """"""
        self.file_format = ".xlsx"
        cfg = {}
        importer = PyfficePortExcel(cfg)
        data = importer.open_file(path, if_data_only, read_only, keep_vba)
        return data

    def file_import_gsheet(self, path, if_data_only=False, read_only=False, keep_vba=False):
        """"""
        self.file_format = ".gsheet"
        cfg = {}
        importer = PyfficePortGoogleSheets(cfg)
        data = importer.open_file(path, if_data_only, read_only, keep_vba)
        return data

    def load_document(self, document=None):
        """"""
        if document is None:
            document = {}
        super().load_document(document)
        self.file_path = self.config.dikt.get("file_path", None)
        self.executable_file = None
        self.set_formula_library()
        self.set_compatibility(self.config.dikt.get("compatibility", "nchantdmatrix"))
        return self

    def sanitize_sheet_name(self, sheet_name, compatibility="excel"):
        """
        Sanitizes the sheet name to conform to Excel's limitations.

        :param sheet_name: Name provided by the user
        :return: Sanitized name
        """
        if compatibility == "excel":
            invalid_chars = ["\\", "/", "*", "[", "]", ":", "?"]
            sanitized_name = "".join(c if c not in invalid_chars else "_" for c in sheet_name)
            return sanitized_name[:31]  # Excel sheet names are limited to 31 characters
        sanitized_name = sheet_name
        return sanitized_name

    def save(self, path=None, syntax=None, encrypt_key=None):
        """"""
        super().save(path, syntax, encrypt_key)
        match syntax:
            case "excel":
                self.save_excel(path)
            case "csv":
                self.save_csv(path)
            case "gsheet":
                self.save_gsheet(path)
        return self

    def save_csv(self, path):
        """"""

    def save_excel(self, path):
        """"""
        porter = PyfficePortExcel({"parent": self})
        porter.file_export(self, path)

    def save_gsheet(self, path):
        """"""
        return self

    def set_charts(self, charts):
        """"""
        return self

    def set_formula_library(self, library=None):
        """"""
        self.formulas_library = PyfficeFormulasLibrary(library)
        return self

    def set_objects(self, objects):
        """"""
        return self

    def set_porter(self, porter):
        """"""
        cfg = {}
        porter = PyfficePortExcel(cfg)
        if porter != self.porter:
            self.add_change("porter", self.porter, porter)
            self.porter = porter
        return self

    def set_sheets(self, sheets):
        """"""
        for sheet in sheets.get("sheets", []):
            self.sheets[sheet["name"]] = PyfficeSpreadSheet(sheet)
        return self

    def save(self, format_=None):
        """"""
        super().save()
        if format_ == "excel":
            self.export_excel()
            # self.wb.save(filename=self.path)
        elif format_ == "csv":
            self.export_csv()
        elif format_ == "gsheet":
            self.export_gsheet()

    def save_as(self, name, path):
        """"""
        super().save_as(path)
        return self

    def save_copy_as(self, name, path=None):
        """"""
        super().save_copy_as(name, path)
        return self

    def set_compatibility(self, compatibility):
        """"""
        self.compatibility = compatibility
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        if "document" not in doc:  # TODO: this may need to come from some other place
            doc["document"] = {}
        doc["document"]["compatibility"] = self.compatibility
        doc["document"]["documents"] = self.sheets
        doc["document"]["document_type"] = "pyffice_matrix"
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
