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
from os import environ
from sys import argv
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||
# import ultimate_notion as uno
from notion_client import Client

# ======================================Solutions Brewer Library Modules==============================================||
import crow

crow.crowLoad("Pyffice", "DELTA")
from pyffice.services.notion import NotionWorkspaceManager
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
log = True

# ====================================================================================================================||
pxcfg = join(here, "_data_", "runNotion.yaml")


def run(args):
    """Run individual tabs with mock data for development purposes"""
    if args[1] == "test":
        notion = Client(auth=environ["NOTION_TOKEN"])
        logma.info(f"Notion {notion.users.list()}")
        page = notion.search(query="Nchantd Action")
        logma.info(f"Notion {page.__dir__()}")
        logma.info(f"Notion {page}")
        # logma.info(f"Notion {notion.search(query='Nchantd Action')}")

        logma.info(notion.__dir__())
        # logma.info(f"Notion {notion.pages.__dir__()}")
        # logma.info(f"Notion {notion.pages.retrieve()}")

        # logma.info(f"Notion {notion.databases.list()}")
        # notion = uno.Session.get_or_create()

        # print(notion.search_db("Nchantd Action"))

    elif args[1] == "connect":
        notion = NotionWorkspaceManager()
        notion.connect("Nchantd Action")


if __name__ == "__main__":
    start = dt.datetime.now()
    logma.info("Start")
    run(argv)
    end = dt.datetime.now()
    logma.info(f"End Duration {end - start}")


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
