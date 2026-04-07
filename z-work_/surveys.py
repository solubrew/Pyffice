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
from ogma.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "surveys.yaml")


class PyfficeResponse(PyfficeDocument):
    """
    PyfficeResponse is a subclass of PyfficeDocument that provides a structure for managing form responses.

    Methods:
        __init__(self, form_id, cfg=None):
            Initializes a PyfficeResponse instance with the given form ID and optional configuration.

        add_answer(self, question_id, answer):
            Adds an answer to the form response by associating it with a specific question ID.
    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, form_id, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).override("")
        super().__init__(self)
        self.config.override(cfg)

    def add_answer(self, question_id, answer):
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


class PyfficeSurvey(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).override("PyfficeSurvey")
        super().__init__(self.config)
        self.config.override(cfg)


class PyfficeSurveyManager(PyfficeDocumentManager):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).override("PyfficeSurveyManager")
        super().__init__(self.config)
        self.config.override(cfg)
        self.surveys = {}
        self.active_survey = None
        self.questions_layout = None
        self.question_layout = None

    def add_question(self):
        """"""

    def create_survey(self):
        """"""

    def select_question(self):
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


class PyfficeSurveyManager(PyfficeDocumentManager):
    """
    Manages the creation, distribution and service used in surveys. Allowing the selection between Google Forms,
    YouForm and PyfficeForms.

    additionally allow for creating surveys on sites like X and incorporating results into survey

    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeSurveyManager")
        super().__init__()
        self.config.override(cfg)
        self.recipients = []
        self.form = None
        self.responses = []

    def clear_responses(self):
        """"""
        self.responses = []

    def distribute_survey(self, recipients):
        """distribute survey to a list of specific recipients or posting locations"""

    def schedule_survey_send(self, date_, time_):
        """"""
        return self

    def send_survey(self, recipient):
        """send survey to a specific recipient"""

    def set_end_date(self):
        """"""
        return self

    def set_form(self, form_id):
        """"""
        self.form_id = form_id
        self.form = self.get_document(form_id)

    def set_start_date(self):
        """"""
        return self

    def post_survey(self, location):
        """Post the survey to an online social media or blog site"""

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
