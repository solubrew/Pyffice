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

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pyffice.images.images import PyfficeImage
from pyffice.charts.charts import PyfficeChart
from pyffice.items.items import PyfficeTable
from pyffice.items.shapes import PyfficeShape
from pyffice.workflows.formulas import PyfficeFormulasLibrary
from pyffice.ports.gports import PyfficePortGoogleSheets
from pyffice.ports.msports import PyfficePortExcel
from pyffice.ports.ports import PyfficePortCSV
from pyffice.document import PyfficeDocumentManager
from pyffice.spreadsheet.spreadsheet import PyfficeSpreadSheet

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "matrix.yaml")


class PyfficeMatrix(PyfficeDocumentManager):
    """A Pyffice Matrix is a top level pyffice document type that can be included in a Pyffice Book"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeMatrix").override(cfg))
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
        cfg = {"name": name, "parent": self, "file_format": self.file_format, "data": data}
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
        doc["document"]["compatibility"] = self.compatibility
        doc["document"]["documents"] = self.sheets
        doc["document"]["document_type"] = "pyffice_matrix"
        return doc

    def to_json_schema(self) -> dict:
        """Convert the matrix (workbook) to JSON Schema format.

        Returns:
            dict: JSON Schema representation of the matrix.
        """
        schema = super().to_json_schema()
        schema["title"] = self.name or "PyfficeMatrix"
        schema["properties"].update(
            {
                "sheets": {
                    "type": "object",
                    "description": "Dictionary of sheet names to PyfficeSpreadSheet objects",
                },
                "active_worksheet": {"type": "string", "description": "Name of active worksheet"},
                "compatibility": {"type": "string", "default": self.compatibility},
                "charts": {"type": "array", "description": "List of charts in the workbook"},
                "objects": {"type": "array", "description": "List of objects (shapes, tables, images)"},
            }
        )
        return schema


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
