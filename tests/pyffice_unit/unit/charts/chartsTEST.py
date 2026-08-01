from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/charts/.

Coverage:
- PyfficeChart construction, inheritance, SERIALIZATION_VERSION, setters

Inheritance map:
- PyfficeChart -> PyfficeDocument -> PyfficeUnit
"""

import pytest

from pyffice.charts.charts import PyfficeChart
from pyffice.document import PyfficeDocument, PyfficeUnit


# --------------------------------------------------------------------------- #
# PyfficeChart
# --------------------------------------------------------------------------- #
class TestPyfficeChart:
    """PyfficeChart extends PyfficeDocument."""

    def test_inherits_pyffice_document(self):
        logma.debug("TestPyfficeChart test class")
        assert issubclass(PyfficeChart, PyfficeDocument)

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeChart, PyfficeUnit)

    def test_constructs_no_args(self):
        c = PyfficeChart()
        assert c is not None

    def test_constructs_with_cfg(self):
        c = PyfficeChart({"title": "Sales"})
        assert c is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficeChart, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeChart.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeChart.SERIALIZATION_VERSION) == 3

    def test_set_title_returns_self(self):
        c = PyfficeChart()
        result = c.set_title("Revenue 2025")
        assert result is c

    def test_set_chart_type_returns_self(self):
        c = PyfficeChart()
        result = c.set_chart_type("bar")
        assert result is c

    def test_set_data_returns_self(self):
        c = PyfficeChart()
        result = c.set_data([1, 2, 3])
        assert result is c
        assert c.data == [1, 2, 3]

    def test_set_background_returns_self(self):
        c = PyfficeChart()
        result = c.set_background("black")
        assert result is c
        assert c.background == "black"

    def test_set_axes_returns_self(self):
        c = PyfficeChart()
        result = c.set_axes([])
        assert result is c
        assert c.axes == []

    def test_set_figsize_returns_self(self):
        c = PyfficeChart()
        result = c.set_figsize((12, 8))
        assert result is c

    def test_set_label_xaxis_returns_self(self):
        c = PyfficeChart()
        result = c.set_label_xaxis("Months")
        assert result is c

    def test_set_label_yaxis_returns_self(self):
        c = PyfficeChart()
        result = c.set_label_yaxis("Revenue")
        assert result is c
