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

from pyffice.tags.ratings import PyfficeRating

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "ratingsTEST.yaml")
cfg = condor.Instruct(pxcfg).select("Test_PyfficeUnit").dikt
test_000 = True
test_001 = True


class Test_PyfficeRating(unittest.TestCase):
    """ """

    @classmethod
    def setup_class(cls, cfg=None):
        """

        :param cfg:
        :return:
        """
        cls.config = condor.Instruct(pxcfg).select("Test_PyfficeRating")
        if test_000:
            cls.test_PyfficeRating_000 = PyfficeRating()
        if test_001:
            cfg = {"document": cls.config.dikt["fixture_001"]["document"]}
            cls.test_PyfficeRating_001 = PyfficeRating(cfg)
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
