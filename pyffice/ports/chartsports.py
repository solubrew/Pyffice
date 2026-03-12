"""
Pyffice Charts Ports - External format converters for chart data.
"""
from pyffice.charts.charts import PyfficeChart
from pyffice.ports.ports import PyfficePort


class JSONChartPort(PyfficePort):
    """Port for JSON chart format."""

    def read(self, file_path: str) -> PyfficeChart:
        """Read JSON chart file and convert to PyfficeChart."""
        pass

    def write(self, chart: PyfficeChart, file_path: str) -> None:
        """Write PyfficeChart to JSON file."""
        pass


class SVGChartPort(PyfficePort):
    """Port for SVG chart format."""

    def read(self, file_path: str) -> PyfficeChart:
        """Read SVG chart file and convert to PyfficeChart."""
        pass

    def write(self, chart: PyfficeChart, file_path: str) -> None:
        """Write PyfficeChart to SVG file."""
        pass


class PNGChartPort(PyfficePort):
    """Port for PNG chart image format."""

    def read(self, file_path: str) -> PyfficeChart:
        """Read PNG chart file and convert to PyfficeChart."""
        pass

    def write(self, chart: PyfficeChart, file_path: str) -> None:
        """Write PyfficeChart to PNG file."""
        pass
