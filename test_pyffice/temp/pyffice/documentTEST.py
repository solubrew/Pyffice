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
from pyffice.document import PyfficeUnit, PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "documentTEST.yaml")
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


class Test_PyfficeUnit(unittest.TestCase):
    """ """

    @classmethod
    def setup_class(cls, cfg=None):
        """

        :param cfg:
        :return:
        """
        if test_000:
            cls.test_PyfficeUnit_000 = PyfficeUnit()
        if test_001:
            cfg = {"unit": fixture001["document"]}
            cls.test_PyfficeUnit_001 = PyfficeUnit(cfg)
        return cls()

    @classmethod
    def teardown_class(cls):
        """
        :return:
        """

    def test_all(self):
        """"""
        self.test_load_unit()
        return self

    def test_init(self):
        """
        :return:
        """

    def test_load_unit(self):
        """"""
        logma.info(f"Test load_unit")
        if test_000:
            self.test_PyfficeUnit_000.load_unit()
            assert len(self.test_PyfficeUnit_000.did) == 36, len(self.test_PyfficeUnit_000.did)
            assert self.test_PyfficeUnit_000.name == self.test_PyfficeUnit_000.did, self.test_PyfficeUnit_000.name
            assert self.test_PyfficeUnit_000.description == "", self.test_PyfficeUnit_000.description
            assert self.test_PyfficeUnit_000.author == "", self.test_PyfficeUnit_000.author
            assert self.test_PyfficeUnit_000.context == "", self.test_PyfficeUnit_000.context
            assert self.test_PyfficeUnit_000.editors == [], self.test_PyfficeUnit_000.editors
            assert self.test_PyfficeUnit_000.encoding == "utf-8", self.test_PyfficeUnit_000.encoding
            assert (
                self.test_PyfficeUnit_000.hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            ), self.test_PyfficeUnit_000.hash
            assert self.test_PyfficeUnit_000.location == "", self.test_PyfficeUnit_000.location
            assert self.test_PyfficeUnit_000.path == "", self.test_PyfficeUnit_000.path
            assert self.test_PyfficeUnit_000.syntax == "plain-text", self.test_PyfficeUnit_000.syntax
            assert self.test_PyfficeUnit_000.tags == [], self.test_PyfficeUnit_000.tags
            self.assertIsInstance(self.test_PyfficeUnit_000.creon, str)
            self.assertIsInstance(self.test_PyfficeUnit_000.modon, str)
            logma.info(f"Test 000 Complete")

        if test_001:
            self.test_PyfficeUnit_001.load_unit()
            assert (
                self.test_PyfficeUnit_001.did == "0681d16e-6bd2-70eb-8000-3fc171bd0f36"
            ), self.test_PyfficeUnit_001.did
            assert self.test_PyfficeUnit_001.name == "test_unit", self.test_PyfficeUnit_001.name
            assert self.test_PyfficeUnit_001.description == "Test Unit 000", self.test_PyfficeUnit_001.description
            assert self.test_PyfficeUnit_001.author == "SoluBrew", self.test_PyfficeUnit_001.author
            assert self.test_PyfficeUnit_001.context == "", self.test_PyfficeUnit_001.context
            assert self.test_PyfficeUnit_001.editors == [
                "SoluBrew",
            ], self.test_PyfficeUnit_001.editors
            assert self.test_PyfficeUnit_001.encoding == "utf-8", self.test_PyfficeUnit_001.encoding
            assert self.test_PyfficeUnit_001.hash == "", self.test_PyfficeUnit_001.hash
            assert self.test_PyfficeUnit_001.location == "", self.test_PyfficeUnit_001.location
            assert self.test_PyfficeUnit_001.path == "", self.test_PyfficeUnit_001.path
            assert self.test_PyfficeUnit_001.syntax == "", self.test_PyfficeUnit_001.syntax
            assert self.test_PyfficeUnit_001.tags == ["test", "fixture"], self.test_PyfficeUnit_001.tags
            assert self.test_PyfficeUnit_001.creon == "2025-05-08 16:43:50", self.test_PyfficeUnit_001.creon
            assert self.test_PyfficeUnit_001.modon == "2025-05-08 16:43:50", self.test_PyfficeUnit_001.modon
            logma.info(f"Test 001 Complete")

    def test_to_dict(self):
        """"""
        logma.info(f"Test to_dict")
        if test_000:
            tree = self.test_PyfficeUnit_000.to_dict()
            assert tree["name"] == self.test_PyfficeUnit_000.name, tree["name"]
            assert tree["did"] == self.test_PyfficeUnit_000.did, tree["did"]
            assert tree["description"] == self.test_PyfficeUnit_000.description, tree["description"]
            assert tree["encoding"] == self.test_PyfficeUnit_000.encoding, tree["encoding"]
            assert tree["hash"] == self.test_PyfficeUnit_000.hash, tree["hash"]
            assert tree["location"] == self.test_PyfficeUnit_000.location, tree["location"]
            assert tree["path"] == self.test_PyfficeUnit_000.path, tree["path"]
            assert tree["syntax"] == self.test_PyfficeUnit_000.syntax, tree["syntax"]
            assert tree["tags"] == self.test_PyfficeUnit_000.tags, tree["tags"]
            assert tree["version"] == self.test_PyfficeUnit_000.version, tree["version"]
            assert tree["meta_data"]["author"] == self.test_PyfficeUnit_000.author, tree["meta_data"]["author"]
            assert tree["meta_data"]["context"] == self.test_PyfficeUnit_000.context, tree["meta_data"]["context"]
            assert tree["meta_data"]["editors"] == self.test_PyfficeUnit_000.editors, tree["meta_data"]["editors"]
            assert tree["meta_data"]["unit_type"] == self.test_PyfficeUnit_000.encoding, tree["meta_data"]["unit_type"]
            assert tree["meta_data"]["creon_dttm"] == self.test_PyfficeUnit_000.creon, tree["meta_data"]["creon_dttm"]
            assert tree["meta_data"]["modon_dttm"] == self.test_PyfficeUnit_000.modon, tree["meta_data"]["modon_dttm"]
            logma.info(f"Test 000 Complete")


class Test_PyfficeDocument(unittest.TestCase):
    """ """

    @classmethod
    def setup_class(cls, cfg=None):
        """

        :param cfg:
        :return:
        """
        if test_002:
            cls.test_PyfficeDocument_002 = PyfficeDocument()
        if test_003:
            cfg = {"unit": fixture003["document"]}
            cls.test_PyfficeDocument_003 = PyfficeDocument(cfg)
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
        if test_002:
            self.test_PyfficeDocument_002.load_document()
        return self

    def to_dict(self):
        """"""
        return self


class Test_PyfficeDocumentManager(unittest.TestCase):
    """ """

    @classmethod
    def setup_class(cls, cfg=None):
        """

        :param cfg:
        :return:
        """
        if test_004:
            cls.test_PyfficeDocumentManager_000 = PyfficeDocumentManager()
        if test_005:
            cfg = {"unit": fixture001["document"]}
            cls.test_PyfficeDocumentManager_001 = PyfficeDocumentManager(cfg)
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
