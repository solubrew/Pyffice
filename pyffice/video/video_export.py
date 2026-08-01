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

    def __init__(self, cfg=None):
        """"""
        logma.debug(f"PyfficeVideo.__init__ called")
        self.config = kahndor.Instruct(pxcfg).select("PyfficeVideo").override(cfg)
        self.has_audio = False
        self.audio = None

    def check_audio(self):
        """Check audio.
        
        Returns:
            Self for chaining.
        """
        if self.audio is None:
            self.audio = PyfficeAudio()
        return self

    def cut_section(self, start, end, keep=False):
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

    def find_pause(self):
        """Find pause points in video."""
        # Placeholder - would analyze video for pauses
        return []

    def find_unpause(self):
        """Find unpause points in video."""
        # Placeholder - would analyze video for resumes
        return []

    def get_duration(self):
        """Get video duration."""
        return getattr(self, 'duration', 0)

    def get_palette(self):
        """Get color palette."""
        return getattr(self, 'palette', [])
# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
