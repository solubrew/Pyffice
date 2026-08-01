"""MOBI ebook format support.

Thin wrappers around :mod:`pyffice.io_helpers` byte I/O. See
:mod:`pyffice.ebook.azw` for the rationale on keeping the
per-format module API.
"""

from typing import Any, Optional
import io

from pyffice.io_helpers import load_bytes, write_bytes

#!/usr/bin/env python3
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
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

# ======================================3rd Party Library Modules=====================================================||


# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

# ====================================================================================================================||
HERE = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
PXCFG = join(HERE, "_data_", ".yaml")

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||


def load(path: str) -> bytes:
    """Load MOBI ebook contents."""
    return load_bytes(path)


def read(path: str) -> bytes:
    """Read MOBI ebook contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to MOBI file."""
    write_bytes(data, path)


def dump(data: bytes, path: str) -> None:
    """Dump data to MOBI file."""
    write(data, path)
