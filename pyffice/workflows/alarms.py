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
from copy import deepcopy

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pyffice.calendars.tasks import PyfficeEvent, PyfficeTask

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "alarms.yaml")


class PyfficeAlarm(PyfficeEvent):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeAlarm")).override(cfg)
        self.acknowledge_task = None
        self.notify_task = None
        self.limit = None
        self.postpone_task = None
        self.postpones = []
        self.tasks = None

    def add_postpone(self, postpone):
        """"""
        self.postpones.append(PyfficeTask(postpone))
        return self

    def load_unit(self, unit):
        """"""
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        self.set_tasks(unit.get("tasks", None))
        return self

    def set_acknowledge(self, acknowledge):
        """"""
        cfg = {"acknowledge": acknowledge}
        self.acknowledge_task = PyfficeTask(cfg)
        return self

    def set_limit(self, limit):
        """"""
        if limit != self.limit:
            self.add_change("limit", self.limit, limit)
            self.limit = limit
        return self

    def set_notify(self, notify):
        """"""
        cfg = {"notify": notify}
        self.notify_task = PyfficeTask(cfg)
        return self

    def set_postpone(self, postpone):
        """"""
        cfg = {"postpone": postpone}
        self.postpone_task = PyfficeTask(cfg)
        return self

    def set_tasks(self, tasks):
        """"""
        self.set_notify(tasks["notify"])
        self.set_acknowledge(tasks["acknowledge"])
        self.set_postpone(tasks["postpone"])
        tasks = {"notify": self.notify_task, "acknowledge": self.acknowledge_task}
        if tasks != self.tasks:
            self.add_change("tasks", deepcopy(self.tasks), deepcopy(tasks))
            self.tasks = tasks
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = {
            "tasks": {"notify": self.tasks["notify"].to_dict(), "acknowledge": self.tasks["acknowledge"].to_dict()}
        }
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
