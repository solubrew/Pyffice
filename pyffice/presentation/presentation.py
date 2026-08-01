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
from pptx import Presentation
from pptx.util import Inches

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "presentation.yaml")


class PyfficeShow(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """A Presentation document type that can link to individual slides, or any other PyfficeDocument type"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeShow").override(cfg)


class PyfficeSlide(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """A single slide document type"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeSlide").override(cfg)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
