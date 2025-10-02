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

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficePlaylist(PyfficeDocument):
    """Pyffice Playlist is a workflow for processing content in a playlist. The playlist can consist of multiple
    content types and multiple addressing methods"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).override("")
        super().__init__(self)
        self.config.override(cfg)

    def add_content_service(self):
        """
        Allow content services like Netflix, Youtube etc as well as local videos, music, photoshows, etc


        :return:
        """

    def add_content(self):
        """
        could be a name of a show or a music artist or a youtube clip

        :return:
        """

    def random_schedule(self):
        """
        randomly swap in various content sources
        :return:
        """

    def ebbnflow_schedule(self):
        """"""

    def schedule(self):
        """"""

    def import_schedule(self):
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
