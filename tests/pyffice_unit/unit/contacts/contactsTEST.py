from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/contacts/.

Coverage:
- PyfficeContact construction, inheritance, SERIALIZATION_VERSION, setters
- PyfficeRolodex construction, inheritance, SERIALIZATION_VERSION, setters
- PyfficePersona construction, inheritance, SERIALIZATION_VERSION, methods

Inheritance map:
- PyfficeContact -> PyfficeDocument -> PyfficeUnit
- PyfficeRolodex -> PyfficeDocumentManager -> PyfficeDocument -> PyfficeUnit
- PyfficePersona -> PyfficeDocument -> PyfficeUnit
"""

import pytest

from pyffice.contacts.contacts import PyfficeContact, PyfficeRolodex
from pyffice.contacts.persona import PyfficePersona
from pyffice.document import PyfficeDocument, PyfficeDocumentManager, PyfficeUnit


# --------------------------------------------------------------------------- #
# PyfficeContact
# --------------------------------------------------------------------------- #
class TestPyfficeContact:
    """PyfficeContact extends PyfficeDocument."""

    def test_inherits_pyffice_document(self):
        logma.debug("TestPyfficeContact test class")
        assert issubclass(PyfficeContact, PyfficeDocument)

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeContact, PyfficeUnit)

    def test_constructs_no_args(self):
        c = PyfficeContact()
        assert c is not None

    def test_constructs_with_cfg(self):
        c = PyfficeContact({"first_name": "Alice"})
        assert c is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficeContact, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeContact.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeContact.SERIALIZATION_VERSION) == 3

    def test_set_name_first_returns_self(self):
        c = PyfficeContact()
        result = c.set_name_first("Alice")
        assert result is c
        assert c.first_name == "Alice"

    def test_set_name_full_returns_self(self):
        c = PyfficeContact()
        result = c.set_name_full("Alice Wonderland")
        assert result is c
        assert c.full_name == "Alice Wonderland"

    def test_add_group_returns_self(self):
        c = PyfficeContact()
        result = c.add_group("VIP")
        assert result is c
        assert "VIP" in c.groups


# --------------------------------------------------------------------------- #
# PyfficeRolodex
# --------------------------------------------------------------------------- #
class TestPyfficeRolodex:
    """PyfficeRolodex extends PyfficeDocumentManager."""

    def test_inherits_document_manager(self):
        logma.debug("TestPyfficeRolodex test class")
        assert issubclass(PyfficeRolodex, PyfficeDocumentManager)

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeRolodex, PyfficeDocument)

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficeRolodex, PyfficeUnit)

    def test_constructs_no_args(self):
        r = PyfficeRolodex()
        assert r is not None

    def test_constructs_with_cfg(self):
        r = PyfficeRolodex({"default_group": "work"})
        assert r is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficeRolodex, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeRolodex.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeRolodex.SERIALIZATION_VERSION) == 3

    def test_add_group_returns_self(self):
        r = PyfficeRolodex()
        result = r.add_group("family")
        assert result is r
        assert "family" in r.groups

    def test_set_group_default_returns_self(self):
        r = PyfficeRolodex()
        result = r.set_group_default("colleagues")
        assert result is r
        assert r.default_group == "colleagues"


# --------------------------------------------------------------------------- #
# PyfficePersona
# --------------------------------------------------------------------------- #
class TestPyfficePersona:
    """PyfficePersona extends PyfficeDocument."""

    def test_inherits_pyffice_document(self):
        logma.debug("TestPyfficePersona test class")
        assert issubclass(PyfficePersona, PyfficeDocument)

    def test_inherits_pyffice_unit(self):
        assert issubclass(PyfficePersona, PyfficeUnit)

    def test_constructs_no_args(self):
        p = PyfficePersona()
        assert p is not None

    def test_constructs_with_cfg(self):
        p = PyfficePersona({"name": "buyer"})
        assert p is not None

    def test_serialization_version_is_tuple_len_3(self):
        assert hasattr(PyfficePersona, "SERIALIZATION_VERSION")
        assert isinstance(PyfficePersona.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePersona.SERIALIZATION_VERSION) == 3

    def test_calculate_myers_briggs_returns_str(self):
        p = PyfficePersona()
        result = p.calculate_myers_briggs(ei=0.8, ns=0.8, tf=0.8, pj=0.8)
        assert isinstance(result, str)
        assert len(result) == 4

    def test_calculate_myers_briggs_istj(self):
        p = PyfficePersona()
        result = p.calculate_myers_briggs(ei=0.6, ns=0.6, tf=0.6, pj=0.6)
        assert result == "ISFJ"
