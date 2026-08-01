"""Tests for pyffice/video/."""

import pytest

from pyffice.video.video_export import PyfficeVideo
from pyffice.document import PyfficeDocument


class TestPyfficeVideoConstruction:
    def test_constructs_with_no_args(self):
        v = PyfficeVideo()
        assert v is not None

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeVideo, PyfficeDocument)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeVideo.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeVideo.SERIALIZATION_VERSION) == 3
