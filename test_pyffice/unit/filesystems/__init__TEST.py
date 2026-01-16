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
    -(WT)-: -32  # 2026-01-15 20:29:57
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import unittest  # 2026-01-15 20:29:56
import tempfile  # 2026-01-15 20:29:56
import json  # 2026-01-15 20:29:56
import os  # 2026-01-15 20:29:56
from pathlib import Path  # 2026-01-15 20:20:15
from typing import Any, Dict, List, Optional  # 2026-01-15 20:20:15
from os.path import join  # 2026-01-15 20:20:15
from os.path import dirname  # 2026-01-15 20:20:15

# ======================================3rd Party Library Modules=====================================================||
from pathlib import Path  # 2026-01-15 20:29:56
from typing import Any, Dict, List, Optional  # 2026-01-15 20:29:56
from os.path import join  # 2026-01-15 20:29:56
from os.path import dirname  # 2026-01-15 20:29:56
from ogma.logma import Logma  # 2026-01-15 20:29:56

# =========================================Local Library Modules======================================================||
from ogma.logma import Logma  # 2026-01-15 20:20:15

from condor import condor  # 2026-01-15 20:20:15
import pytest  # 2026-01-15 20:29:56
import hypothesis  # 2026-01-15 20:29:56
from condor import condor  # 2026-01-15 20:29:56

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2026-01-15 20:29:56
LOGMA = Logma(__name__)  # 2026-01-15 20:29:56
PXCFG = join(HERE, "_data_", "__init__TEST.yaml")  # 2026-01-15 20:29:56
CFG = condor.Instruct(PXCFG).load().dikt  # 2026-01-15 20:29:56


# ====================================================================================================================||


# ====================================================================================================================||
"""

  # 2026-01-15 20:29:57


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
