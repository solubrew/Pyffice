"""Tests for pyffice/reports/."""

import pytest

from pyffice.reports.reports import PyfficeReport
from pyffice.script.script import PyfficeScript


class TestPyfficeReportConstruction:
    def test_constructs_with_no_args(self):
        r = PyfficeReport()
        assert r is not None

    def test_inherits_pyffice_script(self):
        assert issubclass(PyfficeReport, PyfficeScript)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeReport.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeReport.SERIALIZATION_VERSION) == 3
