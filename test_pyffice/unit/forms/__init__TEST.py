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
    -(WT)-: -32  # 2026-01-15 20:29:59
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import unittest  # 2026-01-15 20:29:58
import tempfile  # 2026-01-15 20:29:58
import json  # 2026-01-15 20:29:58
import os  # 2026-01-15 20:29:58
from pathlib import Path  # 2026-01-15 20:20:17
from typing import Any, Dict, List, Optional  # 2026-01-15 20:20:17
from os.path import join  # 2026-01-15 20:20:17
from os.path import dirname  # 2026-01-15 20:20:17

# ======================================3rd Party Library Modules=====================================================||
from pathlib import Path  # 2026-01-15 20:29:58
from typing import Any, Dict, List, Optional  # 2026-01-15 20:29:58
from os.path import join  # 2026-01-15 20:29:58
from os.path import dirname  # 2026-01-15 20:29:59
from ogma.logma import Logma  # 2026-01-15 20:29:59

# =========================================Local Library Modules======================================================||
from ogma.logma import Logma  # 2026-01-15 20:20:17

from condor import condor  # 2026-01-15 20:20:17
import pytest  # 2026-01-15 20:29:59
import hypothesis  # 2026-01-15 20:29:59
from condor import condor  # 2026-01-15 20:29:59

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2026-01-15 20:29:59
LOGMA = Logma(__name__)  # 2026-01-15 20:29:59
PXCFG = join(HERE, "_data_", "__init__TEST.yaml")  # 2026-01-15 20:29:59
CFG = condor.Instruct(PXCFG).load().dikt  # 2026-01-15 20:29:59


# ====================================================================================================================||


# ====================================================================================================================||
"""

  # 2026-01-15 20:29:59


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
