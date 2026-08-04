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
from pyffice.document import PyfficeDocument
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "pyffice.yaml")


class PyfficeConfig(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None, parent=None) -> None:
        """"""
        self.parent = parent
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeConfig").override(cfg))

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
        return self

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "config" in content:
                setattr(self, "config", content["config"])
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
        logma.debug(f"{self.__class__.__name__}.to_dict called")
        super().to_dict()  # populate canonical envelope
        attrs = {
            "config": getattr(self, "config", None),
        }
        doc = {
            "did": self.did,
            "meta_data": {"schema_version": list(self.SERIALIZATION_VERSION)},
            "data": {
                "content": attrs,
                "document_type": "slide",
            },
        }
        return self._canonicalize(doc)


class PyfficeTOML(PyfficeConfig):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).override("PyfficeTOML")).override(cfg)

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "config" in content:
                setattr(self, "config", content["config"])
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
        logma.debug(f"{self.__class__.__name__}.to_dict called")
        super().to_dict()  # populate canonical envelope
        attrs = {
            "config": getattr(self, "config", None),
        }
        doc = {
            "did": self.did,
            "meta_data": {"schema_version": list(self.SERIALIZATION_VERSION)},
            "data": {
                "content": attrs,
                "document_type": "slide",
            },
        }
        return self._canonicalize(doc)


class PyfficeHelp(PyfficeConfig):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeHelp")).override(cfg)

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "config" in content:
                setattr(self, "config", content["config"])
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
        logma.debug(f"{self.__class__.__name__}.to_dict called")
        super().to_dict()  # populate canonical envelope
        attrs = {
            "config": getattr(self, "config", None),
        }
        doc = {
            "did": self.did,
            "meta_data": {"schema_version": list(self.SERIALIZATION_VERSION)},
            "data": {
                "content": attrs,
                "document_type": "slide",
            },
        }
        return self._canonicalize(doc)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
