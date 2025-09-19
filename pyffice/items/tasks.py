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
from condor import condor
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "tasks.yaml")


class PyfficeRecurrenceManager(PyfficeDocumentManager):
    """Extract recurrence information from tasks and then store them in a structure for later retrevial and reprocessing"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).override("")
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

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeTaskManager")
        super().__init__(self.config)
        self.config.override(cfg)
        self.init_tasks_manager()

    def add_task(self, name):
        """"""
        # self.documents.append(PyfficeProject(name))


class PyfficeProject(PyfficeTasksManager):
    """A Project Manages Tasks"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeProject")
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

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeProject")
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

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeTask")
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

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).override("PyfficeWork")
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
