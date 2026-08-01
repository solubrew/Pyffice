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
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument

from typing import Any, Dict, List, Optional, Tuple, Union, Set, FrozenSet

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

    def __init__(self, cfg=None):
        """"""
        logma.debug(f"PyfficeMessage.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeMessage")).override(cfg)

    def set_body(self, body) -> "PyfficeMessage":
        """Set message body."""
        self.body = body
        return self

    def set_from(self, from_) -> "PyfficeMessage":
        """Set sender."""
        self.from_ = from_
        return self

    def set_subject(self, subject) -> "PyfficeMessage":
        """Set subject."""
        self.subject = subject
        return self

    def set_to(self, to) -> "PyfficeMessage":
        """Set recipient."""
        self.to = to
        return self

    def to_dict(self) -> Any:
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
                "body": getattr(self, 'body', None),
                "from": getattr(self, 'from_', None),
                "subject": getattr(self, 'subject', None),
                "to": getattr(self, 'to', None),
            },
        }
        return self._canonicalize(doc)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
