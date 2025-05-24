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
from pyffice.document import PyfficeDocumentManager, PyfficeUnit
from pyffice.calendars.tasks import PyfficeEvent, PyfficeTask, PyfficeTimeUnit

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "calendars.yaml")


class PyfficeCalendar(PyfficeDocumentManager):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).override("PyfficeCalendar")).override(cfg)
        self.events = None
        self.time_unit = None
        self.tasks = None
        self.time_scale = None
        self.start_date = None
        self.end_date = None

    def add_event(self, event):
        """"""
        cfg = {"event": event}
        event = PyfficeEvent(cfg)
        self.add_change("events", deepcopy(self.events), event)
        self.events.append(event)
        return self

    def add_task(self, task):
        """"""
        cfg = {"task": task}
        task = PyfficeTask(cfg)
        self.add_change("tasks", deepcopy(self.tasks), task)
        self.tasks.append(task)
        return self

    def del_event(self, event):
        """"""
        if event in self.events:
            self.events.remove(event)
            self.add_change("events", deepcopy(self.events), self.events, "del")

    def del_task(self, task):
        """"""
        if task in self.tasks:
            self.tasks.remove(task)
            self.add_change("tasks", deepcopy(self.tasks), self.tasks, "del")

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_date_start(document.get("start_date", None))
        self.set_date_end(document.get("end_date", None))
        self.set_time_scale(document.get("time_scale", "day"))
        self.set_scale_unit(document.get("scale_unit", "quarter_hour"))
        self.set_events(document.get("events", []))
        self.set_tasks(document.get("tasks", []))
        return self

    def set_date_end(self, date):
        """"""
        if date != self.end_date:
            self.add_change("end_date", self.end_date, date)
            self.end_date = date
        return self

    def set_date_start(self, date):
        """"""
        if date != self.start_date:
            self.add_change("start_date", self.start_date, date)
            self.start_date = date
        return self

    def set_events(self, events):
        """"""
        cfg = {"events": events}
        event = PyfficeEvent(cfg)
        self.events.append(event)
        return self

    def set_time_unit(self, time_unit):
        """"""
        cfg = {"time_unit": time_unit, "scale": self.time_scale}
        time_unit = PyfficeTimeUnit(cfg)
        if time_unit != self.time_unit:
            self.add_change("time_unit", self.time_unit, time_unit)
            self.time_unit = time_unit
        return self

    def set_tasks(self, tasks):
        """"""
        cfg = {"tasks": tasks}
        task = PyfficeTask(cfg)
        self.tasks.append(task)
        return self

    def set_time_scale(self, time_scale):
        """"""
        cfg = {"time_scale": time_scale}
        time_scale = PyfficeTimeUnit(cfg)
        if time_scale != self.time_scale:
            self.add_change("time_scale", self.scale_unit, time_scale)
            self.time_scale = time_scale
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"]["start_date"] = self.start_date
        doc["document"]["end_date"] = self.end_date
        doc["document"]["time_scale"] = self.time_scale.to_dict()
        doc["document"]["scale_unit"] = self.scale_unit.to_dict()
        doc["document"]["events"] = [x.to_dict() for x in self.events]
        doc["document"]["tasks"] = [x.to_dict() for x in self.tasks]
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
