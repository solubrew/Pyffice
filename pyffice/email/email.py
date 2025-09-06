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
pxcfg = join(here, "_data_", "email.yaml")


class PyfficeEmailMessage(PyfficeDocument):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("PyfficeEmailDocument")
        super().__init__()
        self.config.override(cfg)

    def add_bcc(self, bcc):
        """"""

    def add_cc(self, cc):
        """"""

    def add_recipient(self):
        """"""

    def add_label(self):
        """"""
        return self

    def create_new_document(self, name):
        """"""
        super().create_new_document(name, "mail")
        self.document["document"] = {
            "from": [],
            "to": [],
            "cc": [],
            "bcc": [],
            "subject": None,
            "body": None,
            "attachments": None,
            "extracts": None,
            "tags": None,
            "status": None,
        }

    def get_body(self):
        """"""

    def get_footer(self):
        """"""

    def get_header(self):
        """"""

    def get_recipient(self):
        """"""

    def get_sender(self):
        """"""

    def load_document(self, document):
        """"""
        super().load_document(document)
        return self

    def open_file(self, document):
        """"""

    def save_message(self):
        """"""
        return self

    def remove_label(self):
        """"""
        return self


class PyfficeMailBox(PyfficeDocumentManager):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeMailBoxAccount")).override(cfg)
        self.active_message = None
        self.messages = []

    def connect_service(self):
        """Subclass must implement this method."""

    def create_label(self):
        """"""

    def create_message(self):
        """"""
        self.active_message = PyfficeEmailMessage()

    def create_new_document(self, name):
        """"""
        super().create_new_document(name, "manager")
        self.document["document"] = {"name": None, "address": None, "messages": []}

    def create_rule(self):
        """"""

    def destroy_label(self):
        """"""

    def delete_mail(self):
        """"""

    def delete_rule(self):
        """"""

    def disconnect_service(self):
        """"""

    def get_mail(self):
        """"""

    def get_message(self):
        """"""

    def get_labels(self):
        """"""

    def get_messages(self):
        """"""

    def get_message(self):
        """"""

    def get_rule(self):
        """"""

    def get_rules(self):
        """"""

    def process_rules(self):
        """"""

    def send_mail(self):
        """"""

    def send_message(self):
        """"""
        return self

    def store_mail(self):
        """"""

    def write_message(self, subject, body, recipients=None):
        """"""
        self.active_message.add_subject(subject)
        self.active_message.add_body(body)
        if recipients:
            for recipient in recipients:
                self.active_message.add_recipient(recipient)
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
