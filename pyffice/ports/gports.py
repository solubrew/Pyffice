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
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||

try:
    import dia

    HAS_DIA = True
except ImportError:
    HAS_DIA = False
    pass
# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

from pyffice.ports.ports import PyfficePort

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "../config/_data_", "imports.yaml")


class PyfficePortGoogleDocs(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortGoogleDocs")).override(cfg)

    def to_native(self):
        """Convert to native format."""
        return self.document

    def to_xml(self):
        """Convert to XML format."""
        return self.to_dict()


class PyfficePortGoogleForms(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("")).override(cfg)

    def to_native(self):
        """Convert to native format."""
        return self.document

    def to_xml(self):
        """Convert to XML format."""
        return self.to_dict()


class PyfficePortGoogleSheets(PyfficePort):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortGoogleSheets")).override(cfg)

    def to_native(self):
        """Convert to native format."""
        return self.document

    def to_xml(self):
        """Convert to XML format."""
        return self.to_dict()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
