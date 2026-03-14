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
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

try:
    import dia

    HAS_DIA = True
except ImportError:
    HAS_DIA = False
    pass
# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from subtrix.utilities import uuid
from ogma.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.images.images import PyfficeImage
from pyffice.text.text import PyfficeScript
from pyffice.web.url import PyfficeURL
from pycurity.pymatch import extract_urls

from pyffice.web.web import PyfficeWebBrowser
from pyffice.config.ports import PyfficePort

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "imports.yaml")


class PyfficePortGoogleDocs(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficePortGoogleDocs")).override(cfg)

    def to_native(self):
        """"""

    def to_xml(self):
        """"""


class PyfficePortGoogleForms(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("")).override(cfg)

    def to_native(self):
        """"""

    def to_xml(self):
        """"""


class PyfficePortGoogleSheets(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficePortGoogleSheets")).override(cfg)

    def to_native(self):
        """"""

    def to_xml(self):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
