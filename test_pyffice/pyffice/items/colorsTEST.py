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
from pyffice.items.colors import PyfficeColor

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "colorsTEST.yaml")
test_000 = True
test_001 = True


class Test_PyfficeColor(unittest.TestCase):
    """ """

    @classmethod
    def setup_class(cls, cfg=None):
        """

        :param cfg:
        :return:
        """
        cls.config = condor.Instruct(pxcfg).select("Test_PyfficeColor")
        if test_000:
            cls.test_PyfficeColor_000 = PyfficeColor()
        if test_001:
            cfg = {"document": cls.config.dikt["fixture_001"]["document"]}
            cls.test_PyfficeColor_001 = PyfficeColor(cfg)
        return cls()

    @classmethod
    def teardown_class(cls):
        """
        :return:
        """

    def test_all(self):
        """"""

    def test_init(self):
        """
        :return:
        """

    def test_load_unit(self):
        """"""
        if test_000:
            self.text_PyfficeColor_000.load_unit()
            self.assertIsInstance(self.text_PyfficeColor_000.unit, dict)
            assert self.text_PyfficeColor_000.name == "Test Unit 000"
            assert self.text_PyfficeColor_000.author == "test_000"
            assert self.text_PyfficeColor_000.description == "Test Unit 000"
            assert self.test_Pyffic

    def test_to_dict(self):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
