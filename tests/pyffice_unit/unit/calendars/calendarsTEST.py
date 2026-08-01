from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/calendars/.

Coverage:
- PyfficeCalendar construction, inheritance, SERIALIZATION_VERSION, setters
- PyfficeEvent construction, inheritance, SERIALIZATION_VERSION, setters

Inheritance map:
- PyfficeCalendar -> PyfficeDocumentManager -> PyfficeDocument -> PyfficeUnit
- PyfficeEvent    -> PyfficeUnit
"""

import pytest

from pyffice.calendars.calendars import PyfficeCalendar
from pyffice.calendars.events import PyfficeEvent
from pyffice.document import PyfficeDocument, PyfficeDocumentManager, PyfficeUnit


# --------------------------------------------------------------------------- #
# PyfficeCalendar
# --------------------------------------------------------------------------- #
class TestPyfficeCalendar:
    """PyfficeCalendar extends PyfficeDocumentManager."""

    def test_inherits_document_manager(self):
        logma.debug("TestPyfficeCalendar test class")
        assert issubclass(PyfficeCalendar, PyfficeDocumentManager)

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeCalendar, PyfficeDocument)

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeCalendar, PyfficeUnit)

    def test_constructs_no_args(self):
        cal = PyfficeCalendar()
        assert cal is not None

    def test_constructs_with_cfg(self):
        cal = PyfficeCalendar({"name": "team-cal"})
        assert cal is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficeCalendar, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeCalendar.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeCalendar.SERIALIZATION_VERSION) == 3

    def test_set_date_start_returns_self(self):
        cal = PyfficeCalendar()
        result = cal.set_date_start("2025-01-01")
        assert result is cal
        assert cal.start_date == "2025-01-01"

    def test_set_date_end_returns_self(self):
        cal = PyfficeCalendar()
        result = cal.set_date_end("2025-12-31")
        assert result is cal
        assert cal.end_date == "2025-12-31"


# --------------------------------------------------------------------------- #
# PyfficeEvent
# --------------------------------------------------------------------------- #
class TestPyfficeEvent:
    """PyfficeEvent extends PyfficeUnit."""

    def test_inherits_pyffice_unit(self):
        logma.debug("TestPyfficeEvent test class")
        assert issubclass(PyfficeEvent, PyfficeUnit)

    def test_constructs_no_args(self):
        e = PyfficeEvent()
        assert e is not None

    def test_constructs_with_cfg(self):
        e = PyfficeEvent({"event": "standup"})
        assert e is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficeEvent, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeEvent.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeEvent.SERIALIZATION_VERSION) == 3

    def test_set_event_returns_self(self):
        e = PyfficeEvent()
        result = e.set_event("retro")
        assert result is e
        assert e.event == "retro"

    def test_set_start_dttm_returns_self(self):
        e = PyfficeEvent()
        result = e.set_start_dttm("2025-06-01T09:00")
        assert result is e
        assert e.start_dttm == "2025-06-01T09:00"

    def test_set_end_dttm_returns_self(self):
        e = PyfficeEvent()
        result = e.set_end_dttm("2025-06-01T10:00")
        assert result is e
        assert e.end_dttm == "2025-06-01T10:00"
