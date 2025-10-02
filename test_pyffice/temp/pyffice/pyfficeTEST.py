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
from pyffice.pyffice import Document

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")
cfg = condor.Instruct(pxcfg).select("Test_PyfficeUnit").dikt
test_000 = True
test_001 = True
test_002 = True
test_003 = True
test_004 = True
test_005 = True

fixtures = condor.Instruct(join(here, "..", "fixtures", "fixtures.yaml")).override(cfg).dikt
fixture001 = fixtures["fixture_001"]
fixture003 = fixtures["fixture_003"]
fixture005 = fixtures["fixture_005"]


class Test_(unittest.TestCase):
    """ """

    @classmethod
    def setup_class(cls):
        """
        :return:
        """
        path = join(here, "", "../fixtures", "orgnql", "", "")
        cls.test_Document = Document()
        cfg = {}
        cls.config = condor.instruct(pxcfg).override(cfg)

    @classmethod
    def teardown_class(cls):
        """
        :return:
        """

    def test_init(self):
        """

        :return:
        """
        assert self.test_Document.parent == None

    def test_open(self):
        """"""

    def test_save(self):
        """"""

    def test_save_as(self):
        """"""

    def test_save_copy_as(self):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
