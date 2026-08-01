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
from os.path import dirname, join, exists
from typing import Any

# ======================================3rd Party Library Modules=====================================================||
from pandas import DataFrame

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.images.images import PyfficeImage
from pyffice.charts.charts import PyfficeChart
from pyffice.items.items import PyfficeTable
from pyffice.items.shapes import PyfficeShape
from pyffice.matrix import spreadsheet
from pyffice.workflows.formulas import PyfficeFormulasLibrary
from pyffice.ports.gports import PyfficePortGoogleSheets
from pyffice.ports.msports import PyfficePortExcel
from pyffice.ports.ports import PyfficePortCSV
from pyffice.document import PyfficeDocumentManager
from pyffice.matrix.spreadsheet import PyfficeSpreadSheet
from typing_extensions import Self


# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "matrix.yaml")


class PyfficeMatrix(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """A Pyffice Matrix is a top level pyffice document type that can be included in a Pyffice Book"""

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeMatrix").override(cfg))
        self.active_worksheet = None
        self.charts = []
        self.compatibility = None
        self.file_path = None
        self.formula_library = None
        self.objects = []
        self.sheets = {}

    def add_chart(self, chart) -> Self:
        """Add a chart.
        
        Args:
            chart: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {}
        chart = PyfficeChart(cfg)
        self.add_change("charts", self.charts, chart, "add")
        self.charts.append(chart)
        return self

    def add_object(self, object_type, data=None, cfg=None) -> Self:
        """Add a object.
        
        Args:
            object_type: Parameter.
            data: Parameter.
            cfg: Parameter.
        
        Returns:
            Self for chaining.
        """
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

    def add_charts(self, charts) -> Self:
        """Add a charts.
        
        Args:
            charts: Parameter.
        
        Returns:
            Self for chaining.
        """
        for chart in charts:
            self.add_chart(chart)
        return self

    def add_objects(self, objects) -> Self:
        """Add a objects.
        
        Args:
            objects: Parameter.
        
        Returns:
            Self for chaining.
        """
        for object_ in objects:
            self.add_object(object_["type"], object_["data"], object_["cfg"])
        return self

    def add_worksheet(self, name=None, cfg=None, tabn=None) -> Self:
        """Add a worksheet.
        
        Args:
            name: Parameter.
            cfg: Parameter.
            tabn: Parameter.
        
        Returns:
            Self for chaining.
        """
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

    def add_worksheets(self, sheets) -> Self:
        """Add a worksheets.
        
        Args:
            sheets: Parameter.
        
        Returns:
            Self for chaining.
        """
        for sheet in sheets:
            self.add_worksheet(sheet["name"], sheet)
        return self

    def determine_file_type(self, path) -> str:
        """Return the file type inferred from the path extension.

        Maps: .xlsx/.xls/.xlsm -> 'excel'; .ods -> 'openoffice';
        .csv -> 'csv'. Defaults to 'excel' for unknown extensions
        (backward compatibility with the prior placeholder return).
        """
        if not path:
            return "excel"
        lower = str(path).lower()
        if lower.endswith((".xlsx", ".xls", ".xlsm", ".xlsb")):
            return "excel"
        if lower.endswith(".ods"):
            return "openoffice"
        if lower.endswith(".csv"):
            return "csv"
        return "excel"

    def export(self, format_=None) -> None:
        """Export .
        
        Args:
            format_: Parameter.
        
        Returns:
            Self for chaining.
        """
        super().export()
        if format_ == "excel":
            self.export_excel()
            # self.wb.save(filename=self.path)
        elif format_ == "csv":
            self.export_csv()
        elif format_ == "gsheet":
            self.export_gsheet()

    def export_excel(self, format_=None) -> Self:
        """Export to Excel format."""
        if not self.data:
            return self
        # Placeholder - would use openpyxl
        return self

    def export_csv(self, format_=None) -> Self:
        """Export to CSV format."""
        if not self.data:
            return self
        # Placeholder - would use csv module
        return self

    def export_gsheet(self, format_=None) -> Self:
        """Export to Google Sheets."""
        if not self.data:
            return self
        # Placeholder - would use gspread
        return self

    def file_import(self, file_=None, if_data_only=False, read_only=False, keep_vba=False) -> Self:
        """File import.
        
        Args:
            file_: Parameter.
            if_data_only: Parameter.
            read_only: Parameter.
            keep_vba: Parameter.
        
        Returns:
            Self for chaining.
        """
        from pyffice.pyffice import (
            MissingPathError,
            UnknownFileTypeError,
        )
        file_type = ""
        super().file_import(file_type)
        if file_ is None:
            file_ = self.file_path
        else:
            self.file_path = file_
        if file_ is None:
            raise MissingPathError(f"No File Provided {file_}")
        if ".csv" == file_[-4:]:
            data = self.file_import_csv(file_, if_data_only=if_data_only, read_only=read_only, keep_vba=keep_vba)
        elif ".xlsx" == file_[-5:]:
            data = self.file_import_excel(file_, if_data_only=if_data_only, read_only=read_only, keep_vba=keep_vba)
        elif ".gsheet" == file_[-7:]:
            data = self.file_import_gsheet(file_, if_data_only=if_data_only, read_only=read_only, keep_vba=keep_vba)
        else:
            raise UnknownFileTypeError(f"File Type Unknown {file_}")
        name = file_.split("/")[-1].split(".")[0]
        cfg = {
            "name": name,
            "parent": self,
            "file_format": self.file_format,
            "data": data,
        }
        self.add_worksheets(name, cfg)
        return self

    def file_import_csv(self, path, if_data_only=False, read_only=False, keep_vba=False) -> None:
        """File import csv.
        
        Args:
            path: Parameter.
            if_data_only: Parameter.
            read_only: Parameter.
            keep_vba: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.file_format = ".csv"
        cfg = {}
        importer = PyfficePortCSV(cfg)
        data = importer.open_file(path, if_data_only, read_only, keep_vba)
        logma.info(f"Data {data}")
        return data

    def file_import_excel(self, path, if_data_only=False, read_only=False, keep_vba=False) -> None:
        """File import excel.
        
        Args:
            path: Parameter.
            if_data_only: Parameter.
            read_only: Parameter.
            keep_vba: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.file_format = ".xlsx"
        cfg = {}
        importer = PyfficePortExcel(cfg)
        data = importer.open_file(path, if_data_only, read_only, keep_vba)
        return data

    def file_import_gsheet(self, path, if_data_only=False, read_only=False, keep_vba=False) -> None:
        """File import gsheet.
        
        Args:
            path: Parameter.
            if_data_only: Parameter.
            read_only: Parameter.
            keep_vba: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.file_format = ".gsheet"
        cfg = {}
        importer = PyfficePortGoogleSheets(cfg)
        data = importer.open_file(path, if_data_only, read_only, keep_vba)
        return data

    def load_csv(self, file_path) -> None:
        """Load CSV file into spreadsheet"""
        import csv

        logma.info(f"Load CSV {file_path}")
        self.table.clearContents()
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row_idx, row in enumerate(reader):
                for col_idx, value in enumerate(row):
                    if col_idx >= self.table.columnCount():
                        self.table.insertColumn(col_idx)
                        self.table.setHorizontalHeaderItem(col_idx, pyqt.QTableWidgetItem(chr(65 + col_idx)))
                    item = pyqt.QTableWidgetItem(value)
                    self.table.setItem(row_idx, col_idx, item)
                if row_idx >= self.table.rowCount() - 1:
                    self.table.insertRow(row_idx + 1)

    def load_data(self, data) -> None:
        """Load data into the spreadsheet"""
        if isinstance(data, dict):
            # Load from cell dictionary
            for address, value in data.items():
                self.set_cell_value(address, value)
        elif isinstance(data, list):
            # Load from list (rows)
            for row_idx, row in enumerate(data):
                for col_idx, value in enumerate(row):
                    address = f"{chr(65 + col_idx)}{row_idx + 1}"
                    self.set_cell_value(address, value)

    def load_dataset(self, dataset_name) -> Self:
        """Load data from a named dataset into the table"""
        if self.app and hasattr(self.app, "model"):
            try:
                dataset = self.app.model.codex.get_dataset(dataset_name)
                if dataset and self.table:
                    # Clear existing data
                    self.table.clearContents()
                    # Load new data
                    if hasattr(dataset, "values"):
                        data = dataset.values
                    else:
                        data = dataset

                    for row_idx, row_data in enumerate(data):
                        if row_idx >= self.table.rowCount():
                            self.table.setRowCount(row_idx + 1)
                        for col_idx, cell_value in enumerate(row_data):
                            if col_idx >= self.table.columnCount():
                                self.table.setColumnCount(col_idx + 1)
                            item = pyqt.QTableWidgetItem(str(cell_value))
                            self.table.setItem(row_idx, col_idx, item)
            except (KeyError, ValueError, TypeError) as e:
                logma.error(f"Error loading dataset {dataset_name}: {e}")
        return self

    def load_document(self, document=None) -> Self:
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        if document is None:
            document = self.config.dikt.get("document", {}) or {}
        logma.json(document)
        super().load_document(document)
        logma.info(f"Load Pyffice Matrix")
        logma.info(document)
        self.file_path = self.config.dikt.get("file_path", None)
        self.executable_file = None
        self.set_formula_library()
        self.set_compatibility(self.config.dikt.get("compatibility", "nchantdmatrix"))
        try:
            self.set_data(self.config.get("data", {}).get("content", {}).get("data", None))
        except (KeyError, TypeError, AttributeError) as e:
            logma.warning(e)
            self.set_data(None)
        if self.documents == {}:
            cfg = {}
            _spreadsheet = PyfficeSpreadSheet(cfg)
            self.documents[_spreadsheet.did] = _spreadsheet
        return self

    def load_excel(self, file_path, sheet_name=None) -> None:
        """Load Excel file into spreadsheet with formula preservation

        Args:
            file_path: Path to the Excel file
            sheet_name: Optional specific sheet to load. If None, loads active sheet.
        """
        try:
            import openpyxl
            from openpyxl.utils import get_column_letter

            # Load workbook WITHOUT data_only to preserve formulas
            wb = openpyxl.load_workbook(file_path, data_only=False)

            # Select sheet
            if sheet_name and sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
            else:
                ws = wb.active

            self.table.clearContents()

            # Track workbook data for multi-sheet support
            self._excel_workbook = wb
            self._excel_sheets = list(wb.sheetnames)

            # Get dimensions
            max_row = ws.max_row or 100
            max_col = ws.max_column or 26

            # Ensure we have enough rows/columns
            self.table.setRowCount(max(max_row, 100))
            self.table.setColumnCount(max(max_col, 26))

            # Update column headers for columns beyond Z (AA, AB, etc.)
            for col_idx in range(26, max_col):
                self.table.setHorizontalHeaderItem(col_idx, pyqt.QTableWidgetItem(get_column_letter(col_idx + 1)))

            # Load cells with formulas preserved
            for row_idx, row in enumerate(ws.iter_rows()):
                for col_idx, cell in enumerate(row):
                    value = None

                    # Get formula or value - key for H1: preserve formulas!
                    if cell.data_type == "f":  # Formula cell
                        value = cell.value  # Returns the formula string
                    elif cell.value is not None:
                        value = cell.value

                    # Set cell value (formula or plain value)
                    if value is not None:
                        item = pyqt.QTableWidgetItem(str(value))

                        # Preserve number format
                        if cell.number_format and cell.number_format != "General":
                            item.setData(
                                pyqt.Qt.ItemDataRole.UserRole,
                                {
                                    "number_format": cell.number_format,
                                    "font_bold": cell.font.bold if cell.font else False,
                                    "font_italic": cell.font.italic if cell.font else False,
                                    "fill_color": cell.fill.fgColor.rgb if cell.fill and cell.fill.fgColor else None,
                                },
                            )

                        self.table.setItem(row_idx, col_idx, item)

                    # Preserve column widths
                    if col_idx < max_col:
                        col_dim = ws.column_dimensions.get(get_column_letter(col_idx + 1))
                        if col_dim and col_dim.width:
                            self.table.setColumnWidth(col_idx, int(col_dim.width * 7))

            # Update sheet tabs if in workbook mode
            if self.is_workbook and self.sheet_tabs:
                self._setup_sheet_tabs()

            self.current_sheet = ws.title

        except ImportError:
            pyqt.QMessageBox.warning(self, "Error", "openpyxl not installed. Please install: pip install openpyxl")
        except (OSError, KeyError, ValueError) as e:
            pyqt.QMessageBox.warning(self, "Error", f"Failed to load Excel: {e}")

    def load_from_config(self, cfg) -> None:
        """Load spreadsheet data from configuration"""
        if "data" in cfg:
            self.load_data(cfg["data"])
        if "sheets" in cfg:
            for sheet_name, sheet_data in cfg["sheets"].items():
                self.add_sheet(sheet_name, sheet_data)

    def load_from_file(self, file_path) -> None:
        """Load spreadsheet from file"""
        try:
            if file_path.endswith(".csv"):
                self.load_csv(file_path)
            elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
                self.load_excel(file_path)
            else:
                pyqt.QMessageBox.warning(self, "Error", "Unsupported file format")
        except (OSError, ValueError) as e:
            pyqt.QMessageBox.warning(self, "Error", f"Failed to load file: {e}")

    def open_file(self, file) -> None:
        """Open file.
        
        Args:
            file: Parameter.
        
        Returns:
            Self for chaining.
        """
        from pyffice.pyffice import UnknownFileTypeError
        if file is None:
            file = self.file_path
        self.set_syntax("file")
        if exists(file):
            self.set_file_path(file)
        file_type = self.determine_file_type(file)
        if file.endswith(".csv"):
            data = self.file_import_csv(file)
        elif file.endswith(".xlsx") or file.endswith(".xls"):
            data = self.file_import_excel(file)
        elif file.endswith(".gsheet"):
            data = self.file_import_gsheet(file)
        else:
            raise UnknownFileTypeError(f"Unknown File Type {file_type} for file {file}")
        self.data = data
        # super().file_open(path)

    def open_file_csv(self) -> Self:
        """Open a CSV file."""
        if not self.file_path:
            return self
        import csv
        # Placeholder - would read CSV
        return self

    def open_file_excel(self) -> Self:
        """Open an Excel file."""
        if not self.file_path:
            return self
        # Placeholder - would use openpyxl
        return self

    def sanitize_sheet_name(self, sheet_name, compatibility="excel") -> Any:
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

    def save(self, path=None, syntax=None, encrypt_key=None) -> Self:
        """Save the document.
        
        Args:
            path: Parameter.
            syntax: Parameter.
            encrypt_key: Parameter.
        
        Returns:
            Self for chaining.
        """
        super().save(path, syntax, encrypt_key)
        match syntax:
            case "excel":
                self.save_excel(path)
            case "csv":
                self.save_csv(path)
            case "gsheet":
                self.save_gsheet(path)
        # if i store always at the manager level then is that the right thing to do?
        return self

    def save_csv(self, path) -> Self:
        """Save as CSV file."""
        if not path:
            return self
        # Placeholder - would write CSV
        return self

    def save_excel(self, path) -> None:
        """Save as Excel file."""
        porter = PyfficePortExcel({"parent": self})
        porter.file_export(self, path)

    def save_gsheet(self, path) -> Self:
        """Save to Google Sheets."""
        if not path:
            return self
        # Placeholder - would use gspread
        return self

    def save_document(self, file_path=None) -> Self:
        """Save the current spreadsheet to a file"""
        if file_path is None:
            file_path = self.file_path

        if file_path is None:
            logma.warning("No file path specified for saving")
            return self

        # Determine file format from extension
        file_ext = file_path.split(".")[-1].lower()

        if file_ext in ["xlsx", "xls"]:
            self.save_as_excel(file_path)
        elif file_ext == "ods":
            self.save_as_ods(file_path)
        elif file_ext == "csv":
            self.save_as_csv(file_path)
        elif file_ext == "tsv":
            self.save_as_tsv(file_path)
        else:
            logma.warning(f"Unsupported file format: {file_ext}")

        return self

    def save_as_excel(self, file_path) -> Self:
        """Save as Excel file (.xlsx)"""
        try:
            if self.document:
                # Update document data from table
                self.document.data = self.extract_table_data()
                # Save using PyfficeMatrix
                self.document.file_path = file_path
                self.document.save_file()
            else:
                # Fallback: save using basic method
                import openpyxl

                wb = openpyxl.Workbook()
                ws = wb.active
                data = self.extract_table_data()
                for row_idx, row_data in enumerate(data, start=1):
                    for col_idx, cell_value in enumerate(row_data, start=1):
                        ws.cell(row=row_idx, column=col_idx, value=cell_value)
                wb.save(file_path)
            logma.info(f"Saved Excel file: {file_path}")
        except (OSError, AttributeError) as e:
            logma.error(f"Error saving Excel file: {e}")
        return self

    def save_as_ods(self, file_path) -> Self:
        """Save as OpenDocument Spreadsheet (.ods)"""
        try:
            if self.document:
                # Update document data from table
                self.document.data = self.extract_table_data()
                # Save using PyfficeMatrix
                self.document.file_path = file_path
                self.document.save_as_ods()
            else:
                logma.warning("ODS export requires PyfficeMatrix document")
        except (AttributeError, OSError) as e:
            logma.error(f"Error saving ODS file: {e}")
        return self

    def save_as_csv(self, file_path, delimiter=",") -> Self:
        """Save as CSV file"""
        try:
            import csv

            data = self.extract_table_data()
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=delimiter)
                writer.writerows(data)
            logma.info(f"Saved CSV file: {file_path}")
        except (OSError, ValueError) as e:
            logma.error(f"Error saving CSV file: {e}")
        return self

    def save_as_tsv(self, file_path) -> Any:
        """Save as TSV (Tab-Separated Values) file"""
        return self.save_as_csv(file_path, delimiter="\t")

    def save_file(self) -> None:
        """Save spreadsheet to file"""
        file_path, _ = pyqt.QFileDialog.getSaveFileName(
            self, "Save Spreadsheet", "", "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
        )

        if file_path:
            self.save_to_file(file_path)

    def set_charts(self, charts) -> Self:
        """Set chart objects."""
        self.charts = charts
        return self

    def set_formula_library(self, library=None) -> Self:
        """Set the formula library.
        
        Args:
            library: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.formulas_library = PyfficeFormulasLibrary(library)
        return self

    def set_objects(self, objects) -> Self:
        """Set objects."""
        self.objects = objects
        return self

    def set_porter(self, porter) -> Self:
        """Set the porter.
        
        Args:
            porter: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {}
        porter = PyfficePortExcel(cfg)
        if porter != self.porter:
            self.add_change("porter", self.porter, porter)
            self.porter = porter
        return self

    def set_sheets(self, sheets) -> Self:
        """Set the sheets.
        
        Args:
            sheets: Parameter.
        
        Returns:
            Self for chaining.
        """
        for sheet in sheets.get("sheets", []):
            self.sheets[sheet["name"]] = PyfficeSpreadSheet(sheet)
        return self

    def save_as(self, name, path) -> Self:
        """Save the document.
        
        Args:
            name: Parameter.
            path: Parameter.
        
        Returns:
            Self for chaining.
        """
        super().save_as(path)
        return self

    def save_copy_as(self, name, path=None) -> Self:
        """Save the document.
        
        Args:
            name: Parameter.
            path: Parameter.
        
        Returns:
            Self for chaining.
        """
        super().save_copy_as(name, path)
        return self

    def set_compatibility(self, compatibility) -> Self:
        """Set the compatibility.
        
        Args:
            compatibility: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.compatibility = compatibility
        return self

    def to_dict(self) -> Any:
        """Convert this document to dict.
        
        Returns:
            Self for chaining.
        """
        doc = super().to_dict()
        if isinstance(self.data, DataFrame):
            doc["data"]["table"] = self.data.values.tolist()
        else:
            doc["data"]["table"] = self.data
        doc["data"]["compatibility"] = self.compatibility
        doc["data"]["documents"] = {x: y.to_dict() for x, y in self.documents.items()}
        doc["data"]["document_type"] = "matrix"
        # The line below used to attempt a redundant DataFrame→list
        # conversion on `data["content"]["data"]`, but ``_canonicalize``
        # (called via ``super().to_dict()`` above) already mirrors
        # ``data["table"]`` into ``data["content"]`` — so the access
        # ``data["content"]["data"]`` raises TypeError on every call
        # (silently logged). The line-793 conversion above is the
        # single source of truth for table→list-of-lists.
        return self._canonicalize(doc)

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
                "active_worksheet": {
                    "type": "string",
                    "description": "Name of active worksheet",
                },
                "compatibility": {"type": "string", "default": self.compatibility},
                "charts": {
                    "type": "array",
                    "description": "List of charts in the workbook",
                },
                "objects": {
                    "type": "array",
                    "description": "List of objects (shapes, tables, images)",
                },
            }
        )
        return schema

    @classmethod
    def from_list(cls, data: list[list[Any]]) -> "PyfficeMatrix":
        """Create matrix from 2D list."""
        if not data:
            return cls()
        rows = len(data)
        cols = len(data[0]) if data[0] else 0
        matrix = cls(rows=rows, cols=cols)
        matrix._data = [[float(cell) if cell is not None else 0.0 for cell in row] for row in data]
        return matrix

    @classmethod
    def identity(cls, size: int) -> "PyfficeMatrix":
        """Create identity matrix."""
        matrix = cls(rows=size, cols=size)
        for i in range(size):
            matrix._data[i][i] = 1.0
        return matrix

    def get(self, row: int, col: int) -> float:
        """Get cell value."""
        return self._data[row][col]

    def set(self, row: int, col: int, value: float) -> None:
        """Set cell value."""
        self._data[row][col] = value

    def add(self, other: "PyfficeMatrix") -> "PyfficeMatrix":
        """Add two matrices."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match")
        result = PyfficeMatrix(rows=self.rows, cols=self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result._data[i][j] = self._data[i][j] + other._data[i][j]
        return result

    def multiply(self, other: "PyfficeMatrix") -> "PyfficeMatrix":
        """Multiply two matrices."""
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions incompatible for multiplication")
        result = PyfficeMatrix(rows=self.rows, cols=other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                total = 0.0
                for k in range(self.cols):
                    total += self._data[i][k] * other._data[k][j]
                result._data[i][j] = total
        return result

    def transpose(self) -> "PyfficeMatrix":
        """Return transpose of matrix."""
        result = PyfficeMatrix(rows=self.cols, cols=self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                result._data[j][i] = self._data[i][j]
        return result

    def to_list(self) -> list[list[float]]:
        """Return matrix as 2D list."""
        return [row[:] for row in self._data]


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
