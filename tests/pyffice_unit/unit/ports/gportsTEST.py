from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/ports/gports.py — Google Workspace ports.

T-NEW-070: Tests the 4 Google Workspace ports (Sheets, Docs, Slides,
Forms) that were built out from empty stubs.

All tests verify construction, inheritance, auth surface, and
graceful-dep behavior. Real API calls are not tested — the optional
deps (google-auth, google-api-python-client) are not installed in
this env, so all operation tests verify the RuntimeError guard.
"""

import pytest

from pyffice.ports.gports import (
    PyfficePortGoogleSheets,
    PyfficePortGoogleDocs,
    PyfficePortGoogleSlides,
    PyfficePortGoogleForms,
    HAS_GOOGLE,
)
from pyffice.ports.cloud_ports import PyfficeCloudPort
from pyffice.ports.ports import PyfficePort


# ============================================================================================#
#  GOOGLE SHEETS
# ============================================================================================#

class TestPyfficePortGoogleSheets:
    def test_constructs(self):
        logma.debug("TestPyfficePortGoogleSheets test class")
        s = PyfficePortGoogleSheets()
        assert s is not None
        assert s.authenticated is False

    def test_inherits_cloud_port(self):
        assert issubclass(PyfficePortGoogleSheets, PyfficeCloudPort)

    def test_api_config(self):
        assert PyfficePortGoogleSheets.API_NAME == "sheets"
        assert PyfficePortGoogleSheets.API_VERSION == "v4"
        assert "spreadsheets" in PyfficePortGoogleSheets.SCOPES[0]

    def test_serialization_version(self):
        assert isinstance(PyfficePortGoogleSheets.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePortGoogleSheets.SERIALIZATION_VERSION) == 3

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_authenticate_raises_without_deps(self):
        s = PyfficePortGoogleSheets()
        with pytest.raises(ImportError, match="google-auth"):
            s.authenticate({"access_token": "test"})

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_read_range_raises_not_authenticated(self):
        s = PyfficePortGoogleSheets()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            s.read_range("id", "A1:A10")

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_write_range_raises_not_authenticated(self):
        s = PyfficePortGoogleSheets()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            s.write_range("id", "A1", [["v"]])

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_create_spreadsheet_raises_not_authenticated(self):
        s = PyfficePortGoogleSheets()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            s.create_spreadsheet("test")


# ============================================================================================#
#  GOOGLE DOCS
# ============================================================================================#

class TestPyfficePortGoogleDocs:
    def test_constructs(self):
        logma.debug("TestPyfficePortGoogleDocs test class")
        d = PyfficePortGoogleDocs()
        assert d is not None

    def test_inherits_cloud_port(self):
        assert issubclass(PyfficePortGoogleDocs, PyfficeCloudPort)

    def test_api_config(self):
        assert PyfficePortGoogleDocs.API_NAME == "docs"
        assert PyfficePortGoogleDocs.API_VERSION == "v1"
        assert "documents" in PyfficePortGoogleDocs.SCOPES[0]

    def test_serialization_version(self):
        assert isinstance(PyfficePortGoogleDocs.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePortGoogleDocs.SERIALIZATION_VERSION) == 3

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_authenticate_raises_without_deps(self):
        d = PyfficePortGoogleDocs()
        with pytest.raises(ImportError, match="google-auth"):
            d.authenticate({"access_token": "test"})

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_get_document_raises_not_authenticated(self):
        d = PyfficePortGoogleDocs()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            d.get_document("id")

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_insert_text_raises_not_authenticated(self):
        d = PyfficePortGoogleDocs()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            d.insert_text("id", "hello")

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_create_document_raises_not_authenticated(self):
        d = PyfficePortGoogleDocs()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            d.create_document("test")


# ============================================================================================#
#  GOOGLE SLIDES
# ============================================================================================#

class TestPyfficePortGoogleSlides:
    def test_constructs(self):
        logma.debug("TestPyfficePortGoogleSlides test class")
        s = PyfficePortGoogleSlides()
        assert s is not None

    def test_inherits_cloud_port(self):
        assert issubclass(PyfficePortGoogleSlides, PyfficeCloudPort)

    def test_api_config(self):
        assert PyfficePortGoogleSlides.API_NAME == "slides"
        assert PyfficePortGoogleSlides.API_VERSION == "v1"
        assert "presentations" in PyfficePortGoogleSlides.SCOPES[0]

    def test_serialization_version(self):
        assert isinstance(PyfficePortGoogleSlides.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePortGoogleSlides.SERIALIZATION_VERSION) == 3

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_authenticate_raises_without_deps(self):
        s = PyfficePortGoogleSlides()
        with pytest.raises(ImportError, match="google-auth"):
            s.authenticate({"access_token": "test"})

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_get_presentation_raises_not_authenticated(self):
        s = PyfficePortGoogleSlides()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            s.get_presentation("id")

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_create_presentation_raises_not_authenticated(self):
        s = PyfficePortGoogleSlides()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            s.create_presentation("test")


# ============================================================================================#
#  GOOGLE FORMS
# ============================================================================================#

class TestPyfficePortGoogleForms:
    def test_constructs(self):
        logma.debug("TestPyfficePortGoogleForms test class")
        f = PyfficePortGoogleForms()
        assert f is not None

    def test_inherits_cloud_port(self):
        assert issubclass(PyfficePortGoogleForms, PyfficeCloudPort)

    def test_api_config(self):
        assert PyfficePortGoogleForms.API_NAME == "forms"
        assert PyfficePortGoogleForms.API_VERSION == "v1"
        assert any("forms.body" in s for s in PyfficePortGoogleForms.SCOPES)

    def test_serialization_version(self):
        assert isinstance(PyfficePortGoogleForms.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePortGoogleForms.SERIALIZATION_VERSION) == 3

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_authenticate_raises_without_deps(self):
        f = PyfficePortGoogleForms()
        with pytest.raises(ImportError, match="google-auth"):
            f.authenticate({"access_token": "test"})

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_get_form_raises_not_authenticated(self):
        f = PyfficePortGoogleForms()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            f.get_form("id")

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_create_form_raises_not_authenticated(self):
        f = PyfficePortGoogleForms()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            f.create_form("test")

    @pytest.mark.skipif(HAS_GOOGLE, reason="deps installed")
    def test_list_responses_raises_not_authenticated(self):
        f = PyfficePortGoogleForms()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            f.list_responses("id")


# ============================================================================================#
#  LAZY EXPORT
# ============================================================================================#

class TestGoogleWorkspaceLazyExport:
    def test_sheets_importable_from_ports(self):
        from pyffice.ports import PyfficePortGoogleSheets as Imp
        assert Imp is PyfficePortGoogleSheets

    def test_docs_importable_from_ports(self):
        from pyffice.ports import PyfficePortGoogleDocs as Imp
        assert Imp is PyfficePortGoogleDocs

    def test_slides_importable_from_ports(self):
        from pyffice.ports import PyfficePortGoogleSlides as Imp
        assert Imp is PyfficePortGoogleSlides

    def test_forms_importable_from_ports(self):
        from pyffice.ports import PyfficePortGoogleForms as Imp
        assert Imp is PyfficePortGoogleForms
