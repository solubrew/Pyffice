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
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.ports.msports import PyfficePortExcel
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.items.text import PyfficeText
from pyffice.analytics.sources import PyfficeDataSet
# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "charts.yaml")


class PyfficeChart(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """
    A flexible general-purpose charting class for creating various charts using Seaborn and Matplotlib.
    """

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
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeChart")).override(cfg)
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

    def _merge_config(self, user_data, config_key, fields):
        """Merge user-supplied dict with defaults from config.

        Args:
            user_data: User-supplied dict (may be None).
            config_key: Key in self.config.dikt for defaults.
            fields: List of field names to merge.

        Returns:
            Merged dict.
        """
        defaults = self.config.dikt.get(config_key, {})
        user_data = user_data or {}
        return {f: user_data.get(f, defaults.get(f)) for f in fields}

    def add_axis(self, axis):
        """Add a axis.
        
        Args:
            axis: Parameter.
        
        Returns:
            Self for chaining.
        """
        axis = self._merge_config(axis, "axis", [
            "dimension", "title", "label", "position", "size",
            "orientation", "start", "step", "labels", "primary",
        ])
        self.axes.append(axis)
        return self

    def add_legend(self, legend):
        """Add a legend.
        
        Args:
            legend: Parameter.
        
        Returns:
            Self for chaining.
        """
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
        """Add a plotarea.
        
        Args:
            plotarea: Parameter.
        
        Returns:
            Self for chaining.
        """
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
        format_ = self._merge_config(format_, "series", [
            "marker", "markersize", "linestyle", "linewidth", "pattern",
            "fill", "fill_color", "marker_color", "line_color", "show_labels",
        ])
        if format_.get("marker") is None:
            format_["marker"] = "circle"
        if format_.get("markersize") is None:
            format_["markersize"] = 10
        if format_.get("linestyle") is None:
            format_["linestyle"] = "solid"
        if format_.get("linewidth") is None:
            format_["linewidth"] = 1
        if format_.get("fill") is None:
            format_["fill"] = True
        if format_.get("fill_color") is None:
            format_["fill_color"] = "blue"
        if format_.get("marker_color") is None:
            format_["marker_color"] = "blue"
        if format_.get("line_color") is None:
            format_["line_color"] = "blue"
        if format_.get("show_labels") is None:
            format_["show_labels"] = True
        self.series[label] = {"x": x_index, "y": y_index, "z": z_index, "format": format_}
        return self

    def del_axis(self, axis):
        """Remove the axis.
        
        Args:
            axis: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("axes", deepcopy(self.axes), axis)
        del self.axes[axis]
        return self

    def del_legend(self, legend):
        """Remove the legend.
        
        Args:
            legend: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("legends", deepcopy(self.legends), legend)
        del self.legends[legend]
        return self

    def del_plotarea(self, plotarea):
        """Remove the plotarea.
        
        Args:
            plotarea: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("plotareas", deepcopy(self.plotareas), plotarea)
        del self.plotareas[plotarea]
        return self

    def del_series(self, series):
        """Remove the series.
        
        Args:
            series: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.add_change("series", deepcopy(self.series), series)
        del self.series[series]
        return self

    def load_document(self, document=None):
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
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
        """Save the document.
        
        Args:
            path: Parameter.
            syntax: Parameter.
            encrypt_key: Parameter.
        
        Returns:
            Self for chaining.
        """
        if syntax is None:
            syntax = self.compatibility
        super().save(path, syntax, encrypt_key)
        if path is None:
            return self
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
        """Save the document.
        
        Args:
            path: Parameter.
        
        Returns:
            Self for chaining.
        """
        porter = PyfficePortExcel({"parent": self})
        porter.file_export(self, path)

    def save_html(self, path):
        """Save chart as HTML file."""
        import os
        # Placeholder - would use plotting library to generate HTML
        return self

    def save_latex(self, path):
        """Save chart as LaTeX file."""
        if not path:
            return self
        # Placeholder - would use plotting library to generate LaTeX
        return self

    def set_axes(self, axes):
        """Set chart axes."""
        self.axes = axes
        return self

    def set_background(self, color=None):
        """Set chart background."""
        self.background = color or "white"
        return self

    def set_chart_type(self, chart_type):
        """Set the chart type.
        
        Args:
            chart_type: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("type", chart_type)

    def set_compatibility(self, compatibility):
        """Set the compatibility.

        Args:
            compatibility: Parameter.

        Returns:
            Self for chaining.
        """
        return self._set_with_change("compatibility", compatibility)

    def set_data(self, data):
        """Set chart data."""
        self.data = data
        return self

    def set_figsize(self, figsize):
        """Set the figsize.
        
        Args:
            figsize: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("figsize", figsize)

    def set_label_xaxis(self, label):
        """Set the label xaxis.
        
        Args:
            label: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("xlabel", label)

    def set_label_yaxis(self, label):
        """Set the label yaxis.
        
        Args:
            label: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("ylabel", label)

    def set_legends(self, legends: list = None):
        """Set the legends.
        
        Args:
            legends: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("legends", legends)

    def set_orientation(self, orientation):
        """Set the orientation.
        
        Args:
            orientation: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("orientation", orientation)

    def set_origin(self, origin: list = None):
        """Set the origin.
        
        Args:
            origin: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("origin", origin)

    def set_plotareas(self, plotareas):
        """Set the plotareas.
        
        Args:
            plotareas: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("plotareas", plotareas)

    def set_position(self, position):
        """Set the position.
        
        Args:
            position: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("position", position)

    def set_position_plotarea(self, position, plotarea=None):
        """Set plot area position."""
        self.plotarea_position = position
        return self

    def set_position_legend(self, position, legend=None):
        """Set legend position."""
        self.legend_position = position
        return self

    def set_series(self, series: list = None):
        """Set the series.
        
        Args:
            series: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("series", series)

    def set_size(self, size):
        """Set the size.
        
        Args:
            size: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("size", size)

    def set_size_plotarea(self, size, plotarea):
        """Set plot area size."""
        self.plotarea_size = size
        return self

    def set_size_legend(self, size, legend):
        """Set legend size."""
        self.legend_size = size
        return self

    def set_theme(self, theme="whitegrid"):
        """Set the theme.
        
        Args:
            theme: Parameter.
        
        Returns:
            Self for chaining.
        """
        return self._set_with_change("theme", theme, label="style")

    def set_title(self, title, size: int = 12, color: str = "black"):
        """Set the title.
        
        Args:
            title: Parameter.
            size: Parameter.
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
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

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
