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
import unittest

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

from pyffice.spreadsheet.spreadsheet import SpreadSheet, PyfficeSpreadSheet

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "spreadsheetTEST.yaml")
test_000 = True
test_001 = True


class Test_PyfficeSpreadSheet(unittest.TestCase):
    """ """

    @classmethod
    def setup_class(cls):
        """
        :return:
        """
        cls.config = condor.Instruct(pxcfg).select("Test_PyfficeSpreadSheet")
        if test_000:
            cls.test_PyfficeSpreadSheet_000 = PyfficeSpreadSheet()
        if test_001:
            cfg = {"document": cls.config.dikt["fixture_001"]["document"]}
            cls.test_PyfficeSpreadSheet_001 = PyfficeSpreadSheet(cfg)
        return cls()

    @classmethod
    def teardown_class(cls):
        """
        :return:
        """

    def test_init(self):
        """

        :return:
        """


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
