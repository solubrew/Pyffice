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
from pyffice.text.text_messages import PyfficeMessage
from typing import Any
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "email.yaml")


class PyfficeEmailMessage(PyfficeMessage):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficeEmailMessage.__init__ called")
        self.config = kahndor.Instruct(pxcfg).select("PyfficeEmailDocument")
        super().__init__()
        self.config.override(cfg)

    def add_bcc(self, bcc) -> Self:
        """Add BCC recipient to the message."""
        self.bcc = getattr(self, "bcc", []) + [bcc]
        return self

    def add_cc(self, cc) -> Self:
        """Add CC recipient to the message."""
        self.cc = getattr(self, "cc", []) + [cc]
        return self

    def add_recipient(self, recipient) -> Self:
        """Add recipient to the message."""
        self.recipients = getattr(self, "recipients", []) + [recipient]
        return self

    def add_label(self, label) -> Self:
        """Add label to the message."""
        self.labels = getattr(self, "labels", []) + [label]
        return self

    def create_new_document(self, name) -> None:
        """Create a new document.

        Args:
            name: Parameter.

        Returns:
            Self for chaining.
        """
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

    def get_body(self) -> Any:
        """Get the message body."""
        return getattr(self, "body", None)

    def get_footer(self) -> Any:
        """Get the message footer."""
        return getattr(self, "footer", None)

    def get_header(self, key) -> Any:
        """Get a header value by key."""
        headers = getattr(self, "headers", {})
        return headers.get(key)

    def get_recipient(self, index=0) -> Any:
        """Get recipient at index."""
        recipients = getattr(self, "recipients", [])
        return recipients[index] if index < len(recipients) else None

    def get_sender(self) -> Any:
        """Get the sender address."""
        return getattr(self, "from", None)

    def open_file(self, file_path) -> Self:
        """Open an email file."""
        if not file_path:
            return self
        import email

        with open(file_path, "rb") as f:
            msg = email.message_from_bytes(f.read())
            self.message = msg
        return self

    def save_message(self) -> Self:
        """Save the current message."""
        if not self.message:
            return self
        # Placeholder - would serialize to file
        return self

    def connect_service(self) -> Self:
        """Connect to email service."""
        # Placeholder - would use imaplib/smtp
        self.connected = True
        return self

    def remove_label(self, label) -> Self:
        """Remove label from message."""
        labels = getattr(self, "labels", [])
        if label in labels:
            labels.remove(label)
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
            if "bcc" in content:
                setattr(self, "bcc", content["bcc"])
            if "cc" in content:
                setattr(self, "cc", content["cc"])
            if "recipients" in content:
                setattr(self, "recipients", content["recipients"])
            if "labels" in content:
                setattr(self, "labels", content["labels"])
            if "message" in content:
                setattr(self, "message", content["message"])
            if "connected" in content:
                setattr(self, "connected", content["connected"])
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


class PyfficeMailBox(PyfficeDocumentManager):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficeMailBox.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeMailBoxAccount")).override(cfg)
        self.active_message = None
        self.messages = []

    def connect_service(self) -> Self:
        """Connect to email service (OAuth/imap)."""
        # Placeholder - would connect to IMAP/SMTP
        self.connected = True
        return self

    def create_label(self, name) -> Self:
        """Create a new label."""
        self.labels = getattr(self, "labels", {})
        self.labels[name] = []
        return self

    def create_message(self) -> Any:
        """Create a new email message."""
        self.active_message = PyfficeEmailMessage()
        return self.active_message

    def create_rule(self, condition, action) -> Self:
        """Create a new mail rule."""
        self.rules = getattr(self, "rules", [])
        self.rules.append({"condition": condition, "action": action})
        return self

    def destroy_label(self, name) -> Self:
        """Delete a label."""
        labels = getattr(self, "labels", {})
        if name in labels:
            del labels[name]
        return self

    def delete_mail(self, uid) -> Self:
        """Delete mail by UID."""
        self.messages = [m for m in getattr(self, "messages", []) if m.get("uid") != uid]
        return self

    def delete_rule(self, rule_id) -> Self:
        """Delete a mail rule."""
        rules = getattr(self, "rules", [])
        self.rules = [r for i, r in enumerate(rules) if i != rule_id]
        return self

    def disconnect_service(self) -> Self:
        """Disconnect from email service."""
        self.connected = False
        return self

    def get_mail(self, uid) -> Any:
        """Get mail by UID."""
        messages = getattr(self, "messages", [])
        for m in messages:
            if m.get("uid") == uid:
                return m
        return None

    def get_message(self, index=0) -> Any:
        """Get message at index."""
        messages = getattr(self, "messages", [])
        return messages[index] if index < len(messages) else None

    def get_labels(self) -> Any:
        """Get all labels."""
        return getattr(self, "labels", {})

    def get_messages(self) -> Any:
        """Get all messages."""
        return getattr(self, "messages", [])

    def get_message_by_id(self, msg_id) -> Any:
        """Get message by ID."""
        messages = getattr(self, "messages", [])
        for m in messages:
            if m.get("id") == msg_id:
                return m
        return None

    def get_rule(self, index) -> Any:
        """Get rule at index."""
        rules = getattr(self, "rules", [])
        return rules[index] if index < len(rules) else None

    def get_rules(self) -> Any:
        """Get all rules."""
        return getattr(self, "rules", [])

    def process_rules(self) -> Self:
        """Apply all rules to inbox."""
        rules = getattr(self, "rules", [])
        for rule in rules:
            # Placeholder - would apply each rule
            pass
        return self

    def send_mail(self, message) -> Self:
        """Send an email message."""
        if not message:
            return self
        # Placeholder - would use SMTP to send
        return self

    def send_message(self) -> Any:
        """Send the current message."""
        return self.send_mail(self.active_message) if self.active_message else self

    def store_mail(self, message) -> Self:
        """Store a message in the mailbox."""
        self.messages = getattr(self, "messages", [])
        self.messages.append(message)
        return self

    def write_message(self, subject, body, recipients=None) -> Self:
        """Write message.

        Args:
            subject: Parameter.
            body: Parameter.
            recipients: Parameter.

        Returns:
            Self for chaining.
        """
        self.active_message.add_subject(subject)
        self.active_message.add_body(body)
        if recipients:
            for recipient in recipients:
                self.active_message.add_recipient(recipient)
        return self

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "active_message" in content:
                setattr(self, "active_message", content["active_message"])
            if "messages" in content:
                setattr(self, "messages", content["messages"])
            if "connected" in content:
                setattr(self, "connected", content["connected"])
            if "labels" in content:
                setattr(self, "labels", content["labels"])
            if "rules" in content:
                setattr(self, "rules", content["rules"])
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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
