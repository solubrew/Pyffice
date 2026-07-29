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
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from subtrix.utilities import uuid
from pyffice.web.web import PyfficeWebBrowser
from pyffice.items.text import PyfficeText

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "prompts.yaml")


class PyfficeContext(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeContext")).override(cfg)


class PyfficePrompt(PyfficeDocument):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePrompt")).override(cfg)
        self.file_type = "prompt"
        self.context = None
        self.context_metrics = None
        self.input = None
        self.input_metrics = None
        self.prompt = None
        self.prompt_metrics = None
        self.response = None
        self.response_metrics = None
        self.response_scope = None
        self.persona = None
        self.scope = None
        self.topic = None

    def get_metrics(self):
        """"""
        metrics = {}
        return metrics

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
        super().load_document(document)
        self.set_context(document.get("context", ""))
        self.set_input(document.get("input", ""))
        self.set_prompt(document.get("prompt", ""))
        self.set_response(document.get("responses", []))
        return self

    def set_context(self, context):
        """"""
        cfg = {"text": context}
        context = PyfficeText(cfg)
        if context != self.context:
            self.add_change("context", self.context, context)
            self.context = context
            self.context_metrics = {"tokens": len(context.to_string().split()), "characters": len(context.to_string())}
        return self

    def set_input(self, input):
        """"""
        cfg = {"text": input}
        input = PyfficeText(cfg)
        if input != self.input:
            self.add_change("input", self.input, input)
            self.input = input
            self.input_metrics = {"tokens": len(input.to_string().split()), "characters": len(input.to_string())}
        return self

    def set_persona(self, persona=0):
        """How to define and organize personas: https://www.personality-is-graph.com/"""
        personas = [
            "teacher",
            "plumber",
            "electrician",
            "doctor",
            "lawyer",
            "psychologist",
            "engineer",
            "mathematician",
            "historian",
            "empath",
            "psychopath",
            "socialite",
            "sociopath",
            "marketer",
            "nurse",
            "narcissist",
            "pessimist",
            "optimist",
            "realist",
            "opportunist",
            "friend",
            "enemy",
            "stranger",
            "acquaintance",
            "frenemy",
            "philosopher",
            "researcher",
            "intern",
            "student",
            "industrialist",
        ]
        persona = personas[self.config.dikt.get("persona", persona)]
        if persona != self.persona:
            self.add_change("persona", self.persona, persona)
            self.persona = persona
        return self

    def set_prompt(self, prompt):
        """"""
        cfg = {"text": prompt}
        prompt = PyfficeText(cfg)
        if prompt != self.prompt:
            self.add_change("prompt", self.prompt, prompt)
            self.prompt = prompt
        return self

    def set_response(self, response):
        """"""
        cfg = {"text": response}
        response = PyfficeText(cfg)
        if response != self.response:
            self.add_change("response", self.response, response)
            self.response = response
        return self

    def set_response_scope(self, scope):
        """"""
        if scope != self.scope:
            self.scope = scope
            self.add_change("scope", self.scope, scope)
        else:
            return self
        if scope == "conversational":
            response_scope = "Respond to the given input in a conversational manner."
            if "teacher" in self.persona:
                response_scope += " As a teacher, explain concepts brought up in the conversation."
        elif scope == "diagnostic":
            response_scope = "Provide a diagnostic of the given input."
            if "mechanic" in self.persona:
                response_scope += " Provide a diagnostic of the given input."
            elif "engineer" in self.persona:
                response_scope += " Provide a diagnostic of the given input."
        elif scope == "analytic":
            match self.persona:
                case _:
                    response_scope = "Provide an analytic of the given input."
        elif scope == "explanation":
            match self.persona:
                case _:
                    response_scope = "Provide an explanation of the given input. Detailing the main points in bullet points summaries"
        elif scope == "question":
            match self.persona:
                case _:
                    response_scope = (
                        "Provide the best possible answer to the given input exploring counter points briefly"
                    )
        elif scope == "recommendation":
            match self.persona:
                case _:
                    response_scope = "Provide a recommendation for the given input."
        else:
            match self.persona:
                case _:
                    response_scope = "Respond to the given input."
        self.response_scope = response_scope
        return self

    def set_topic(self, topic):
        """"""
        if topic != self.topic:
            self.add_change("topic", self.topic, topic)
            self.topic = topic
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["data"] = {
            "context": {},
            "input": {},
            "response": {},
        }
        doc["data"]["context"]["metrics"] = self.context.get_metrics()
        doc["data"]["prompt"]["metrics"] = self.prompt.get_metrics()
        doc["data"]["response"]["metrics"] = self.response.get_metrics()
        return doc


class PyfficeResponse(PyfficeDocument):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeResponse")).override(cfg)

    def add_source(self):
        """"""

    def load_document(self, document=None):
        """"""

    def set_sources(self, sources):
        """"""
        if sources != self.sources:
            self.add_change("sources", self.sources, sources)
            self.sources = sources
        return self


class PyfficePromptsManager(PyfficeDocumentManager):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePromptsManager")).override(cfg)
        self.active_service = None
        self.services = None
        self.browser_left = None
        self.browser_right = None
        self.prompts = None
        self.responses = None

    def add_prompt(self, input=None, context=None, tags=None):
        """"""
        now = dt.datetime.now()
        prompt = {
            "datetime": now,
            "tags": tags,
            "context": {"text": context, "metrics": {}},
            "input": {"datetime": None, "text": input, "metrics": {}},
            "responses": [],
        }
        self.active_prompt = prompt
        self.prompt = prompt
        return self

    def add_prompt_response(self, text, service, metrics=None, prompt=None):
        """"""
        now = dt.datetime.now()
        response = {
            "text": text,
            "datetime": now,
            "service": service,
            "uuid": uuid(),
            "metrics": {
                "tokens": len(text.split()),
                "characters": len(text),
                "rating": metrics["rating"],
            },
        }
        self.response = response
        return self

    def add_prompt(self, prompt):
        """"""
        cfg = {"prompt": prompt}
        prompt = PyfficePrompt(cfg)
        self.add_change("prompts", self.prompts, prompt)
        self.prompts.append(prompt)
        return self

    def add_service(self, service, metrics, model):
        """"""
        service = {"service": service, "metrics": metrics, "model": model}
        self.active_service = service
        self.document["document"]["services"].append(service)
        return self

    def load_document(self, document=None):
        """"""
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_prompts(document.get("prompts", None))
        self.set_services(document.get("services", None))
        self.set_service_active(document.get("active_service", None))
        return self

    def set_browser_left(self, browser):
        """"""
        cfg = {"browser": browser}
        self.browser_left = PyfficeWebBrowser(cfg)
        return self

    def set_browser_right(self, browser):
        """"""
        cfg = {"browser": browser}
        self.browser_right = PyfficeWebBrowser(cfg)
        return self

    def set_service_active(self, service):
        """"""
        if service != self.active_service:
            self.add_change("active_service", self.active_service, service)
            self.active_service = service
            if service not in self.services:
                self.services.append(service)
        return self

    def set_services(self, services):
        """"""
        if services is None:
            services = []
        if services != self.services:
            self.add_change("services", self.services, services)
            self.services = services
        return self

    def set_prompts(self, prompts):
        """"""
        if prompts is None:
            prompts = []
        if prompts != self.prompts:
            self.add_change("prompts", self.prompts, prompts)
            self.prompts = prompts
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["documents"] = {"services": self.services, "prompts": [x.to_dict() for x in self.prompts]}
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
