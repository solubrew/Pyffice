# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
-(META)-:
    docid: <[uuid]>
    name: <[file name]>
    description: >
      <[description]>
    expiry: <[expiration]>
    version: <[version]>
    authority: <[authority]>
    security: <[security]>
    -(WT)-: -32  # 2025-11-29 11:59:53
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt
import unittest


import json  # 2025-11-29 11:59:53
import tempfile  # 2025-11-29 11:59:53
import os  # 2025-11-29 11:59:53

# ======================================3rd Party Library Modules=====================================================||
from pyffice.items.shapes import PyfficeShape

import join  # 2025-11-29 11:59:53
import dirname  # 2025-11-29 11:59:53
import Logma  # 2025-11-29 11:59:53

# =========================================Local Library Modules======================================================||
from condor import condor
from ogma.logma import Logma

import condor  # 2025-11-29 11:59:53

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

pxcfg = join(here, "_data_", "shapesTEST.yaml")
cfg = condor.Instruct(pxcfg).select("Test_PyfficeUnit").dikt
test_000 = True
test_001 = True


HERE = join(dirname(__file__))  # 2025-11-29 11:59:53
LOGMA = Logma(__name__)  # 2025-11-29 11:59:53
PXCFG = join(HERE, "_data_", "shapesTEST.yaml")  # 2025-11-29 11:59:53
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-29 11:59:53
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-29 11:59:53

# ====================================================================================================================||


class Test_PyfficeShape(unittest.TestCase):  # 2025-11-29 11:59:53
    """"""

    @classmethod
    def setup_class(cls, cfg=None):
        """

        :param cfg:
        :return:
        """
        cls.config = condor.Instruct(pxcfg).select("Test_PyfficeShape")
        if test_000:
            cls.test_PyfficeShape_000 = PyfficeShape()
        if test_001:
            cfg = {"document": cls.config.dikt["fixture_001"]["document"]}
            cls.test_PyfficeShape_001 = PyfficeShape(cfg)
        return cls()

    @classmethod
    def teardown_class(cls):
        """
        :return:
        """

    def test_all(self):
        """"""
        return self

    def test_add_shape(self):  # 2025-11-29 11:59:53
        """"""
        if TEST_000:
            pass

    def test_add_text(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_init(self):
        """
        :return:
        """
        return self

    def test_load_document(self):
        """"""
        return self

    def test_load_unit(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_mirror_shape(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_mirror_text(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_move_shape(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_move_text(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_rotate_shape(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_rotate_text(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_set_background(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_set_origin(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_set_shapes(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_set_size(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_to_dict(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test_to_html(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def to_dict(self):
        """"""
        return self

    def test___init__(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test__set_envelope(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass

    def test__update_shape_sizes(self):  # 2025-11-29 11:59:54
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-29 11:59:54
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-29 11:59:54
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-29 11:59:54
        """"""

        return

    def reset(self):  # 2025-11-29 11:59:54
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-29 11:59:54
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-29 11:59:53


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
