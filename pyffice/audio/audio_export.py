# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from typing import Any
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ======================================3rd Party Library Modules=====================================================||
has_ffmpeg = False
try:
    import ffmpeg

    has_ffmpeg = True
except ImportError:
    logma.warning("FFMPEG not Available.")
# try:
#     import pydub
# except:
#     print("Pydub not Available.")

# ====================================================================================================================||
pxcfg = join(here, "_data_", "audio.yaml")


class PyfficeAudio(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, path, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeAudio")
        super().__init__()
        self.config.override(cfg)
        self.path = path
        # self.audio = pydub.AudioSegment.from_file(path)

    def load_document(self, document=None) -> Self:
        """"""
        super().load_document(document)
        # TODO implement method
        return self

    def open_file(self, file_=None):
        """"""
        super().open_file(file_)
        # TODO implement method
        return self

    def save(self, path=None, format_=None, encrypt=None):
        """"""
        super().save(path, format_, encrypt)
        # TODO implement method
        return self

    def to_dict(self):
        # TODO implement method
        super().to_dict()
        return self

    def add_fade(self, inn=False, out=False, in_duration=None, out_duration=None) -> Self:
        """Add a fade.

        Args:
            inn: Parameter.
            out: Parameter.
            in_duration: Parameter.
            out_duration: Parameter.

        Returns:
            Self for chaining.
        """
        if inn:
            if in_duration is None:
                in_duration = 2000
            self.audio = self.audio.fade_in(in_duration)
        if out:
            if out_duration is None:
                out_duration = 2000
            self.audio = self.audio.fade_out(out_duration)
        return self

    def convert_mp3_to_wave(self, new_path) -> Self:
        """Convert mp3 to wave.

        Args:
            new_path: Parameter.

        Returns:
            Self for chaining.
        """
        if not has_ffmpeg:
            logma.warning(f"MP3 Not Supported without FFMPEG.")
        return self

    def convert_wav_to_mp3(self, new_path) -> Self:
        """Convert wav to mp3.

        Args:
            new_path: Parameter.

        Returns:
            Self for chaining.
        """
        if not has_ffmpeg:
            logma.warning(f"MP3 Not Supported without FFMPEG.")
        self.audio.export(new_path, format="mp3")
        return self

    def cut_section(self, start, end, keep=False) -> Self:
        """Cut section.

        Args:
            start: Parameter.
            end: Parameter.
            keep: Parameter.

        Returns:
            Self for chaining.
        """
        trimmed_audio = self.audio[start:end]
        trimmed_audio.export(self.path, format="mp3")
        return self

    def find_pause(self) -> Any:
        """Find pause points in audio."""
        return []

    def find_unpause(self) -> Any:
        """Find unpause points in audio."""
        return []

    def get_duration(self) -> Any:
        """Get audio duration."""
        return getattr(self, "duration", 0)

    def increase_volume(self, percent) -> Self:
        """Increase volume by percent."""
        current = getattr(self, "volume", 100)
        self.volume = min(100, current + percent)
        return self

    def decrease_volume(self, percent) -> Self:
        """Decrease volume by percent."""
        current = getattr(self, "volume", 100)
        self.volume = max(0, current - percent)
        return self


class PyfficePlayList(PyfficeDocumentManager):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).override("")
        super().__init__(self)
        self.config.override(cfg)

    def load_document(self, document=None) -> Self:
        """"""
        super().load_document(document)
        # TODO implement method
        return self

    def open_file(self, file_=None):
        """"""
        super().open_file(file_)
        # TODO implement method
        return self

    def save(self, path=None, format_=None, encrypt=None):
        """"""
        super().save(path, format_, encrypt)
        # TODO implement method
        return self

    def to_dict(self):
        # TODO implement method
        super().to_dict()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
