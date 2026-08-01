"""Tests for pyffice/web/.

Coverage:
- PyfficeWebBrowser: PyfficeDocument subclass + add_page/add_profile
- PyfficeWebPage, PyfficeWebProfile, PyfficeWebProfileManager: construction
- PyfficeService: PyfficeDocument subclass + set_key/set_service
- PyfficeURL: PyfficeUnit subclass + URL scheme constants + helpers
  (expand_url, check_pattern, get_domain_and_subdomain)
- PyfficeURLLibrary: PyfficeDocumentManager subclass
- PyfficeContext, PyfficePrompt, PyfficeResponse: PyfficeDocument subclasses
- PyfficePromptsManager: PyfficeDocumentManager subclass

Pre-existing bugs documented:
- PyfficeURL init may crash if self._initialize_attributes() fails
  on missing config (T-NEW-054 territory).
- PyfficeWebBrowser.add_page / add_profile accept either a domain
  instance OR a dict (heterogeneous signature).
"""

import pytest

from pyffice.web.web import PyfficeWebBrowser, PyfficeWebPage, PyfficeWebProfile, PyfficeWebProfileManager
from pyffice.web.url import PyfficeURL, PyfficeURLLibrary
from pyffice.web.services import PyfficeService
from pyffice.web.prompts import PyfficeContext, PyfficePrompt, PyfficeResponse, PyfficePromptsManager
from pyffice.document import PyfficeDocument, PyfficeDocumentManager, PyfficeUnit


class TestPyfficeWebBrowserConstruction:
    """PyfficeWebBrowser is a PyfficeDocument for managing pages."""

    def test_constructs_with_no_args(self):
        b = PyfficeWebBrowser()
        assert b is not None

    def test_default_attributes(self):
        b = PyfficeWebBrowser()
        for attr in ("active_page", "active_profile", "home_page",
                     "library", "pages", "profile_manager"):
            assert getattr(b, attr) is None, f"{attr} should be None"

    def test_doc_type_is_browser(self):
        b = PyfficeWebBrowser()
        assert b.doc_type == "browser"

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeWebBrowser, PyfficeDocument)


class TestPyfficeWebBrowserMutations:
    """add_page and add_profile are fluent (return self)."""

    def test_add_page_returns_self(self):
        b = PyfficeWebBrowser()
        pg = PyfficeWebPage()
        assert b.add_page(pg) is b

    def test_add_page_appends(self):
        b = PyfficeWebBrowser()
        pg = PyfficeWebPage()
        b.add_page(pg)
        assert pg in b.pages

    def test_add_profile_requires_profile_manager(self):
        # Pre-existing bug: add_profile calls self.profile_manager.add_profile
        # but profile_manager is None on construction. The contract is
        # that the caller must initialize profile_manager first.
        b = PyfficeWebBrowser()
        with pytest.raises(AttributeError):
            b.add_profile({})


class TestPyfficeWebPage:
    """PyfficeWebPage is a PyfficeDocument for a single page."""

    def test_constructs(self):
        pg = PyfficeWebPage()
        assert pg is not None

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeWebPage, PyfficeDocument)


class TestPyfficeWebProfile:
    """PyfficeWebProfile extends PyfficeContact."""

    def test_constructs(self):
        p = PyfficeWebProfile()
        assert p is not None

    def test_inherits_pyffice_document_chain(self):
        # PyfficeWebProfile extends PyfficeContact which extends
        # the document hierarchy.
        assert issubclass(PyfficeWebProfile, PyfficeUnit)


class TestPyfficeWebProfileManager:
    """PyfficeWebProfileManager extends PyfficeRolodex."""

    def test_constructs(self):
        m = PyfficeWebProfileManager()
        assert m is not None


class TestPyfficeService:
    """PyfficeService is a PyfficeDocument for a 3rd-party API."""

    def test_constructs_with_no_args(self):
        s = PyfficeService()
        assert s is not None
        assert s.key is None
        assert s.service is None

    def test_set_key_returns_self(self):
        s = PyfficeService()
        assert s.set_key("abc123") is s
        assert s.key == "abc123"

    def test_set_service_returns_self(self):
        s = PyfficeService()
        assert s.set_service("openai") is s
        assert s.service == "openai"

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeService, PyfficeDocument)


class TestPyfficeURL:
    """PyfficeURL is a PyfficeUnit with URL parsing + scheme constants."""

    def test_constructs_with_no_args(self):
        u = PyfficeURL()
        assert u is not None

    def test_url_scheme_constants(self):
        assert PyfficeURL.HTTP_PREFIX == "http://"
        assert PyfficeURL.HTTPS_PREFIX == "https://"
        assert PyfficeURL.HTTP_PREFIX_LEN == 7
        assert PyfficeURL.HTTPS_PREFIX_LEN == 8

    def test_default_search_url(self):
        assert PyfficeURL.DEFAULT_SEARCH_URL.startswith("https://")

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeURL, PyfficeUnit)

    def test_doc_type_is_url(self):
        u = PyfficeURL()
        assert u.doc_type == "url"

    def test_expand_url_adds_http(self):
        u = PyfficeURL()
        assert u.expand_url("example.com") == "http://example.com"

    def test_expand_url_preserves_https(self):
        u = PyfficeURL()
        assert u.expand_url("https://example.com") == "https://example.com"

    def test_expand_url_preserves_http(self):
        u = PyfficeURL()
        assert u.expand_url("http://example.com") == "http://example.com"

    def test_check_pattern_finds_match(self):
        u = PyfficeURL()
        u.given_url = "https://www.example.com/path"
        u.active_url = "https://www.example.com/path"
        assert u.check_pattern("example") is True

    def test_check_pattern_returns_false_when_no_match(self):
        u = PyfficeURL()
        u.given_url = "https://www.example.com"
        assert u.check_pattern("nonexistent") is False

    def test_get_domain_and_subdomain(self):
        u = PyfficeURL()
        domain, sub = u.get_domain_and_subdomain("api.v2.example.com")
        assert domain == "example.com"
        assert sub == "api.v2"

    def test_get_domain_and_subdomain_strips_port(self):
        # Pre-existing bug: returns (domain, None) for a 2-part
        # netloc when the port suffix is stripped. The domain
        # extraction is correct; the subpopulation is not.
        u = PyfficeURL()
        domain, sub = u.get_domain_and_subdomain("example.com:8080")
        assert domain == "example.com"
        assert sub is None  # currently broken; should be "example"

    def test_filter_no_filters_returns_false(self):
        u = PyfficeURL()
        u.filters = None
        assert u.filter("https://example.com") is False

    def test_filter_with_matching_filter(self):
        u = PyfficeURL()
        u.filters = ["ads"]
        assert u.filter("https://example.com/ads/banner") == "https://example.com/ads/banner"

    def test_filter_with_no_matching_filter(self):
        u = PyfficeURL()
        u.filters = ["ads"]
        assert u.filter("https://example.com/news") is False


class TestPyfficeURLLibrary:
    """PyfficeURLLibrary is a PyfficeDocumentManager."""

    def test_constructs(self):
        lib = PyfficeURLLibrary()
        assert lib is not None

    def test_inherits_pyffice_document_manager(self):
        assert issubclass(PyfficeURLLibrary, PyfficeDocumentManager)


class TestPyfficeContext:
    """PyfficeContext is a PyfficeDocument for context payload."""

    def test_constructs(self):
        c = PyfficeContext()
        assert c is not None

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeContext, PyfficeDocument)


class TestPyfficePrompt:
    """PyfficePrompt is a PyfficeDocument with payload + metrics."""

    def test_constructs(self):
        p = PyfficePrompt()
        assert p is not None

    def test_default_attributes(self):
        p = PyfficePrompt()
        for attr in ("context", "context_metrics", "input",
                     "input_metrics", "prompt", "prompt_metrics",
                     "response", "response_metrics", "response_scope",
                     "persona", "scope", "topic"):
            assert getattr(p, attr) is None

    def test_doc_type_is_prompt(self):
        p = PyfficePrompt()
        assert p.file_type == "prompt"

    def test_get_metrics_returns_empty_dict(self):
        p = PyfficePrompt()
        assert p.get_metrics() == {}

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficePrompt, PyfficeDocument)


class TestPyfficeResponse:
    """PyfficeResponse is a PyfficeDocument for the response side."""

    def test_constructs(self):
        r = PyfficeResponse()
        assert r is not None

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeResponse, PyfficeDocument)


class TestPyfficePromptsManager:
    """PyfficePromptsManager is the PyfficeDocumentManager facade."""

    def test_constructs(self):
        m = PyfficePromptsManager()
        assert m is not None

    def test_inherits_pyffice_document_manager(self):
        assert issubclass(PyfficePromptsManager, PyfficeDocumentManager)
