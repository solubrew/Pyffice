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
    -(WT)-: -32  # 2025-11-29 11:58:44
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-29 11:58:44
import tempfile  # 2025-11-29 11:58:44
import os  # 2025-11-29 11:58:44

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-29 11:58:44
import dirname  # 2025-11-29 11:58:44
import Logma  # 2025-11-29 11:58:44
from pyffice.charts.sankey import SankeyChart  # 2025-11-29 11:58:44

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-29 11:58:44

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-29 11:58:44
LOGMA = Logma(__name__)  # 2025-11-29 11:58:44
PXCFG = join(HERE, "_data_", "sankeyTEST.yaml")  # 2025-11-29 11:58:44
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-29 11:58:44
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-29 11:58:44

# ====================================================================================================================||


class Test_SankeyChart:  # 2025-11-29 11:58:44
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-29 11:58:44
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-29 11:58:44
        """"""

        return

    def reset(self):  # 2025-11-29 11:58:44
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-29 11:58:44
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_create_sankey_chart(self):  # 2025-11-29 11:58:44
        """"""
        if TEST_000:
            pass

    def test_load_document(self):  # 2025-11-29 11:58:44
        """"""
        if TEST_000:
            pass

    def test_open_file(self):  # 2025-11-29 11:58:44
        """"""
        if TEST_000:
            pass

    def test_save_sankey_chart(self):  # 2025-11-29 11:58:44
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-29 11:58:44
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-29 11:58:44
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-29 11:58:44
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-29 11:58:44
        """"""

        return

    def reset(self):  # 2025-11-29 11:58:44
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-29 11:58:44
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-29 11:58:44


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
