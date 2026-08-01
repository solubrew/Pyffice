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
from typing import Any
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "prompts.yaml")


class PyfficeContext(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeContext")).override(cfg)

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "file_path" in content:
                setattr(self, "file_path", content["file_path"])
        return self

    def open_file(self, file_=None):
        import json as _json
        from os.path import exists
        if file_ is None:
            file_ = self.file_path
        if not file_ or not exists(file_):
            logma.warning(f"{self.__class__.__name__}.open_file: no such path {file_!r}")
            return self
        try:
            with open(file_, "r") as f:
                doc = _json.load(f)
        except (OSError, ValueError) as e:
            logma.warning(f"{self.__class__.__name__}.open_file failed for {file_!r}: {e}")
            return self
        return self.load_document(doc)

    def save(self, path=None, format_=None, encrypt=None):
        logma.debug(f"{self.__class__.__name__}.save called path={path!r}")
        super().save(path, format_, encrypt)
        if path is None:
            path = self.file_path
        if not path:
            logma.warning(f"{self.__class__.__name__}.save: no path available")
            return
        import json as _json
        doc = self.to_dict()
        with open(path, "w") as f:
            _json.dump(doc, f, indent=2, default=str)
        return

    def to_dict(self):
        # TODO implement method
        super().to_dict()
        return self


class PyfficePrompt(PyfficeDocument):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
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

    def get_metrics(self) -> Any:
        """Return the metrics.

        Returns:
            Self for chaining.
        """
        metrics = {}
        return metrics

    def load_document(self, document=None) -> Self:
        """Load document into this document.

        Args:
            document: Parameter.

        Returns:
            Self for chaining.
        """
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
        super().load_document(document)
        self.set_context(document.get("context", ""))
        self.set_input(document.get("input", ""))
        self.set_prompt(document.get("prompt", ""))
        self.set_response(document.get("responses", []))
        return self

    def set_context(self, context) -> Self:
        """Set the context.

        Args:
            context: Parameter.

        Returns:
            Self for chaining.
        """
        cfg = {"text": context}
        context = PyfficeText(cfg)
        if context != self.context:
            self.add_change("context", self.context, context)
            self.context = context
            self.context_metrics = {"tokens": len(context.to_string().split()), "characters": len(context.to_string())}
        return self

    def set_input(self, input) -> Self:
        """Set the input.

        Args:
            input: Parameter.

        Returns:
            Self for chaining.
        """
        cfg = {"text": input}
        input = PyfficeText(cfg)
        if input != self.input:
            self.add_change("input", self.input, input)
            self.input = input
            self.input_metrics = {"tokens": len(input.to_string().split()), "characters": len(input.to_string())}
        return self

    def set_persona(self, persona=0) -> Self:
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

    def set_prompt(self, prompt) -> Self:
        """Set the prompt.

        Args:
            prompt: Parameter.

        Returns:
            Self for chaining.
        """
        cfg = {"text": prompt}
        prompt = PyfficeText(cfg)
        if prompt != self.prompt:
            self.add_change("prompt", self.prompt, prompt)
            self.prompt = prompt
        return self

    def set_response(self, response) -> Self:
        """Set the response.

        Args:
            response: Parameter.

        Returns:
            Self for chaining.
        """
        cfg = {"text": response}
        response = PyfficeText(cfg)
        if response != self.response:
            self.add_change("response", self.response, response)
            self.response = response
        return self

    def set_response_scope(self, scope) -> Self:
        """Set the response scope.

        Args:
            scope: Parameter.

        Returns:
            Self for chaining.
        """
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

    def set_topic(self, topic) -> Self:
        """Set the topic.

        Args:
            topic: Parameter.

        Returns:
            Self for chaining.
        """
        if topic != self.topic:
            self.add_change("topic", self.topic, topic)
            self.topic = topic
        return self

    def to_dict(self) -> Self:
        """Convert this document to dict.

        Returns:
            Self for chaining.
        """
        doc = super().to_dict()
        doc["data"] = {
            "context": {},
            "input": {},
            "response": {},
        }
        doc["data"]["context"]["metrics"] = self.context.get_metrics()
        doc["data"]["prompt"]["metrics"] = self.prompt.get_metrics()
        doc["data"]["response"]["metrics"] = self.response.get_metrics()
        return self._canonicalize(doc)


class PyfficeResponse(PyfficeDocument):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeResponse")).override(cfg)

    def add_source(self) -> Self:
        """Add a source."""
        _p = True  # placeholder
        return self

    def load_document(self, document=None) -> Self:
        """Load document."""
        _p = True  # placeholder
        return self

    def set_sources(self, sources) -> Self:
        """Set the sources.

        Args:
            sources: Parameter.

        Returns:
            Self for chaining.
        """
        if sources != self.sources:
            self.add_change("sources", self.sources, sources)
            self.sources = sources
        return self


class PyfficePromptsManager(PyfficeDocumentManager):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficePromptsManager.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePromptsManager")).override(cfg)
        self.active_service = None
        self.services = None
        self.browser_left = None
        self.browser_right = None
        self.prompts = None
        self.responses = None

    def add_prompt(self, input=None, context=None, tags=None) -> Self:
        """Add a prompt.

        Args:
            input: Parameter.
            context: Parameter.
            tags: Parameter.

        Returns:
            Self for chaining.
        """
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

    def add_prompt_response(self, text, service, metrics=None, prompt=None) -> Self:
        """Add a prompt response.

        Args:
            text: Parameter.
            service: Parameter.
            metrics: Parameter.
            prompt: Parameter.

        Returns:
            Self for chaining.
        """
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

    def add_prompt(self, prompt) -> Self:
        """Add a prompt.

        Args:
            prompt: Parameter.

        Returns:
            Self for chaining.
        """
        cfg = {"prompt": prompt}
        prompt = PyfficePrompt(cfg)
        self.add_change("prompts", self.prompts, prompt)
        self.prompts.append(prompt)
        return self

    def add_service(self, service, metrics, model) -> Self:
        """Add a service.

        Args:
            service: Parameter.
            metrics: Parameter.
            model: Parameter.

        Returns:
            Self for chaining.
        """
        service = {"service": service, "metrics": metrics, "model": model}
        self.active_service = service
        self.document["document"]["services"].append(service)
        return self

    def load_document(self, document=None) -> Self:
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
        self.set_prompts(document.get("prompts", None))
        self.set_services(document.get("services", None))
        self.set_service_active(document.get("active_service", None))
        return self

    def set_browser_left(self, browser) -> Self:
        """Set the browser left.

        Args:
            browser: Parameter.

        Returns:
            Self for chaining.
        """
        cfg = {"browser": browser}
        self.browser_left = PyfficeWebBrowser(cfg)
        return self

    def set_browser_right(self, browser) -> Self:
        """Set the browser right.

        Args:
            browser: Parameter.

        Returns:
            Self for chaining.
        """
        cfg = {"browser": browser}
        self.browser_right = PyfficeWebBrowser(cfg)
        return self

    def set_service_active(self, service) -> Self:
        """Set the service active.

        Args:
            service: Parameter.

        Returns:
            Self for chaining.
        """
        if service != self.active_service:
            self.add_change("active_service", self.active_service, service)
            self.active_service = service
            if service not in self.services:
                self.services.append(service)
        return self

    def set_services(self, services) -> Self:
        """Set the services.

        Args:
            services: Parameter.

        Returns:
            Self for chaining.
        """
        if services is None:
            services = []
        if services != self.services:
            self.add_change("services", self.services, services)
            self.services = services
        return self

    def set_prompts(self, prompts) -> Self:
        """Set the prompts.

        Args:
            prompts: Parameter.

        Returns:
            Self for chaining.
        """
        if prompts is None:
            prompts = []
        if prompts != self.prompts:
            self.add_change("prompts", self.prompts, prompts)
            self.prompts = prompts
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
