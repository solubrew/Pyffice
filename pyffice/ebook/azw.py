"""Amazon Kindle (AZW) ebook format support.

The load/read/write/dump helpers are thin wrappers around the
shared :mod:`pyffice.io_helpers` byte I/O. They're kept here so
callers can continue to import ``from pyffice.ebook.azw import
load`` etc. (the per-format module API is part of pyffice's
public surface).
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
    """Load AZW ebook contents."""
    return load_bytes(path)


def read(path: str) -> bytes:
    """Read AZW ebook contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to AZW file."""
    write_bytes(data, path)


def dump(data: bytes, path: str) -> None:
    """Dump data to AZW file."""
    write(data, path)
