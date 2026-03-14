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
    -(WT)-: -32  # 2026-01-15 20:31:30
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import unittest  # 2026-01-15 20:31:30
import tempfile  # 2026-01-15 20:31:30
import json  # 2026-01-15 20:31:30
import os  # 2026-01-15 20:31:30
from pathlib import Path  # 2026-01-15 20:21:44
from typing import Any, Dict, List, Optional  # 2026-01-15 20:21:44
from os.path import join  # 2026-01-15 20:21:44
from os.path import dirname  # 2026-01-15 20:21:44

# ======================================3rd Party Library Modules=====================================================||
from pathlib import Path  # 2026-01-15 20:31:30
from typing import Any, Dict, List, Optional  # 2026-01-15 20:31:30
from os.path import join  # 2026-01-15 20:31:30
from os.path import dirname  # 2026-01-15 20:31:30
from ogma.logma import Logma  # 2026-01-15 20:31:30

# =========================================Local Library Modules======================================================||
from ogma.logma import Logma  # 2026-01-15 20:21:44

from condor import condor  # 2026-01-15 20:21:44
import pytest  # 2026-01-15 20:31:30
import hypothesis  # 2026-01-15 20:31:30
from condor import condor  # 2026-01-15 20:31:30

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2026-01-15 20:31:30
LOGMA = Logma(__name__)  # 2026-01-15 20:31:30
PXCFG = join(HERE, "_data_", "__init__TEST.yaml")  # 2026-01-15 20:31:30
CFG = condor.Instruct(PXCFG).load().dikt  # 2026-01-15 20:31:30


# ====================================================================================================================||


# ====================================================================================================================||
"""

  # 2026-01-15 20:31:30


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
