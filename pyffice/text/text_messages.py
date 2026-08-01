# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
            Implement a format that can be used to store messages for as many services/protocols as possible.
            email, sms, etc.
            connect through ports to get messages from things like slack, discord, etc.
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join, exists
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
pxcfg = join(here, "_data_", ".yaml")


class PyfficeMessage(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficeMessage.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeMessage")).override(cfg)

    def set_body(self, body) -> Self:
        """Set message body."""
        self.body = body
        return self

    def set_from(self, from_) -> Self:
        """Set sender."""
        self.from_ = from_
        return self

    def set_subject(self, subject) -> Self:
        """Set subject."""
        self.subject = subject
        return self

    def set_to(self, to) -> Self:
        """Set recipient."""
        self.to = to
        return self

    def to_dict(self) -> Self:
        """Convert to dictionary (additive canonical shape).

        The class-specific payload is wrapped under ``doc["data"]``;
        the canonical envelope (did, meta_data, schema_version,
        pyffice_compat) is built inline here and finalized by
        ``_canonicalize``. We avoid ``super().to_dict()`` for the
        reason in PyfficeProject.to_dict — the import chain is
        not available in the test environment.
        """
        doc = {
            "did": self.did,
            "meta_data": {"schema_version": list(self.SERIALIZATION_VERSION)},
            "data": {
                "body": getattr(self, "body", None),
                "from": getattr(self, "from_", None),
                "subject": getattr(self, "subject", None),
                "to": getattr(self, "to", None),
            },
        }
        return self._canonicalize(doc)

    def load_document(self, document=None) -> Self:
        """Load document into this document.

        Restore the message envelope from a dict previously produced by
        :meth:`to_dict`. Calls the canonical base implementation first so
        common fields (did, content, paths, schema_version, etc.) are
        populated, then unpacks the message-specific payload from
        ``document["data"]`` back onto the instance attributes
        ``body``, ``from_``, ``subject``, ``to``.

        Args:
            document: A dict (or JSON string) produced by :meth:`to_dict`.

        Returns:
            Self for chaining.
        """
        document = document or self.config.dikt.get("document", {}) or {}
        logma.debug(f"PyfficeMessage.load_document called for {document.get('did', '?')}")
        super().load_document(document)
        data = document.get("data", {}) or {}
        self.set_body(data.get("body"))
        self.set_from(data.get("from"))
        self.set_subject(data.get("subject"))
        self.set_to(data.get("to"))
        return self

    def open_file(self, file_=None) -> Self:
        """Open a message file and load it as a PyfficeMessage.

        Reads the file (JSON envelope produced by ``save``), then
        delegates to :meth:`load_document`.

        Args:
            file_: Path to a message file. ``None`` means use
                ``self.file_path``.

        Returns:
            Self for chaining.
        """
        import json as _json
        if file_ is None:
            file_ = self.file_path
        if not file_ or not exists(file_):
            logma.warning(f"PyfficeMessage.open_file: no such path {file_!r}")
            return self
        try:
            with open(file_, "r") as f:
                doc = _json.load(f)
        except (OSError, ValueError) as e:
            logma.warning(f"PyfficeMessage.open_file failed for {file_!r}: {e}")
            return self
        logma.debug(f"PyfficeMessage.open_file loaded {file_!r}")
        return self.load_document(doc)

    def save(self, path=None, format_=None, encrypt=None) -> None:
        """Save this message to ``path``.

        Writes the canonical envelope produced by :meth:`to_dict` to
        disk as JSON. Calls the base ``save`` to update version /
        change-tracking metadata first so the persisted envelope
        includes the bumped version.

        Args:
            path: Destination path. ``None`` means use ``self.file_path``.
            format_: Format identifier (always JSON for messages).
            encrypt: Unused for messages (JSON is plaintext).
        """
        logma.debug(f"PyfficeMessage.save called path={path!r}")
        super().save(path, format_, encrypt)
        if path is None:
            path = self.file_path
        if not path:
            logma.warning("PyfficeMessage.save: no path available")
            return
        import json as _json
        doc = self.to_dict()
        with open(path, "w") as f:
            _json.dump(doc, f, indent=2, default=str)
        return None


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
