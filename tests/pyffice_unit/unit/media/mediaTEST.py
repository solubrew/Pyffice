"""Tests for pyffice/media/.

Coverage:
- MediaType enum: AUDIO/VIDEO/IMAGE/EMBEDDED values
- MediaError is an Exception subclass
- Media dataclass: construction + is_loaded + load (file/url) +
  unload + __post_init__ defaults metadata
- MediaProcessor: register_handler + process dispatch +
  extract_audio/extract_thumbnail happy + error paths
- PyfficeHeic / PyfficeRaw: stub construction
"""

import pytest

from pyffice.media.media import (
    MediaType,
    MediaError,
    Media,
    MediaProcessor,
)
from pyffice.media.heic import PyfficeHeic
from pyffice.media.raw import PyfficeRaw


class TestMediaType:
    """MediaType enum has the documented values."""

    def test_four_values(self):
        assert len(list(MediaType)) == 4

    def test_audio_value(self):
        assert MediaType.AUDIO.value == "audio"

    def test_video_value(self):
        assert MediaType.VIDEO.value == "video"

    def test_image_value(self):
        assert MediaType.IMAGE.value == "image"

    def test_embedded_value(self):
        assert MediaType.EMBEDDED.value == "embedded"


class TestMediaError:
    """MediaError subclasses Exception."""

    def test_subclasses_exception(self):
        assert issubclass(MediaError, Exception)

    def test_can_be_raised(self):
        with pytest.raises(MediaError, match="boom"):
            raise MediaError("boom")


class TestMediaConstruction:
    """Media dataclass + defaults."""

    def test_construction_sets_attributes(self):
        m = Media(media_type=MediaType.IMAGE, source="photo.jpg")
        assert m.media_type == MediaType.IMAGE
        assert m.source == "photo.jpg"
        assert m.data is None

    def test_metadata_defaults_to_empty_dict(self):
        m = Media(media_type=MediaType.AUDIO, source="audio.mp3")
        assert m.metadata == {}

    def test_is_loaded_false_when_data_none(self):
        m = Media(media_type=MediaType.AUDIO, source="x.mp3")
        assert m.is_loaded is False

    def test_is_loaded_true_when_data_set(self):
        m = Media(media_type=MediaType.AUDIO, source="x.mp3", data=b"abc")
        assert m.is_loaded is True


class TestMediaLoad:
    """Media.load reads from file source."""

    def test_load_from_file(self, tmp_path):
        f = tmp_path / "audio.mp3"
        f.write_bytes(b"fake mp3 data")
        m = Media(media_type=MediaType.AUDIO, source=str(f))
        data = m.load()
        assert data == b"fake mp3 data"
        assert m.is_loaded is True

    def test_load_returns_cached_data(self, tmp_path):
        f = tmp_path / "audio.mp3"
        f.write_bytes(b"on disk")
        m = Media(media_type=MediaType.AUDIO, source=str(f),
                  data=b"in memory")
        # Returns the cached data, doesn't touch disk.
        assert m.load() == b"in memory"

    def test_load_missing_file_raises(self, tmp_path):
        m = Media(media_type=MediaType.AUDIO, source=str(tmp_path / "nope.mp3"))
        with pytest.raises((FileNotFoundError, OSError)):
            m.load()

    def test_unload_clears_data(self, tmp_path):
        f = tmp_path / "audio.mp3"
        f.write_bytes(b"data")
        m = Media(media_type=MediaType.AUDIO, source=str(f))
        m.load()
        assert m.is_loaded is True
        m.unload()
        assert m.is_loaded is False


class TestMediaProcessorRegistration:
    """register_handler + process dispatch."""

    def test_constructs_with_empty_handlers(self):
        p = MediaProcessor()
        assert p._handlers == {}

    def test_register_handler(self):
        p = MediaProcessor()
        sentinel = lambda m, **opts: "result"
        p.register_handler(MediaType.AUDIO, sentinel)
        assert p._handlers[MediaType.AUDIO] is sentinel

    def test_process_dispatches_to_handler(self):
        p = MediaProcessor()
        p.register_handler(MediaType.IMAGE, lambda m, **opts: b"processed")
        m = Media(media_type=MediaType.IMAGE, source="x.jpg")
        assert p.process(m) == b"processed"

    def test_process_passes_options(self):
        p = MediaProcessor()
        captured = {}
        def handler(m, **opts):
            captured.update(opts)
            return "ok"
        p.register_handler(MediaType.VIDEO, handler)
        m = Media(media_type=MediaType.VIDEO, source="x.mp4")
        p.process(m, size=100, format="webm")
        assert captured == {"size": 100, "format": "webm"}

    def test_process_no_handler_raises(self):
        p = MediaProcessor()
        m = Media(media_type=MediaType.AUDIO, source="x.mp3")
        with pytest.raises(MediaError, match="No handler"):
            p.process(m)


class TestMediaProcessorExtracts:
    """extract_audio / extract_thumbnail happy + error paths."""

    def test_extract_audio_happy(self, tmp_path):
        f = tmp_path / "audio.mp3"
        f.write_bytes(b"audio bytes")
        p = MediaProcessor()
        m = Media(media_type=MediaType.AUDIO, source=str(f))
        assert p.extract_audio(m) == b"audio bytes"

    def test_extract_audio_wrong_type_raises(self):
        p = MediaProcessor()
        m = Media(media_type=MediaType.VIDEO, source="x.mp4")
        with pytest.raises(MediaError, match="Cannot extract audio"):
            p.extract_audio(m)

    def test_extract_thumbnail_happy(self, tmp_path):
        f = tmp_path / "thumb.jpg"
        f.write_bytes(b"thumb bytes")
        p = MediaProcessor()
        m = Media(media_type=MediaType.IMAGE, source=str(f))
        assert p.extract_thumbnail(m) == b"thumb bytes"

    def test_extract_thumbnail_default_size(self, tmp_path):
        # Default size is (128, 128).
        f = tmp_path / "thumb.jpg"
        f.write_bytes(b"thumb bytes")
        p = MediaProcessor()
        m = Media(media_type=MediaType.IMAGE, source=str(f))
        result = p.extract_thumbnail(m)  # default size
        assert result == b"thumb bytes"

    def test_extract_thumbnail_wrong_type_raises(self):
        p = MediaProcessor()
        m = Media(media_type=MediaType.AUDIO, source="x.mp3")
        with pytest.raises(MediaError, match="Cannot extract thumbnail"):
            p.extract_thumbnail(m)


class TestPyfficeHeic:
    """PyfficeHeic stub constructs."""

    def test_constructs(self):
        h = PyfficeHeic()
        assert h is not None


class TestPyfficeRaw:
    """PyfficeRaw stub constructs."""

    def test_constructs(self):
        r = PyfficeRaw()
        assert r is not None