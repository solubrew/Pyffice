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

from copy import deepcopy

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pyffice.ports.msports import PyfficePortExcel
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.items.text import PyfficeText

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "charts.yaml")


class PyfficeChart(PyfficeDocument):
    """
    A flexible general-purpose charting class for creating various charts using Seaborn and Matplotlib.
    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """
        Initialize the chart with default configurations.

        Args:
            title (str): Title of the chart.
            xlabel (str): Label for the X-axis.
            ylabel (str): Label for the Y-axis.
            figsize (tuple): Size of the figure (width, height).
        """
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeChart")).override(cfg)
        self.axes = None
        self.background = None
        self.compatibility = None
        self.data = None  # Store the chart's data
        self.figsize = None
        self.legends = None
        self.origin = None
        self.orientation = None
        self.plotareas = None
        self.position = None
        self.porter = None
        self.series = None  # Stores individual series configurations
        self.size = None
        self.theme = None
        self.title = None
        self.type = None
        self.xlabel = None
        self.ylabel = None

    def add_axis(self, axis):
        """"""
        default_axis = self.config.dikt.get("axis", {})
        axis = {
            "dimension": axis.get("dimension", default_axis.get("dimension", None)),
            "title": axis.get("title", default_axis.get("title", None)),
            "label": axis.get("label", default_axis.get("label", None)),
            "position": axis.get("position", default_axis.get("position", None)),
            "size": axis.get("size", default_axis.get("size", None)),
            "orientation": axis.get("orientation", default_axis.get("orientation", None)),
            "start": axis.get("start", default_axis.get("start", None)),
            "step": axis.get("step", default_axis.get("step", None)),
            "labels": axis.get("labels", default_axis.get("labels", None)),
            "primary": axis.get("primary", default_axis.get("primary", None)),
        }
        self.axes.append(axis)
        return self

    def add_legend(self, legend):
        """"""
        default_legend = self.config.dikt.get("legend", {})
        legend = {
            "position": legend.get("position", default_legend.get("position", None)),
            "size": legend.get("size", default_legend.get("size", None)),
            "color": legend.get("color", default_legend.get("color", None)),
            "image": legend.get("image", default_legend.get("image", None)),
            "border": legend.get("border", default_legend.get("border", None)),
            "translucence": legend.get("translucence", default_legend.get("translucence", None)),
        }
        self.legends.append(legend)
        return self

    def add_plotarea(self, plotarea):
        """"""
        default_plotarea = self.config.dikt.get("plotarea", {})
        plotarea = {
            "position": plotarea.get("position", default_plotarea.get("position", None)),
            "size": plotarea.get("size", default_plotarea.get("size", None)),
            "background": plotarea.get("background", default_plotarea.get("background", None)),
            "axes": plotarea.get("axes", default_plotarea.get("axes", None)),
            "translucence": plotarea.get("translucence", default_plotarea.get("translucence", None)),
            "color": plotarea.get("color", default_plotarea.get("color", None)),
        }
        self.plotareas.append(plotarea)
        return self

    def add_series(self, label, x_index: list, y_index: list, z_index=None, format_=None):
        """
        Add a new series to the chart.

        Args:
            x (list): Data for the X-axis.
            y (list): Data for the Y-axis.
            label (str): Label for the legend.
            **kwargs: Additional keyword arguments for Seaborn or Matplotlib plots (e.g., color, linestyle).
        """
        default_series = self.config.dikt.get("series", {})
        self.series[label] = {"x": x_index, "y": y_index, "z": z_index, "format": {}}
        self.series[label]["format"] = {
            "marker": format_.get("marker", default_series.get("marker", "circle")),
            "markersize": format_.get("markersize", default_series.get("markersize", 10)),
            "linestyle": format_.get("linestyle", default_series.get("linestyle", "solid")),
            "linewidth": format_.get("linewidth", default_series.get("linewidth", 1)),
            "pattern": format_.get("pattern", default_series.get("pattern", None)),
            "fill": format_.get("fill", default_series.get("fill", True)),
            "fill_color": format_.get("fill_color", default_series.get("fill_color", "blue")),
            "marker_color": format_.get("marker_color", default_series.get("marker_color", "blue")),
            "line_color": format_.get("line_color", default_series.get("line_color", "blue")),
            "show_labels": format_.get("show_labels", default_series.get("show_labels", True)),
        }
        return self

    def del_axis(self, axis):
        """"""
        self.add_change("axes", deepcopy(self.axes), axis)
        del self.axes[axis]
        return self

    def del_legend(self, legend):
        """"""
        self.add_change("legends", deepcopy(self.legends), legend)
        del self.legends[legend]
        return self

    def del_plotarea(self, plotarea):
        """"""
        self.add_change("plotareas", deepcopy(self.plotareas), plotarea)
        del self.plotareas[plotarea]
        return self

    def del_series(self, series):
        """"""
        self.add_change("series", deepcopy(self.series), series)
        del self.series[series]
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_chart_type(document.get("type", None))
        self.set_data(document.get("data", None))  # Store the chart's data
        self.set_figsize(document.get("figsize", (10, 6)))  # Default figure size
        self.set_label_xaxis(document.get("xlabel", None))
        self.set_label_yaxis(document.get("ylabel", None))
        self.set_legends(document.get("legends", []))
        self.set_origin(document.get("origin", []))
        self.set_plotareas(document.get("plotareas", []))
        self.set_position(document.get("position", None))
        self.set_series(document.get("series", []))
        self.set_theme(document.get("theme", None))
        self.set_title(document.get("title", None))
        return self

    def save(self, path=None, syntax=None, encrypt_key=None):
        """"""
        if syntax is None:
            syntax = self.compatibility
        super().save(path, syntax, encrypt_key)
        match syntax:
            case "latex":
                self.save_latex(path)
            case "excel":
                self.save_excel(path)
            case "html":
                self.save_html(path)
            case _:
                self.save_pyffice(path, syntax, encrypt_key)
        return self

    def save_excel(self, path):
        """"""
        porter = PyfficePortExcel({"parent": self})
        porter.file_export(self, path)

    def save_html(self, path):
        """"""

    def save_latex(self, path):
        """"""

    def set_axes(self, axes):
        """"""
        return self

    def set_background(self):
        """"""
        return self

    def set_chart_type(self, chart_type):
        """"""
        if chart_type != self.type:
            self.add_change("type", self.type, chart_type)
            self.type = chart_type
        return self

    def set_compatibility(self, compatibility):
        """"""
        if compatibility != self.compatibility:
            self.add_change("compatibility", self.compatibility, compatibility)
            self.compatibility = compatibility
        return self

    def set_data(self, data):
        """"""
        return self

    def set_figsize(self, figsize):
        """"""
        if figsize != self.figsize:
            self.add_change("figsize", self.figsize, figsize)
            self.figsize = figsize
        return self

    def set_label_xaxis(self, label):
        """"""
        if label != self.xlabel:
            self.add_change("xlabel", self.xlabel, label)
            self.xlabel = label
        return self

    def set_label_yaxis(self, label):
        """"""
        if label != self.ylabel:
            self.add_change("ylabel", self.ylabel, label)
            self.ylabel = label
        return self

    def set_legends(self, legends: list = None):
        """"""
        if legends != self.legends:
            self.add_change("legends", self.legends, legends)
            self.legends = legends
        return self

    def set_orientation(self, orientation):
        """"""
        if orientation != self.orientation:
            self.add_change("orientation", self.orientation, orientation)
            self.orientation = orientation
        return self

    def set_origin(self, origin: list = None):
        """"""
        if origin != self.origin:
            self.add_change("origin", self.origin, origin)
            self.origin = origin
        return self

    def set_plotareas(self, plotareas):
        """"""
        if plotareas != self.plotareas:
            self.add_change("plotareas", self.plotareas, plotareas)
            self.plotareas = plotareas
        return self

    def set_position(self, position):
        """"""
        if position != self.position:
            self.add_change("position", self.position, position)
            self.position = position
        return self

    def set_position_plotarea(self, position, plotarea=None):
        """"""
        return self

    def set_position_legend(self, position, legend=None):
        """"""
        return self

    def set_series(self, series: list = None):
        """"""
        if series != self.series:
            self.add_change("series", self.series, series)
            self.series = series
        return self

    def set_size(self, size):
        """"""
        if size != self.size:
            self.add_change("size", self.size, size)
            self.size = size
        return self

    def set_size_plotarea(self, size, plotarea):
        """"""
        return self

    def set_size_legend(self, size, legend):
        """"""
        return self

    def set_theme(self, theme="whitegrid"):
        """"""
        if theme != self.theme:
            self.add_change("style", self.theme, theme)
            self.theme = theme
        return self

    def set_title(self, title, size: int = 12, color: str = "black"):
        """"""
        cfg = {
            "value": title,
            "alignment": {"horizontal": "center", "vertical": "center", "wrap": True},
            "font": {"color": color, "style": "sans-serif", "size": size, "bold": True},
        }
        title = PyfficeText(cfg)
        if title != self.title:
            self.add_change("title", self.title, title)
            self.title = title
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"]["title"] = self.title.to_dict()
        doc["document"]["axes"] = {"xlabel": self.xlabel, "ylabel": self.ylabel}
        doc["document"]["theme"] = self.theme
        doc["document"]["type"] = self.type
        doc["document"]["position"] = self.position
        doc["document"]["size"] = self.size
        doc["document"]["orientation"] = self.orientation
        doc["document"]["origin"] = self.origin
        doc["document"]["background"] = self.background
        doc["document"]["plotareas"] = self.plotareas
        doc["document"]["legends"] = self.legends
        doc["document"]["data"] = self.data.to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
