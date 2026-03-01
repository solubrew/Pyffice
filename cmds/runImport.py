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
from sys import argv
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
import crow

crow.crowLoad("", "DELTA")

from condor import condor
from ogma.logma import Logma
from pyffice.config.gports import PyfficeImportCherryTree

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
log = True

# ====================================================================================================================||
pxcfg = join(here, "_data_", "runMain.yaml")


def run(args):
    """Run individual tabs with mock data for development purposes"""
    file_path = "/home/solubrew/_work/MicroMole.ctd"
    if args[1] == "cherry_tree":
        doc = PyfficeImportCherryTree({"file_path": file_path})
        logma.info(doc.import_file())


if __name__ == "__main__":
    start = dt.datetime.now()
    logma.info("Start")
    run(argv)
    end = dt.datetime.now()
    logma.info(f"End Duration {end - start}")


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
