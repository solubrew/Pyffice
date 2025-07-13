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
from pyffice.document import PyfficeUnit, PyfficeDocumentManager
from subtrix.subtrix import uuid
from pyffice.web.web import PyfficeWebBrowser
from pyffice.items.text import PyfficeText

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "prompts.yaml")


class PyfficePrompt(PyfficeUnit):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficePrompt")).override(cfg)
        self.file_type = "prompt"
        self.context = None
        self.context_metrics = None
        self.input = None
        self.input_metrics = None
        self.prompt = None
        self.prompt_metrics = None
        self.response = None
        self.response_metrics = None

    def get_metrics(self):
        """"""
        metrics = {}
        return metrics

    def load_unit(self, unit=None):
        """"""
        logma.info(f"Load Document {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        self.set_context(unit.get("context", ""))
        self.set_input(unit.get("input", ""))
        self.set_prompt(unit.get("prompt", ""))
        self.set_response(unit.get("responses", []))
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

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"] = {
            "context": self.context.to_dict(),
            "prompt": self.prompt.to_dict(),
            "response": self.response.to_dict(),
        }
        doc["unit"]["context"]["metrics"] = self.context.get_metrics()
        doc["unit"]["prompt"]["metrics"] = self.prompt.get_metrics()
        doc["unit"]["response"]["metrics"] = self.response.get_metrics()
        return doc


class PyfficePromptsManager(PyfficeDocumentManager):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficePromptsManager")).override(cfg)
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
