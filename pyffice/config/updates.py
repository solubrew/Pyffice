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


class PyfficeUpdate(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeUpdate").override(cfg)
        self.document = None

    def create_temp_file(self):
        """"""
        return

    def process(self):
        """"""
        document = self.config.dikt.get("document", {})
        return document


class PyfficeUnitUpdate(PyfficeUpdate):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("")).override(cfg)

    def create_temp_unit(self):
        """"""


class PyfficeDocumentUpdate(PyfficeUpdate):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("")).override(cfg)

    def create_temp_document(self):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
