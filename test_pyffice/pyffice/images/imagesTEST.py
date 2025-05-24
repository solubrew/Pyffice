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

from pyffice.images.images import PyfficeImage

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "imagesTEST.yaml")
test_000 = True
test_001 = True


class Test_PyfficeDocument(unittest.TestCase):
    """ """

    @classmethod
    def setup_class(cls, cfg=None):
        """

        :param cfg:
        :return:
        """
        cls.config = condor.Instruct(pxcfg).select("Test_PyfficeImage")
        if test_000:
            cls.test_PyfficeImage_000 = PyfficeImage()
        if test_001:
            cfg = {"document": cls.config.dikt["fixture_001"]["document"]}
            cls.test_PyfficeImage_001 = PyfficeImage(cfg)
        return cls()

    @classmethod
    def teardown_class(cls):
        """
        :return:
        """

    def test_all(self):
        """"""
        return self

    def test_init(self):
        """
        :return:
        """
        return self

    def test_load_document(self):
        """"""
        return self

    def to_dict(self):
        """"""
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
