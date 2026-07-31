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
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocumentManager, PyfficeUnit
from pyffice.calendars.events import PyfficeEvent, PyfficeTimeUnit  # , PyfficeTask

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "calendars.yaml")


class PyfficeCalendar(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).override("PyfficeCalendar")).override(cfg)
        self.events = None
        self.time_unit = None
        self.tasks = []
        self.time_scale = None
        self.start_date = None
        self.end_date = None
        self.time_unit = None

    def add_event(self, event):
        """Add a event.
        
        Args:
            event: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"event": event}
        event = PyfficeEvent(cfg)
        self.add_change("events", deepcopy(self.events), event)
        self.events.append(event)
        return self

    # def add_task(self, task):
    #     """"""
    #     cfg = {"task": task}
    #     task = PyfficeTask(cfg)
    #     self.add_change("tasks", deepcopy(self.tasks), task)
    #     self.tasks.append(task)
    #     return self

    def del_event(self, event):
        """Remove the event.
        
        Args:
            event: Parameter.
        
        Returns:
            Self for chaining.
        """
        if event in self.events:
            self.events.remove(event)
            self.add_change("events", deepcopy(self.events), self.events, "del")

    # def del_task(self, task):
    #     """"""
    #     if task in self.tasks:
    #         self.tasks.remove(task)
    #         self.add_change("tasks", deepcopy(self.tasks), self.tasks, "del")

    def load_document(self, document=None):
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_date_start(document.get("start_date", None))
        self.set_date_end(document.get("end_date", None))
        self.set_time_scale(document.get("time_scale", "day"))
        # PyfficeTimeUnit()
        # self.set_scale_unit(document.get("scale_unit", "quarter_hour"))
        self.set_events(document.get("events", []))
        self.set_tasks(document.get("tasks", []))
        return self

    def set_date_end(self, date):
        """Set the date end.
        
        Args:
            date: Parameter.
        
        Returns:
            Self for chaining.
        """
        if date != self.end_date:
            self.add_change("end_date", self.end_date, date)
            self.end_date = date
        return self

    def set_date_start(self, date):
        """Set the date start.
        
        Args:
            date: Parameter.
        
        Returns:
            Self for chaining.
        """
        if date != self.start_date:
            self.add_change("start_date", self.start_date, date)
            self.start_date = date
        return self

    def set_events(self, events):
        """Replace self.events with [PyfficeEvent(e) for e in events]."""
        self.events = [PyfficeEvent({"event": x}) for x in events]
        return self

    def set_tasks(self, tasks):
        """Set the tasks.
        
        Args:
            tasks: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.tasks += tasks

    def set_time_unit(self, time_unit):
        """Set the time unit.
        
        Args:
            time_unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"time_unit": time_unit, "scale": self.time_scale}
        time_unit = PyfficeTimeUnit(cfg)
        if time_unit != self.time_unit:
            self.add_change("time_unit", self.time_unit, time_unit)
            self.time_unit = time_unit
        return self

    # def set_tasks(self, tasks):
    #     """"""
    #     cfg = {"tasks": tasks}
    #     task = PyfficeTask(cfg)
    #     self.tasks.append(task)
    #     return self

    def set_time_scale(self, time_scale):
        """Set the time scale.
        
        Args:
            time_scale: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"time_scale": time_scale}
        time_scale = PyfficeTimeUnit(cfg)
        if time_scale != self.time_scale:
            self.add_change("time_scale", time_scale.scale_unit, time_scale)
            self.time_scale = time_scale
        return self

    def to_dict(self):
        """Convert this document to dict.
        
        Returns:
            Self for chaining.
        """
        doc = super().to_dict()
        if "document" not in doc.keys():
            doc["document"] = {}
        doc["document"]["start_date"] = self.start_date
        doc["document"]["end_date"] = self.end_date
        doc["document"]["time_scale"] = self.time_scale.to_dict()
        #doc["document"]["scale_unit"] = self.scale_unit.to_dict()
        doc["document"]["events"] = [x.to_dict() for x in self.events]
        doc["document"]["tasks"] = [x.to_dict() for x in self.tasks]
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
