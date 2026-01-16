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
    -(WT)-: -32  # 2026-01-15 20:29:10
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import unittest  # 2026-01-15 20:29:09
import tempfile  # 2026-01-15 20:29:09
import json  # 2026-01-15 20:29:09
import os  # 2026-01-15 20:29:09
from pathlib import Path  # 2026-01-15 20:19:30
from typing import Any, Dict, List, Optional  # 2026-01-15 20:19:30
from os.path import join  # 2026-01-15 20:19:30
from os.path import dirname  # 2026-01-15 20:19:31

# ======================================3rd Party Library Modules=====================================================||
from pathlib import Path  # 2026-01-15 20:29:09
from typing import Any, Dict, List, Optional  # 2026-01-15 20:29:09
from os.path import join  # 2026-01-15 20:29:09
from os.path import dirname  # 2026-01-15 20:29:10
from ogma.logma import Logma  # 2026-01-15 20:29:10

# =========================================Local Library Modules======================================================||
from ogma.logma import Logma  # 2026-01-15 20:19:31

from condor import condor  # 2026-01-15 20:19:31
import pytest  # 2026-01-15 20:29:10
import hypothesis  # 2026-01-15 20:29:10
from condor import condor  # 2026-01-15 20:29:10

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2026-01-15 20:29:10
LOGMA = Logma(__name__)  # 2026-01-15 20:29:10
PXCFG = join(HERE, "_data_", "__init__TEST.yaml")  # 2026-01-15 20:29:10
CFG = condor.Instruct(PXCFG).load().dikt  # 2026-01-15 20:29:10


# ====================================================================================================================||


# ====================================================================================================================||
"""

  # 2026-01-15 20:29:10


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
