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

# ======================================3rd Party Library Modules=====================================================||
import ffmpeg

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

from pyffice.audio.audio_export import PyfficeAudio
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from typing import Any
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "video.yaml")


class PyfficeVideo(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficeVideo.__init__ called")
        self.config = kahndor.Instruct(pxcfg).select("PyfficeVideo").override(cfg)
        self.has_audio = False
        self.audio = None

    def check_audio(self) -> Self:
        """Check audio.

        Returns:
            Self for chaining.
        """
        if self.audio is None:
            self.audio = PyfficeAudio()
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
        if keep:
            file_ = ffmpeg.input(self.path, start, end)
        else:
            start = 0
            end = start
            file_ = ffmpeg.input(self.path, start, end)

        if self.has_audio:
            self.audio.cut_section(start, end, keep)

        return self

    def find_pause(self) -> Any:
        """Find pause points in video."""
        # Placeholder - would analyze video for pauses
        return []

    def find_unpause(self) -> Any:
        """Find unpause points in video."""
        # Placeholder - would analyze video for resumes
        return []

    def get_duration(self) -> Any:
        """Get video duration."""
        return getattr(self, "duration", 0)

    def get_palette(self) -> Any:
        """Get color palette."""
        return getattr(self, "palette", [])

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "config" in content:
                setattr(self, "config", content["config"])
            if "has_audio" in content:
                setattr(self, "has_audio", content["has_audio"])
            if "audio" in content:
                setattr(self, "audio", content["audio"])
        return self

    def open_file(self, file_=None):
        import json as _json
        from os.path import exists
        if file_ is None:
            file_ = self.file_path
        if not file_ or not exists(file_):
            logma.warning(f"{self.__class__.__name__}.open_file: no such path {file_!r}")
            return self
        try:
            with open(file_, "r") as f:
                doc = _json.load(f)
        except (OSError, ValueError) as e:
            logma.warning(f"{self.__class__.__name__}.open_file failed for {file_!r}: {e}")
            return self
        return self.load_document(doc)

    def save(self, path=None, format_=None, encrypt=None):
        logma.debug(f"{self.__class__.__name__}.save called path={path!r}")
        super().save(path, format_, encrypt)
        if path is None:
            path = self.file_path
        if not path:
            logma.warning(f"{self.__class__.__name__}.save: no path available")
            return
        import json as _json
        doc = self.to_dict()
        with open(path, "w") as f:
            _json.dump(doc, f, indent=2, default=str)
        return

    def to_dict(self):
        # TODO implement method
        super().to_dict()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
