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
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocumentManager, PyfficeUnit
from axn.axn import AXN

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "tasks.yaml")

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
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from kahndor.logma import Logma
from pyffice.calendars.calendars import PyfficeTask

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "tasks.yaml")


class PyfficeRecurrenceManager(PyfficeDocumentManager):
    """Extract recurrence information from tasks and then store them in a structure for later retrevial and reprocessing"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).override("")
        super().__init__(self)
        self.config.override(cfg)

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeTasksManager(PyfficeDocumentManager):
    """A Tasks Manager manages projects"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeTaskManager")
        super().__init__(self.config)
        self.config.override(cfg)
        self.init_tasks_manager()

    def add_task(self, name):
        """"""
        # self.documents.append(PyfficeProject(name))


class PyfficeProject(PyfficeTasksManager):
    """A Project Manages Tasks"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeProject")
        super().__init__(self.config)
        self.config.override(cfg)

    def add_task(self, name):
        """"""
        super().add_task()

    def create_new_document(self, name, type_=None):
        """"""
        super().create_new_document(name, "manager")

    def init_project(self):
        """"""

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeProjectsManager(PyfficeTasksManager):
    """A Project Manages Tasks"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeProject")
        super().__init__(self.config)
        self.config.override(cfg)

    def add_project(self, name):
        """"""

    def create_new_document(self, name, type_=None):
        """"""
        super().create_new_document(name, "manager")

    def init_project(self):
        """"""

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeTaskFrame(PyfficeTask):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("PyfficeTask")
        super().__init__(self.config)
        self.config.override(cfg)

    def add_work(self, cfg=None):
        """"""
        work = PyfficeWork(cfg)
        # self.documents.append(work)
        self.document["document"]["work"].append(work)
        return

    def add_precedent(self, precedent):
        """"""
        self.document["document"]["precedents"].append(precedent)

    def add_dependent(self, dependent):
        """"""
        self.document["document"]["dependents"].append(dependent)

    def create_new_document(self, name, type_=None):
        """"""
        super().create_new_document(name, "manager")
        self.document["document"] = {
            "verb_noun_txt": None,
            "entry_dttm": None,
            "due_dttm": None,
            "start_dttm": None,
            "complete_dttm": None,
            "etc_tm": None,
            "parent": None,
            "precedents": [],
            "dependents": [],
            "work": [],
        }

    def set_verb_noun_txt(self, verb_noun):
        """"""
        self.document["documents"]["verb_noun_txt"] = verb_noun
        return self

    def set_due_dttm(self, due):
        """"""
        self.document["documents"]["due_dttm"] = due
        return self

    def set_start_dttm(self, start):
        """"""
        self.document["documents"]["start_dttm"] = start
        return self

    def set_complete_dttm(self, complete):
        """"""
        self.document["documents"]["complete_dttm"] = complete
        return self

    def set_etc_tm(self, etc):
        """"""
        self.document["documents"]["etc_tm"] = etc
        return self

    def set_parent(self, parent):
        """"""
        self.document["documents"]["parent"] = parent
        return self

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeWork(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).override("PyfficeWork")
        super().__init__(self.config)
        self.config.override(cfg)

    def create_new_document(self, name):
        """"""
        super().create_new_document(name, "work")
        self.document["document"] = {
            "ets_tm": None,
            "work_ltxt": None,
            "effort_txt": None,
            "issues_txt": None,
            "etc_tm": None,
        }

    def set_ets_tm(self, ets):
        """"""
        self.document["document"]["ets_tm"] = ets
        return self

    def set_work_ltxt(self, work):
        """"""
        self.document["document"]["work_ltxt"] = work
        return self

    def set_effort_txt(self, effort):
        """"""
        self.document["document"]["effort_txt"] = effort
        return self

    def set_issues_txt(self, issues):
        """"""
        self.document["document"]["issues_txt"] = issues
        return self

    def set_etc_tm(self, etc):
        """"""
        self.document["document"]["etc_tm"] = etc
        return self

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||


class PyfficeTask(PyfficeUnit):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeTask")).override(cfg)
        self.action_verb_noun = None
        self.complete_dttm = None
        self.due_dttm = None
        self.start_dttm = None
        self.work = None
        name = None
        details = None
        cfg = None
        self.action = AXN(name, details, cfg)

    def load_unit(self, unit):
        """"""
        logma.info(f"Load Unit {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        self.set_action_verb_noun(unit.get("action_verb_noun", None))
        self.set_complete_dttm(unit.get("complete_dttm", None))
        self.set_due_dttm(unit.get("due_dttm", None))
        self.set_start_dttm(unit.get("start_dttm", None))
        self.set_work(unit.get("work", None))
        return self

    def set_action_verb_noun(self, text):
        """"""
        if text != self.text:
            self.add_change("text", self.action_verb_noun, text)
            self.action_verb_noun = text
        return self

    def set_complete_dttm(self, complete_dttm):
        """"""
        if complete_dttm != self.complete_dttm:
            self.add_change("complete_dttm", self.complete_dttm, complete_dttm)
            self.complete_dttm = complete_dttm
        return self

    def set_due_dttm(self, due_dttm):
        """"""
        if due_dttm != self.due_dttm:
            self.add_change("due_dttm", self.due_dttm, due_dttm)
            self.due_dttm = due_dttm
        return self

    def set_start_dttm(self, start_dttm):
        """"""
        if start_dttm != self.start_dttm:
            self.add_change("start_dttm", self.start_dttm, start_dttm)
            self.start_dttm = start_dttm
        return self

    def set_work(self, work):
        """"""
        if work != self.work:
            self.add_change("work", self.work, work)
            self.work = work
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"]["action_verb_noun"] = self.action_verb_noun
        doc["unit"]["due_dttm"] = self.due_dttm
        doc["unit"]["start_dttm"] = self.start_dttm
        doc["unit"]["work"] = self.work
        doc["unit"]["complete_dttm"] = self.complete_dttm
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
