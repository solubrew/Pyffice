from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/forms/forms.py.

Coverage:
- PyfficeForm construction (defaults, cfg dict)
- PyfficeForm inheritance (PyfficeDocument)
- PyfficeForm SERIALIZATION_VERSION tuple
- PyfficeForm fluent setters: set_form_id, set_sections,
  add_response, del_field, del_response, del_section
- PyfficeFormsManager construction + inheritance + SERIALIZATION_VERSION
- PyfficeFormsManager fluent setters: set_forms, load_document
- PyfficeSurvey construction + inheritance + SERIALIZATION_VERSION
"""

import pytest

from pyffice.forms.forms import (
    PyfficeForm,
    PyfficeFormsManager,
    PyfficeSurvey,
)
from pyffice.document import PyfficeDocument, PyfficeDocumentManager


class TestPyfficeFormConstruction:
    """PyfficeForm() constructs with default attributes."""

    def test_constructs_no_args(self):
        f = PyfficeForm()
        assert f is not None

    def test_constructs_with_cfg(self):
        f = PyfficeForm({"name": "form1"})
        assert f is not None

    def test_default_attributes(self):
        f = PyfficeForm()
        assert f.form_id is None
        assert f.description is None
        assert f.footer_image is None
        assert f.header_image is None
        assert f.sections is None
        assert f.responses is None


class TestPyfficeFormInheritance:
    """PyfficeForm subclasses PyfficeDocument."""

    def test_subclasses_document(self):
        assert issubclass(PyfficeForm, PyfficeDocument)


class TestPyfficeFormSerializationVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_is_tuple_of_len_3(self):
        assert isinstance(PyfficeForm.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeForm.SERIALIZATION_VERSION) == 3


class TestPyfficeFormSetters:
    """Fluent setters return self for chaining."""

    def test_set_form_id_returns_self(self):
        logma.debug("TestPyfficeFormSetters test class")
        f = PyfficeForm()
        assert f.set_form_id("abc123") is f
        assert f.form_id == "abc123"

    def test_set_sections_returns_self(self):
        f = PyfficeForm()
        assert f.set_sections({"s1": {}}) is f
        assert f.sections == {"s1": {}}

    def test_del_field_returns_self(self):
        f = PyfficeForm()
        # del_field uses getattr(self, 'fields', []) fallback
        assert f.del_field("nope") is f

    def test_del_response_raises_when_none(self):
        f = PyfficeForm()
        # responses defaults to None; del_response uses getattr fallback
        # but the attr IS set (to None), so `in None` raises TypeError.
        with pytest.raises(TypeError):
            f.del_response("nope")

    def test_del_response_works_after_init(self):
        f = PyfficeForm()
        f.responses = []  # initialize manually
        assert f.del_response("nope") is f

    def test_del_section_missing_returns_self(self):
        f = PyfficeForm()
        f.sections = {}  # initialize manually
        assert f.del_section("missing") is f

    def test_del_section_existing_returns_self(self):
        f = PyfficeForm()
        f.sections = {"s1": {"questions": []}}
        assert f.del_section("s1") is f
        assert "s1" not in f.sections


class TestPyfficeFormAddResponse:
    """add_response appends to self.responses."""

    def test_add_response_returns_self(self):
        f = PyfficeForm()
        f.responses = []  # initialize manually
        assert f.add_response("r1") is f
        assert f.responses == ["r1"]


class TestPyfficeFormsManagerConstruction:
    """PyfficeFormsManager() constructs with default attributes."""

    def test_constructs_no_args(self):
        m = PyfficeFormsManager()
        assert m is not None

    def test_constructs_with_cfg(self):
        m = PyfficeFormsManager({"name": "mgr"})
        assert m is not None

    def test_default_forms_none(self):
        m = PyfficeFormsManager()
        assert m.forms is None


class TestPyfficeFormsManagerInheritance:
    """PyfficeFormsManager subclasses PyfficeDocumentManager."""

    def test_subclasses_document_manager(self):
        assert issubclass(PyfficeFormsManager, PyfficeDocumentManager)


class TestPyfficeFormsManagerSerializationVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_is_tuple_of_len_3(self):
        assert isinstance(PyfficeFormsManager.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeFormsManager.SERIALIZATION_VERSION) == 3


class TestPyfficeFormsManagerSetters:
    """Fluent setters return self for chaining."""

    def test_set_forms_returns_self(self):
        m = PyfficeFormsManager()
        assert m.set_forms(["f1", "f2"]) is m
        assert m.forms == ["f1", "f2"]

    def test_set_forms_none_becomes_empty(self):
        m = PyfficeFormsManager()
        m.set_forms(None)
        assert m.forms == []

    def test_load_document_returns_self(self):
        m = PyfficeFormsManager()
        assert m.load_document({}) is m


class TestPyfficeSurveyConstruction:
    """PyfficeSurvey() constructs with default attributes."""

    def test_constructs_no_args(self):
        s = PyfficeSurvey()
        assert s is not None

    def test_constructs_with_cfg(self):
        s = PyfficeSurvey({"name": "survey1"})
        assert s is not None

    def test_default_attributes(self):
        s = PyfficeSurvey()
        assert s.distribution is None
        assert s.form is None
        assert s.form_id is None
        assert s.recipients is None
        assert s.responses is None
        assert s.schedule is None


class TestPyfficeSurveyInheritance:
    """PyfficeSurvey subclasses PyfficeDocument."""

    def test_subclasses_document(self):
        assert issubclass(PyfficeSurvey, PyfficeDocument)


class TestPyfficeSurveySerializationVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_is_tuple_of_len_3(self):
        assert isinstance(PyfficeSurvey.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeSurvey.SERIALIZATION_VERSION) == 3


class TestPyfficeSurveySetters:
    """Fluent setters return self for chaining."""

    def test_set_responses_returns_self(self):
        logma.debug("TestPyfficeSurveySetters test class")
        s = PyfficeSurvey()
        assert s.set_responses({"r": 1}) is s
        assert s.responses == {"r": 1}

    def test_set_schedule_returns_self(self):
        s = PyfficeSurvey()
        assert s.set_schedule({"start": "now"}) is s
        assert s.schedule == {"start": "now"}

    def test_del_recipient_raises_when_none(self):
        s = PyfficeSurvey()
        # recipients defaults to None; del_recipient uses getattr fallback
        # but the attr IS set (to None), so `in None` raises TypeError.
        with pytest.raises(TypeError):
            s.del_recipient("nope")

    def test_del_recipient_works_after_init(self):
        s = PyfficeSurvey()
        s.recipients = []  # initialize manually
        assert s.del_recipient("nope") is s

    def test_del_form_response_returns_self(self):
        s = PyfficeSurvey()
        assert s.del_form_response("rid") is s

    def test_del_field_response_returns_self(self):
        s = PyfficeSurvey()
        assert s.del_field_response("f", "fid", "rid") is s
