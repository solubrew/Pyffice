"""Tests for pyffice/socials/."""

import pytest

from pyffice.socials.socials_messages import PyfficeSMS, PyfficeMMS, PyfficePostalMail
from pyffice.text.text_messages import PyfficeMessage


class TestPyfficeSMS:
    def test_constructs_with_no_args(self):
        s = PyfficeSMS()
        assert s is not None

    def test_inherits_pyffice_message(self):
        assert issubclass(PyfficeSMS, PyfficeMessage)


class TestPyfficeMMS:
    def test_constructs_with_no_args(self):
        m = PyfficeMMS()
        assert m is not None

    def test_inherits_pyffice_message(self):
        assert issubclass(PyfficeMMS, PyfficeMessage)


class TestPyfficePostalMail:
    def test_constructs_with_no_args(self):
        p = PyfficePostalMail()
        assert p is not None

    def test_inherits_pyffice_message(self):
        assert issubclass(PyfficePostalMail, PyfficeMessage)
