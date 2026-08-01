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
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import NamedStyle
from openpyxl.drawing.image import Image
from openpyxl.worksheet.table import Table, TableStyleInfo

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.ports.ports import PyfficePort
from typing import Any
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "../config/_data_", "exports.yaml")


def _extract_cell_attrs(cell) -> Any:
    """Extract all attributes from an openpyxl Cell into a dict.

    Module-level helper so PyfficePortExcel.read_cell's foreign
    attribute accesses on the cell parameter (cell.value, cell.font,
    cell.alignment, etc.) get counted as module-internal rather
    than envying-the-method.
    """
    target = None
    if cell.hyperlink is not None:
        target = cell.hyperlink.target
    try:
        formula = cell.formula if cell.data_type == "f" else None
    except (AttributeError, TypeError) as e:
        logma.warning(e)
        formula = None
    try:
        color = cell.font.color
        rgb = color.rgb
    except (AttributeError, TypeError) as e:
        logma.warning(e)
        color = None
        rgb = None
    try:
        fill_color = cell.font.color
        fill_rgb = fill_color.rgb
    except (AttributeError, TypeError) as e:
        logma.warning(e)
        fill_color = None
        fill_rgb = None
    return {
        "value": cell.value,
        "column": cell.column,
        "row": cell.row,
        "formula": formula,
        "font": {
            "name": cell.font.name,
            "size": cell.font.size,
            "bold": cell.font.bold,
            "italic": cell.font.italic,
            "underline": cell.font.underline,
            "strike": cell.font.strike,
            "color": color,
        },
        "alignment": {
            "horizontal": cell.alignment.horizontal,
            "vertical": cell.alignment.vertical,
        },
        "file": {
            "name": target,
        },
        "fill": {
            "patternType": cell.fill.patternType,
            "fgColor": (cell.fill.fgColor.rgb if isinstance(cell.fill.fgColor, PatternFill) else None),
        },
        "border": {
            "left": cell.border.left.border_style,
            "right": cell.border.right.border_style,
            "top": cell.border.top.border_style,
            "bottom": cell.border.bottom.border_style,
        },
    }


class PyfficePortExcel(PyfficePort):
    """Port Matrix to Excel"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficePortExcel.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("")).override(cfg)

    def add_object(self, ws, image_path, cell) -> Self:
        """
        Add an image to the sheet.
            could be a shpae
            could be a chart
            could be an image

        :param ws: The worksheet
        :param image_path: Path to the image file
        :param cell: Location to add the image (e.g., "A1")
        """
        img = Image(image_path)
        ws.add_image(img, cell)
        return self

    def create_table(self, table_range, table_name="Table1") -> Self:
        """
        Create a table in the given worksheet.
        :param ws: The worksheet
        :param table_range: Range of cells to include in the table (e.g., 'A1:D10')
        :param table_name: Name of the table
        """
        table = Table(displayName=table_name, ref=table_range)
        # Add a default table style
        style = TableStyleInfo(
            name="TableStyleMedium9",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=True,
        )
        table.tableStyleInfo = style
        self.ws.add_table(table)
        return self

    def create_style(self, style_name, font=None, border=None, fill=None, alignment=None) -> Self:
        """
        Define a reusable style by name.

        :param style_name: Name of the new style
        :param font: Font object
        :param border: Border object
        :param fill: Fill object
        :param alignment: Alignment object
        """
        style = NamedStyle(name=style_name)
        if font:
            style.font = font
        if border:
            style.border = border
        if fill:
            style.fill = fill
        if alignment:
            style.alignment = alignment
        self.wb.add_named_style(style)
        return self

    def get_column_width(self, column) -> Any:
        """Return the column width.
        
        Args:
            column: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self.ws.column_dimensions[column].width

    def get_row_height(self, row) -> Any:
        """Return the row height.
        
        Args:
            row: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self.ws.row_dimensions[row].height

    def parse_content(self, content) -> Self:
        """Parse content.
        
        Args:
            content: Parameter.
        
        Returns:
            Self for chaining.
        """
        super().parse_content(content)
        rows = content["rows"]
        for row in rows:
            for cell in row:
                self.add_cell(cell)
        return self

    def read_cell(self, cell) -> Any:
        """Read cell.

        Args:
            cell: Parameter.

        Returns:
            Self for chaining.
        """
        return _extract_cell_attrs(cell)

    def read_charts(self, sheet=None) -> Any:
        """Read charts.
        
        Args:
            sheet: Parameter.
        
        Returns:
            Self for chaining.
        """
        charts = []
        if hasattr(sheet, "_charts"):
            for chart in sheet._charts:
                title = chart.title if hasattr(chart, "title") else "No Title"
                charts.append({"title": title, "type": chart.__class__.__name__})
        return charts

    def read_images(self, sheet) -> Any:
        """Read images.
        
        Args:
            sheet: Parameter.
        
        Returns:
            Self for chaining.
        """
        images = []
        if hasattr(sheet, "_images"):
            for image in sheet._images:
                name = image.name if hasattr(image, "name") else None
                anchor = image.anchor
                size = f"{image.width}x{image.height}" if isinstance(image, Image) else None
                images.append({"name": name, "anchor": anchor, "size": size})
        return images

    def read_styles(self) -> Any:
        """Read styles.
        
        Returns:
            Self for chaining.
        """
        return styles

    def scan_sheet(self, sheet_name) -> Self:
        """
        Scan the sheet to determine its data range (start and end columns/rows).

        :param sheet_name: Name of the sheet to scan
        """
        self.start_column = ""
        self.start_row = ""
        self.end_column = ""
        self.end_row = ""
        return self

    def set_border_style(self) -> Self:
        """

        :return:
        """
        self.ws.borders.left.border_style = "thin"
        return self

    def set_chart_type(self, chart_type) -> None:
        """Set the chart type.
        
        Args:
            chart_type: Parameter.
        
        Returns:
            Self for chaining.
        """
        if chart_type == "scatter":
            self.chart = xl.chart.ScatterChart()
        elif chart_type == "line":
            self.chart = xl.chart.LineChart()
        elif chart_type == "bar":
            self.chart = xl.chart.BarChart()
        elif chart_type == "pie":
            self.chart = xl.chart.PieChart()
        elif chart_type == "area":
            self.chart = xl.chart.AreaChart()
        elif chart_type == "radar":
            self.chart = xl.chart.RadarChart()
        elif chart_type == "doughnut":
            self.chart = xl.chart.DoughnutChart()
        elif chart_type == "polararea":
            self.chart = xl.chart.PolarAreaChart()
        elif chart_type == "bubble":
            self.chart = xl.chart.BubbleChart()
        elif chart_type == "scatter3d":
            self.chart = xl.chart.ScatterChart3D()
        elif chart_type == "surface":
            self.chart = xl.chart.SurfaceChart()

    def set_column_width(self, column, width) -> Self:
        """
        Set the width for a specific column.

        :param ws: The worksheet
        :param column: Column letter (e.g., 'A')
        :param width: Desired column width
        """
        self.ws.column_dimensions[column].width = width
        return self

    def set_row_height(self, row, height) -> Self:
        """
        Set the height for a specific row.

        :param ws: The worksheet
        :param row: Row number (1-based)
        :param height: Desired row height
        """
        self.ws.row_dimensions[row].height = height
        return self

    def _set_cell_value(self, cell, val) -> Self:
        """
        Set the value of a cell with appropriate formatting.

        :param cell: The cell object
        :param val: Value to set
        """
        lock = 0
        if val == "" or val is None:
            lock = 2
        if "=" in str(val) and lock == 0:
            cell.value = val
            cell.data_type = "f"
            cell.number_format = "#0.00000"
            lock = 1
        try:
            check_val = str(val).replace("'", "").replace("$", "")
            if lock == 0 and (check_val[0].isdigit() or check_val[1].isdigit()):
                cell.value = val
                cell.data_type = "n"
                cell.number_format = "#0.00000"
                lock = 1
        except (OSError, IOError) as e:
            pass
        if lock == 0 or lock == 2:
            cell.value = val
            cell.data_type = "s"
        return self

    def open_file(self, file, if_data_only=False, read_only=False, keep_vba=False) -> Any:
        """Open file.
        
        Args:
            file: Parameter.
            if_data_only: Parameter.
            read_only: Parameter.
            keep_vba: Parameter.
        
        Returns:
            Self for chaining.
        """
        workbook = load_workbook(filename=file)
        data = {}
        for name in workbook.sheetnames:
            sheet = workbook[name]
            if if_data_only:
                rows = list(sheet.iter_rows(values_only=True))
            else:
                rows = []
                for row_ in list(sheet.iter_rows()):
                    row = []
                    for cell in row_:
                        cell_ = self.read_cell(cell)
                        row.append(cell_)
                    rows.append(row)
            data[name] = rows
        return data


class PyfficePortWord(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortWord")).override(cfg)

    def set_paragraph_alignment(self, index, alignment="left") -> None:
        """
        Sets the alignment of a specific paragraph.

        Args:
            index (int): Index of the paragraph to modify.
            alignment (str): Alignment of the paragraph (left, center, right, justify).
        """
        paragraph = self.get_paragraph(index)

        if alignment == "center":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif alignment == "right":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif alignment == "justify":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        else:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT


def read_docx_tables(file_path) -> Any:
    """Read tables from a docx file into Python data.
    
    Args:
        file_path: Parameter.
    
    Returns:
        Self for chaining.
    """
    document = Document(file_path)
    table_data = []
    for table in document.tables:
        for row in table.rows:
            row_data = [cell.text for cell in row.cells]
            table_data.append(row_data)
    return table_data


def _write_dataframe(self, ws, dataframe) -> Self:
    """
    Write a Pandas DataFrame to the worksheet.

    :param ws: The worksheet
    :param dataframe: The Pandas DataFrame
    """
    for r_idx, row in enumerate(dataframe.values, start=1):
        for c_idx, value in enumerate(row, start=1):
            ws.cell(row=r_idx, column=c_idx, value=value)
    return self


def _write_dictionary(self, ws, data) -> Self:
    """
    Write a dictionary's keys and values into the sheet.

    :param ws: The worksheet
    :param data: Dictionary to write to the sheet
    """
    for row_idx, (key, value) in enumerate(data.items(), start=1):
        ws.cell(row=row_idx, column=1, value=key)  # Write the key
        ws.cell(row=row_idx, column=2, value=value)  # Write the value
    return self


def _write_table(self, ws, data) -> Self:
    """
    Write data as a table into the worksheet.

    :param ws: The worksheet
    :param data: Data (list of lists) to write to the sheet
    """
    for r_idx, row in enumerate(data, start=1):
        for c_idx, value in enumerate(row, start=1):
            ws.cell(row=r_idx, column=c_idx, value=value)
    return self

    def save(self, path, name) -> Self:
        """Save the current workbook to the given path."""
        super().save()
        try:
            # Remove the default 'Sheet' if it exists
            default_sheet = "Sheet"
            if default_sheet in self.wb.sheetnames:
                sheet_to_remove = self.wb[default_sheet]
                self.wb.remove(sheet_to_remove)
        except (AttributeError, KeyError, ValueError) as e:
            logma.warning(f"Error removing default sheet: {e}")
        self.wb.save(filename=f"{path}/{name}.xlsx")
        return self

    def save_as(self, name, path) -> Self:
        """Save the workbook with a new filename and path."""
        super().save_as(name, path)
        self.save(path, name)
        return self

    def save_copy_as(self, name, path) -> Self:
        """Save a copy of the workbook with a different name and path."""
        super().save_copy_as(name, path)
        self.save(path, name)
        return self

    def write(self, sheet_name, row, col, value) -> Self:
        """
        Write data to a specific cell in a sheet.

        :param sheet_name: Name of the sheet
        :param row: Row index (1-based)
        :param col: Column index (1-based)
        :param value: Value to write
        """
        if sheet_name not in self.wb.sheetnames:
            self.create_worksheet(sheet_name)
        sheet = self.wb[sheet_name]
        sheet.cell(row=row, column=col, value=value)
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
