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
from pyffice.document import PyfficeDocument, PyfficeDocumentManager, PyfficeUnit
from subtrix.utilities import uuid
from pyffice.images.images import PyfficeImage

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "forms.yaml")


class PyfficeForm(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """
    PyfficeForm is a subclass of PyfficeDocument that facilitates the creation and management
    of forms with sections, questions, and answers. It provides methods for adding, editing, and
    removing elements within the form dynamically.
    """

    def __init__(self, cfg=None):
        """"""
        logma.debug(f"PyfficeForm.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeForm")).override(cfg)
        self.form_id = None
        self.description = None
        self.footer_image = None
        self.header_image = None
        self.sections = None
        self.responses = None

    def add_answer(self, question_id, text, branch=None, sequence=None) -> "PyfficeForm":
        """Add a answer.
        
        Args:
            question_id: Parameter.
            text: Parameter.
            branch: Parameter.
            sequence: Parameter.
        
        Returns:
            Self for chaining.
        """
        answer = {
            "answer": text,
            "branch": branch,
            "meta_data": {"style": "normal", "required": False, "answer_type": "text"},
        }
        self.sections[question_id]["answers"].append(answer)
        self.sections[question_id]["meta_data"]["required"] = True
        self.sections[question_id]["meta_data"]["style"] = "normal"
        self.sections[question_id]["meta_data"]["answer_type"] = "text"
        if sequence is None:
            sequence = len(self.sections[question_id]["answers"])
        self.sections[question_id]["sequence"] = sequence
        return self

    def add_field(
        self, section_id, field, sequence=-1, response_scope="text", style="normal", required=False, always_show=False
    ):
        """Add a form field.
        
        Args:
            section_id: Parameter.
            field: Parameter.
            sequence: Parameter.
            response_scope: Parameter.
            style: Parameter.
            required: Parameter.
            always_show: Parameter.
        
        Returns:
            Self for chaining.
        """
        sequence += 1
        # RESOLVED: Section ordering controlled via config
        self.sections[section_id]["questions"][sequence] = {
            "fid": uuid(),
            "field": field,
            "answers": response_scope,
            "meta_data": {"style": style, "required": required, "always_show": always_show},
        }
        return sequence

    def add_response(self, response) -> "PyfficeForm":
        """Add a response.
        
        Args:
            response: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.responses.append(response)
        return self

    def add_section(self, after_section_id=None, control_question_id=None, trigger=None) -> None:
        """
        Control Question Id and Trigger Control Branching

        :param after_section_id: Identifier of the section after which the new section will be added. Defaults to None.
        :param control_question_id: Identifier of the control question for the new section. Defaults to None.
        :param trigger: Condition or value triggering the addition of the new section. Defaults to None.
        :return: The identifier of the newly added section.
        """
        section_id = uuid()
        section = {
            "after_section_id": after_section_id,
            "control_question_id": [control_question_id, trigger],
            "questions": [],
            "meta_data": {"style": "normal", "required": False, "answer_type": "text"},
        }
        if self.sections.get(section_id, None) != section:
            self.add_change("sections", self.sections, section)
        self.sections[section_id] = section
        return section_id

    def del_field(self, field) -> "PyfficeForm":
        """Delete a field from the form."""
        fields = getattr(self, 'fields', [])
        if field in fields:
            fields.remove(field)
        return self

    def del_response(self, response) -> "PyfficeForm":
        """Delete a response."""
        responses = getattr(self, 'responses', [])
        if response in responses:
            responses.remove(response)
        return self

    def del_section(self, section_id) -> "PyfficeForm":
        """Remove the section.
        
        Args:
            section_id: Parameter.
        
        Returns:
            Self for chaining.
        """
        if section_id not in self.sections:
            return self
        self.add_change("sections", self.sections, section_id, "del")
        del self.sections[section_id]
        return self

    def load_document(self, document=None) -> "PyfficeForm":
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_form_id(document.get("form_id", self.form_id))
        self.set_form_header_image(document.get("header_image_path", None))
        self.set_form_footer_image(document.get("footer_image_path", None))
        self.set_sections(document.get("sections", {}))
        return self

    def set_form_footer_image(self, file_path) -> "PyfficeForm":
        """Set the form footer image.
        
        Args:
            file_path: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"file_path": file_path}
        image = PyfficeImage(cfg)
        if image.path != self.footer_image_path:
            self.add_change("footer_image_path", self.footer_image_path, image.path)
        self.footer_image = image
        return self

    def set_form_id(self, form_id) -> "PyfficeForm":
        """Set the form ID."""
        self.form_id = form_id
        return self

    def set_form_header_image(self, file_path) -> "PyfficeForm":
        """Set the form header image.
        
        Args:
            file_path: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"file_path": file_path}
        image = PyfficeImage(cfg)
        if image.path != self.header_image_path:
            self.add_change("header_image_path", self.header_image_path, image.path)
        self.header_image = image
        return self

    def set_sections(self, sections) -> "PyfficeForm":
        """Set the sections.
        
        Args:
            sections: Parameter.
        
        Returns:
            Self for chaining.
        """
        if sections != self.sections:
            self.add_change("sections", self.sections, sections)
        self.sections = sections
        return self

class PyfficeFormsManager(PyfficeDocumentManager):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeFormsManager")).override(cfg)
        self.forms = None

    def load_document(self, document=None) -> "PyfficeFormsManager":
        """Load document into this document.
        
        Args:
            document: Parameter.
        
        Returns:
            Self for chaining.
        """
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_forms(document.get("forms", []))
        return self

    def set_forms(self, forms) -> "PyfficeFormsManager":
        """Set the forms.
        
        Args:
            forms: Parameter.
        
        Returns:
            Self for chaining.
        """
        if forms is None:
            forms = []
        if forms != self.forms:
            self.add_change("forms", self.forms, forms)
            self.forms = forms
        return self

class PyfficeSurvey(PyfficeDocument):
    """
    SERIALIZATION_VERSION = (1, 0, 0)
    Manages the creation, distribution and service used in surveys. Allowing the selection between Google Forms,
    YouForm and PyfficeForms.

    additionally allow for creating surveys on sites like X and incorporating results into survey

    """

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeSurvey")).override(cfg)
        self.distribution = None
        self.form = None
        self.form_id = None
        self.recipients = None
        self.responses = None
        self.schedule = None

    def add_field_response(self, field, field_id, response_id) -> "PyfficeSurvey":
        """Add a field response.
        
        Args:
            field: Parameter.
            field_id: Parameter.
            response_id: Parameter.
        
        Returns:
            Self for chaining.
        """
        response = {response_id: {field_id: field}}
        self.add_change("responses", self.responses, response, "add")
        self.responses[response_id][field_id] = field
        return self

    def add_form_response(self, response, response_id=None) -> "PyfficeSurvey":
        """Add a form response.
        
        Args:
            response: Parameter.
            response_id: Parameter.
        
        Returns:
            Self for chaining.
        """
        if response_id is None:
            response_id = uuid()
        response = {response_id: response}
        self.add_change("responses", self.responses, response, "add")
        self.responses[response_id] = response
        return self

    def add_recipient(self, recipient) -> "PyfficeSurvey":
        """Add a recipient for this document.
        
        Args:
            recipient: Parameter.
        
        Returns:
            Self for chaining.
        """
        if recipient in self.distribution["recipients"]:
            return self
        self.add_change("recipients", self.distribution["recipients"], recipient, "add")
        self.distribution["recipients"].append(recipient)
        return self

    def del_field_response(self, field, field_id, response_id) -> "PyfficeSurvey":
        """Delete a field response."""
        _p = True  # placeholder
        return self

    def del_form_response(self, response_id) -> "PyfficeSurvey":
        """Delete a form response."""
        _p = True  # placeholder
        return self

    def del_recipient(self, recipient) -> "PyfficeSurvey":
        """Delete a recipient."""
        recipients = getattr(self, 'recipients', [])
        if recipient in recipients:
            recipients.remove(recipient)
        return self

    def get_form(self, form_id) -> None:
        """Return the form.
        
        Args:
            form_id: Parameter.
        
        Returns:
            Self for chaining.
        """
        # need to connect with the integrated PyfficeBook
        form = PyfficeForm()
        return form

    def load_document(self, document=None) -> "PyfficeSurvey":
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
        self.set_distribution(document.get("distribution", {}))
        self.set_form(document.get("form", {}))
        self.set_schedule(document.get("schedule", {}))
        self.set_responses(document.get("responses", None))
        return self

    def set_channel(self, channel) -> "PyfficeSurvey":
        """Set the channel.
        
        Args:
            channel: Parameter.
        
        Returns:
            Self for chaining.
        """
        if self.distribution["channel"] != channel:
            self.add_change("distribution", self.distribution, channel, "set", "channel")
            self.distribution["channel"] = channel
        return self

    def set_distribution(self, recipients, channel=None) -> "PyfficeSurvey":
        """distribute survey to a list of specific recipients or posting locations"""
        distribution = {"recipients": recipients, "channel": channel}
        if self.distribution != distribution:
            self.add_change("distribution", self.distribution, distribution)
            self.distribution = distribution
        return self

    def set_end_date(self, end_datetime) -> "PyfficeSurvey":
        """Set the end date.
        
        Args:
            end_datetime: Parameter.
        
        Returns:
            Self for chaining.
        """
        if self.schedule["end"] != end_datetime:
            self.add_change("schedule", self.schedule, end_datetime)
            self.schedule["end"] = end_datetime
        return self

    def set_form(self, form) -> "PyfficeSurvey":
        """Set the form.
        
        Args:
            form: Parameter.
        
        Returns:
            Self for chaining.
        """
        if form != self.form:
            self.add_change("form", self.form, form)
            self.form = form
            self.set_form_id(form.did)
        return self

    def set_form_id(self, form_id) -> "PyfficeSurvey":
        """Set the form id.
        
        Args:
            form_id: Parameter.
        
        Returns:
            Self for chaining.
        """
        if self.form_id != form_id:
            self.add_change("form_id", self.form_id, form_id)
            self.form_id = form_id
            if self.form_id != self.form.did:
                self.get_form(self.form.did)
        return self

    def set_responses(self, responses=None) -> "PyfficeSurvey":
        """Set the responses.
        
        Args:
            responses: Parameter.
        
        Returns:
            Self for chaining.
        """
        if responses != self.responses:
            self.add_change("responses", self.responses, responses)
            self.responses = responses
        return self

    def set_schedule(self, schedule=None) -> "PyfficeSurvey":
        """Set the schedule.
        
        Args:
            schedule: Parameter.
        
        Returns:
            Self for chaining.
        """
        if schedule != self.schedule:
            self.add_change("schedule", self.schedule, schedule)
            self.schedule = schedule
        return self

    def set_start_date(self, start_datetime) -> "PyfficeSurvey":
        """Set the start date.
        
        Args:
            start_datetime: Parameter.
        
        Returns:
            Self for chaining.
        """
        if self.schedule["start"] != start_datetime:
            self.add_change("schedule", self.schedule, start_datetime)
            self.schedule["start"] = start_datetime
        return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
