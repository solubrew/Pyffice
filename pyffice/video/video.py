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

from pyffice.audio.audio import PyfficeAudio
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "video.yaml")


class PyfficeVideo(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeVideo").override(cfg)
        self.has_audio = False
        self.audio = None

    def check_audio(self):
        """"""
        if self.audio is None:
            self.audio = PyfficeAudio()
        return self

    def cut_section(self, start, end, keep=False):
        """"""
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
        """"""

    def find_unpause(self):
        """"""

    def get_duration(self):
        """"""

    def get_palette(self):
        """"""

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
