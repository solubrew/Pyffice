"""Tests for pyffice/email/.

Note: the `from pyffice.text.messages import PyfficeMessage` import
in email.py was a stale reference — fixed in this commit to
`pyffice.text.text_messages` (the actual module).
"""

import pytest

from pyffice.email.email import PyfficeEmailMessage, PyfficeMailBox
from pyffice.text.text_messages import PyfficeMessage
from pyffice.document import PyfficeDocumentManager


class TestPyfficeEmailMessage:
    def test_constructs_with_no_args(self):
        m = PyfficeEmailMessage()
        assert m is not None

    def test_inherits_pyffice_message(self):
        assert issubclass(PyfficeEmailMessage, PyfficeMessage)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeEmailMessage.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeEmailMessage.SERIALIZATION_VERSION) == 3


class TestPyfficeMailBox:
    def test_constructs_with_no_args(self):
        b = PyfficeMailBox()
        assert b is not None

    def test_inherits_pyffice_document_manager(self):
        assert issubclass(PyfficeMailBox, PyfficeDocumentManager)
