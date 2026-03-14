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

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "audio.yaml")


class PyfficeAudio(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, path, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeAudio")
        super().__init__()
        self.config.override(cfg)
        self.path = path
        # self.audio = pydub.AudioSegment.from_file(path)

    def add_fade(self, inn=False, out=False, in_duration=None, out_duration=None):
        """"""
        if inn:
            if in_duration is None:
                in_duration = 2000
            self.audio = self.audio.fade_in(in_duration)
        if out:
            if out_duration is None:
                out_duration = 2000
            self.audio = self.audio.fade_out(out_duration)
        return self

    def convert_mp3_to_wave(self, new_path):
        """"""
        if not has_ffmpeg:
            logma.warning(f"MP3 Not Supported without FFMPEG.")
        return self

    def convert_wav_to_mp3(self, new_path):
        """"""
        if not has_ffmpeg:
            logma.warning(f"MP3 Not Supported without FFMPEG.")
        self.audio.export(new_path, format="mp3")
        return self

    def cut_section(self, start, end, keep=False):
        """"""
        trimmed_audio = self.audio[start:end]
        trimmed_audio.export(self.path, format="mp3")
        return self

    def find_pause(self):
        """"""
        return self

    def find_unpause(self):
        """"""
        return self

    def get_duration(self):
        """"""
        return self

    def increase_volume(self, percent):
        """"""

    def decrease_volume(self, percent):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficePlayList(PyfficeDocumentManager):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).override("")
        super().__init__(self)
        self.config.override(cfg)

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
