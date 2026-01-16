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
    -(WT)-: -32  # 2026-01-15 20:30:37
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import unittest  # 2026-01-15 20:30:37
import tempfile  # 2026-01-15 20:30:37
import json  # 2026-01-15 20:30:37
import os  # 2026-01-15 20:30:37
from pathlib import Path  # 2026-01-15 20:20:53
from typing import Any, Dict, List, Optional  # 2026-01-15 20:20:53
from os.path import join  # 2026-01-15 20:20:53
from os.path import dirname  # 2026-01-15 20:20:53

# ======================================3rd Party Library Modules=====================================================||
from pathlib import Path  # 2026-01-15 20:30:37
from typing import Any, Dict, List, Optional  # 2026-01-15 20:30:37
from os.path import join  # 2026-01-15 20:30:37
from os.path import dirname  # 2026-01-15 20:30:37
from ogma.logma import Logma  # 2026-01-15 20:30:37

# =========================================Local Library Modules======================================================||
from ogma.logma import Logma  # 2026-01-15 20:20:53

from condor import condor  # 2026-01-15 20:20:53
import pytest  # 2026-01-15 20:30:37
import hypothesis  # 2026-01-15 20:30:37
from condor import condor  # 2026-01-15 20:30:37

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2026-01-15 20:30:37
LOGMA = Logma(__name__)  # 2026-01-15 20:30:37
PXCFG = join(HERE, "_data_", "__init__TEST.yaml")  # 2026-01-15 20:30:37
CFG = condor.Instruct(PXCFG).load().dikt  # 2026-01-15 20:30:37


# ====================================================================================================================||


# ====================================================================================================================||
"""

  # 2026-01-15 20:30:37


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
