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
from os.path import abspath, dirname, join, expanduser
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor, utils
from ogma.logma import Logma
from squirl.objnql import txtonql
from squirl.orgnql import conql, yonql
from pyffice.analytics.sources import PyfficeDataSet, PyfficeDataView, PyfficeSources
from pyffice.calendars.calendars import PyfficeCalendar
from pyffice.charts.charts import PyfficeChart
from pyffice.config.ports import PyfficePortCherryTree
from pyffice.contacts.contacts import PyfficeRolodex
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from pyffice.forms.forms import PyfficeForm, PyfficeFormsManager
from pyffice.images.images import PyfficeImage
from pyffice.diagrams.diagrams import PyfficeSketch
from pyffice.images.pdfs import PyfficePDF
from pyffice.notebooks.notebooks import PyfficeNotebook
from pyffice.spreadsheet.spreadsheet import PyfficeMatrix
from pyffice.text.text import PyfficeScript
from pyffice.web.prompts import PyfficePromptsManager
from pyffice.web.url import PyfficeURLLibrary
from pyffice.web.web import PyfficeWebBrowser, PyfficeWebPage
from pyffice.filesystems.filesystems import PyfficeFileSystem

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "pyffice.yaml")


class PyfficeCodex(PyfficeDocumentManager):
    """A Pyffice Book is a container that can hold multiple instances and types of Pyffice Top Level Documents"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeCodex")).override(cfg)
        cfg = {}
        self.url_library = PyfficeURLLibrary(cfg)
        self.contacts = None
        self.documents = None
        self.forms_manager = None
        self.imports = None

    def add_pydocument(self, pydoc):
        """"""
        if isinstance(pydoc, str):
            pydoc = self.load_pydocument(pydoc)
        self.documents.append(pydoc)

    def add_url(self, url):
        """"""
        id = self.url_library.add_url(url)
        return id

    def get_url(self, url_id=None):
        """"""
        return self.url_library.get_url_by_id(url_id)

    def import_cherrytree(self, cfg):
        """"""
        logma.info(f"CFG {cfg}")
        cherrytree = PyfficePortCherryTree(cfg)
        logma.info(f"CherryTree: {cherrytree.file_path}")
        import_doc = cherrytree.file_import()
        cherrytree.file_export(join(expanduser("~"), "_work", "cherrytree.yaml"))
        self.imports[cherrytree.did] = import_doc
        return cherrytree

    def import_pdf(self, cfg):
        """"""

    def import_session(self, cfg):
        """"""

    def import_text(self, cfg):
        """"""

    def init_browser(self, cfg):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        browser = PyfficeWebBrowser(cfg)
        # browser.profile_manager.add_profiles(self.contacts.get_group_by_name("profiles"))
        self.documents[browser.did] = browser
        return browser

    def init_calendar(self, cfg):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        calendar = PyfficeCalendar(cfg)
        self.documents[calendar.did] = calendar
        return calendar

    def init_chart(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        chart = PyfficeChart(cfg)
        self.documents[chart.did] = chart
        return chart

    def init_contacts(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        self.contacts = PyfficeRolodex(cfg)
        self.documents[self.contacts.did] = self.contacts
        return self.contacts

    def init_files(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        files = PyfficeFileSystem(cfg)
        self.documents[files.did] = files
        return files

    def init_form(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        form = self.forms_manager.create_new_form(cfg)
        self.documents[form.did] = form
        return form

    def init_forms_manager(self, cfg):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        self.forms_manager = PyfficeFormsManager(cfg)
        self.documents[self.forms_manager.did] = self.forms_manager
        return self.forms_manager

    def init_image(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        image = PyfficeImage(cfg)
        self.documents[image.did] = image
        return image

    def init_matrix(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        matrix = PyfficeMatrix(cfg)
        self.documents[matrix.did] = matrix
        return matrix

    def init_note(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        note = PyfficeScript(cfg)
        self.documents[note.did] = note
        return note

    def init_notebook(self):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        notebook = PyfficeNotebook()
        self.documents[notebook.did] = notebook
        return notebook

    def init_pdf(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        pdf = PyfficePDF(cfg)
        self.documents[pdf.did] = pdf
        return pdf

    def init_prompt(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        prompts = PyfficePromptsManager(cfg)
        self.documents[prompts.did] = prompts
        return prompts

    def init_script(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        script = PyfficeScript(cfg)
        self.documents[script.did] = script
        return script

    # def init_settings(self, cfg):
    #     """"""
    #     if cfg is None:
    #         cfg = {}
    #     settings = PyfficeApplicationConfig(cfg)
    #     self.documents[settings.did] = settings
    #     return settings

    def init_sketch(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        sketch = PyfficeSketch(cfg)
        self.documents[sketch.did] = sketch
        return sketch

    def init_source_manager(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        self.source_manager = PyfficeSources(cfg)
        self.documents[self.source_manager.did] = self.source_manager
        return self.source_manager

    def init_source(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["codex"] = self
        self.source = self.source_manager.create_new_source(cfg)
        self.documents[self.source.did] = self.source
        return self.source

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        # lookup and initialize the proper Pyffice Document type
        self.set_documents(document.get("documents", {}))
        self.set_imports(document.get("imports", {}))
        return document

    def save(self, path=None, syntax=None, encrypt_key=None):
        """"""
        return self

    def set_imports(self, imports):
        """"""
        if imports is None:
            imports = {}
        if imports != self.imports:
            self.add_change("imports", self.imports, imports)
            self.imports = imports
        return self

    def set_storage(self):
        """
        set storage location for the book.  This can be either a folder
        where documents and configurations will be stored as files or a database
        :return:
        """


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
