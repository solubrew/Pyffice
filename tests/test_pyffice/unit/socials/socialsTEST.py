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
    -(WT)-: -32  # 2026-01-15 20:30:36
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import unittest  # 2026-01-15 20:30:36
import tempfile  # 2026-01-15 20:30:36
import json  # 2026-01-15 20:30:36
import os  # 2026-01-15 20:30:36
from pathlib import Path  # 2026-01-15 20:20:53
from typing import Any, Dict, List, Optional  # 2026-01-15 20:20:53
from os.path import join  # 2026-01-15 20:20:53
from os.path import dirname  # 2026-01-15 20:20:53

# ======================================3rd Party Library Modules=====================================================||
from pathlib import Path  # 2026-01-15 20:30:36
from typing import Any, Dict, List, Optional  # 2026-01-15 20:30:36
from os.path import join  # 2026-01-15 20:30:36
from os.path import dirname  # 2026-01-15 20:30:36
from kahndor.logma import Logma  # 2026-01-15 20:30:36

# =========================================Local Library Modules======================================================||
from kahndor.logma import Logma  # 2026-01-15 15:14:14

from kahndor import kahndor  # 2026-01-15 20:20:53

import pytest  # 2026-01-15 20:30:36
import hypothesis  # 2026-01-15 20:30:36
from kahndor import kahndor  # 2026-01-15 20:30:36

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2026-01-15 20:30:36
LOGMA = Logma(__name__)  # 2026-01-15 20:30:36
PXCFG = join(HERE, "_data_", "socialsTEST.yaml")  # 2026-01-15 20:30:36
CFG = kahndor.Instruct(PXCFG).load().dikt  # 2026-01-15 20:30:36


# ====================================================================================================================||


# ====================================================================================================================||
"""

  # 2026-01-15 20:30:36


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
