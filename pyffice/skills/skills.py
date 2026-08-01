# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
            create a skill system for an internal Ai Agent



        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
# T-NEW-066 step 4: condor was the original SB-stack logging package
# and was folded into kahndor (per user direction, 2026-07-31). The
# previous `from condor import condor` here was a stale reference.
# kahndor is the only SB-stack dependency this module needs.
from kahndor import kahndor  # noqa: F401
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")

# NOTE: this skills framework is intentionally scoped to creating
# documents within the database file (for downstream nchantdoffice
# integration). It blocks access to system files outside the
# document store. See T-NEW-054 for the protocol design and
# T-NEW-067 for the implementation card.
#
# PLACEHOLDER: as of 2026-07-31, this module does NOT define the
# PyfficeSkill / PyfficeSkillManager / PyfficeCapability / SkillRegistry
# classes that `pyffice/skills/__init__.py` re-exports. Those classes
# are T-NEW-067 work. Until then, the lazy __getattr__ proxy in
# __init__.py preserves importability without crashing.
# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
