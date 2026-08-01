from kahndor.logma import Logma
logma = Logma(__name__)
"""Tests for pyffice/audio/.

Coverage:
- PyfficeAudio construction (path, cfg)
- PyfficeAudio inheritance from PyfficeDocument
- SERIALIZATION_VERSION tuple
- get_duration, increase_volume, decrease_volume, find_pause, find_unpause
- convert_mp3_to_wave returns self (no ffmpeg path)
- PyfficePlayList construction (defaults, cfg)
- PyfficePlayList inheritance from PyfficeDocumentManager
"""

import pytest

from pyffice.audio.audio_export import PyfficeAudio, PyfficePlayList
from pyffice.document import PyfficeDocument, PyfficeDocumentManager


class TestPyfficeAudioConstruction:
    """PyfficeAudio(path) constructs and stores the path."""

    def test_constructs_with_path(self):
        a = PyfficeAudio("/tmp/test.mp3")
        assert a is not None
        assert a.path == "/tmp/test.mp3"

    def test_constructs_with_cfg(self):
        a = PyfficeAudio("/tmp/test.wav", {"format": "wav"})
        assert a is not None
        assert a.path == "/tmp/test.wav"


class TestPyfficeAudioInheritance:
    """PyfficeAudio extends PyfficeDocument."""

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeAudio, PyfficeDocument)


class TestPyfficeAudioVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_serialization_version_tuple(self):
        assert hasattr(PyfficeAudio, "SERIALIZATION_VERSION")
        assert isinstance(PyfficeAudio.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeAudio.SERIALIZATION_VERSION) == 3


class TestPyfficeAudioMethods:
    """Volume, duration, and pause-finding methods."""

    def test_get_duration_default_zero(self):
        logma.debug("TestPyfficeAudioMethods test class")
        a = PyfficeAudio("/tmp/x.mp3")
        assert a.get_duration() == 0

    def test_increase_volume_returns_self(self):
        a = PyfficeAudio("/tmp/x.mp3")
        assert a.increase_volume(20) is a
        assert a.volume == 100  # capped at 100 from default 100

    def test_decrease_volume_returns_self(self):
        a = PyfficeAudio("/tmp/x.mp3")
        a.increase_volume(10)  # 100 -> stays 100 (capped)
        assert a.decrease_volume(30) is a
        assert a.volume == 70

    def test_decrease_volume_floored_at_zero(self):
        a = PyfficeAudio("/tmp/x.mp3")
        a.decrease_volume(200)
        assert a.volume == 0

    def test_find_pause_returns_list(self):
        a = PyfficeAudio("/tmp/x.mp3")
        assert a.find_pause() == []

    def test_find_unpause_returns_list(self):
        a = PyfficeAudio("/tmp/x.mp3")
        assert a.find_unpause() == []

    def test_convert_mp3_to_wave_returns_self(self):
        a = PyfficeAudio("/tmp/x.mp3")
        # Without ffmpeg the method warns but still returns self
        assert a.convert_mp3_to_wave("/tmp/out.wav") is a


class TestPyfficePlayListConstruction:
    """PyfficePlayList() constructs with defaults."""

    def test_constructs_no_args(self):
        pl = PyfficePlayList()
        assert pl is not None

    def test_constructs_with_cfg(self):
        pl = PyfficePlayList({"name": "mix"})
        assert pl is not None


class TestPyfficePlayListInheritance:
    """PyfficePlayList extends PyfficeDocumentManager."""

    def test_inherits_document_manager(self):
        assert issubclass(PyfficePlayList, PyfficeDocumentManager)


class TestPyfficePlayListVersion:
    """SERIALIZATION_VERSION is a 3-tuple."""

    def test_serialization_version_tuple(self):
        assert hasattr(PyfficePlayList, "SERIALIZATION_VERSION")
        assert isinstance(PyfficePlayList.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePlayList.SERIALIZATION_VERSION) == 3
