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
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficePersona(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("")).override(cfg)

    def calculate_myers_briggs(self, ei=0.5, ns=0.5, tf=0.5, pj=0.5):
        """"""
        if ei >= 0.5:
            myersbriggs = "I"
        else:
            myersbriggs = "E"
        if ns >= 0.5:
            myersbriggs += "S"
        else:
            myersbriggs += "N"
        if tf >= 0.5:
            myersbriggs += "F"
        else:
            myersbriggs += "T"
        if pj >= 0.5:
            myersbriggs += "J"
        else:
            myersbriggs += "P"
        return myersbriggs


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
