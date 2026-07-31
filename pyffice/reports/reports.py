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
from pyffice.text.text import PyfficeScript

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "_data_", "reports.yaml")


class PyfficeReport(PyfficeScript):
    """Pyffice Report is a Document type that handles reports within the pyffice framework. A report is a specifically
    structured Pyffice Script that requires certain fields and metadata"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(pxcfg).select("Report").override(cfg)
        self.summary = None
        self.appendices = []

    def add_summary(self, summary=None):
        """Add a summary to the report"""
        if summary is None:
            summary = self.generate_summary()
        self.summary = summary

    def add_appendix(self, appendix):
        """Add an appendix to the report"""
        self.appendices.append(appendix)

    def generate_summary(self):
        """Generate a summary of the report"""
        return f"Summary of {self.config['title']} report"

    def import_report(self):
        """Import a report from a file"""
        # Placeholder - would import report
        return self

    def export_report(self):
        """Export the report to a file"""
        # Placeholder - would export report
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
