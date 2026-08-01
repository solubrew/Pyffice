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

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "email.yaml")


class PyfficeEmailMessage(PyfficeMessage):
    """"""

    def __init__(self, cfg=None):
        """"""
        logma.debug(f"PyfficeEmailMessage.__init__ called")
        self.config = kahndor.Instruct(pxcfg).select("PyfficeEmailDocument")
        super().__init__()
        self.config.override(cfg)

    def add_bcc(self, bcc) -> "PyfficeEmailMessage":
        """Add BCC recipient to the message."""
        self.bcc = getattr(self, 'bcc', []) + [bcc]
        return self

    def add_cc(self, cc) -> "PyfficeEmailMessage":
        """Add CC recipient to the message."""
        self.cc = getattr(self, 'cc', []) + [cc]
        return self

    def add_recipient(self, recipient) -> "PyfficeEmailMessage":
        """Add recipient to the message."""
        self.recipients = getattr(self, 'recipients', []) + [recipient]
        return self

    def add_label(self, label) -> "PyfficeEmailMessage":
        """Add label to the message."""
        self.labels = getattr(self, 'labels', []) + [label]
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
        return getattr(self, 'body', None)

    def get_footer(self) -> Any:
        """Get the message footer."""
        return getattr(self, 'footer', None)

    def get_header(self, key) -> Any:
        """Get a header value by key."""
        headers = getattr(self, 'headers', {})
        return headers.get(key)

    def get_recipient(self, index=0) -> Any:
        """Get recipient at index."""
        recipients = getattr(self, 'recipients', [])
        return recipients[index] if index < len(recipients) else None

    def get_sender(self) -> Any:
        """Get the sender address."""
        return getattr(self, 'from', None)
    def open_file(self, file_path):
        """Open an email file."""
        if not file_path:
            return self
        import email
        with open(file_path, 'rb') as f:
            msg = email.message_from_bytes(f.read())
            self.message = msg
        return self

    def save_message(self) -> "PyfficeEmailMessage":
        """Save the current message."""
        if not self.message:
            return self
        # Placeholder - would serialize to file
        return self

    def connect_service(self) -> "PyfficeEmailMessage":
        """Connect to email service."""
        # Placeholder - would use imaplib/smtp
        self.connected = True
        return self

    def remove_label(self, label) -> "PyfficeEmailMessage":
        """Remove label from message."""
        labels = getattr(self, 'labels', [])
        if label in labels:
            labels.remove(label)
        return self


class PyfficeMailBox(PyfficeDocumentManager):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        logma.debug(f"PyfficeMailBox.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeMailBoxAccount")).override(cfg)
        self.active_message = None
        self.messages = []

    def connect_service(self) -> "PyfficeMailBox":
        """Connect to email service (OAuth/imap)."""
        # Placeholder - would connect to IMAP/SMTP
        self.connected = True
        return self

    def create_label(self, name) -> "PyfficeMailBox":
        """Create a new label."""
        self.labels = getattr(self, 'labels', {})
        self.labels[name] = []
        return self

    def create_message(self) -> Any:
        """Create a new email message."""
        self.active_message = PyfficeEmailMessage()
        return self.active_message

    def create_rule(self, condition, action) -> "PyfficeMailBox":
        """Create a new mail rule."""
        self.rules = getattr(self, 'rules', [])
        self.rules.append({'condition': condition, 'action': action})
        return self

    def destroy_label(self, name) -> "PyfficeMailBox":
        """Delete a label."""
        labels = getattr(self, 'labels', {})
        if name in labels:
            del labels[name]
        return self

    def delete_mail(self, uid) -> "PyfficeMailBox":
        """Delete mail by UID."""
        self.messages = [m for m in getattr(self, 'messages', []) if m.get('uid') != uid]
        return self

    def delete_rule(self, rule_id) -> "PyfficeMailBox":
        """Delete a mail rule."""
        rules = getattr(self, 'rules', [])
        self.rules = [r for i, r in enumerate(rules) if i != rule_id]
        return self

    def disconnect_service(self) -> "PyfficeMailBox":
        """Disconnect from email service."""
        self.connected = False
        return self

    def get_mail(self, uid) -> None:
        """Get mail by UID."""
        messages = getattr(self, 'messages', [])
        for m in messages:
            if m.get('uid') == uid:
                return m
        return None

    def get_message(self, index=0) -> Any:
        """Get message at index."""
        messages = getattr(self, 'messages', [])
        return messages[index] if index < len(messages) else None

    def get_labels(self) -> Any:
        """Get all labels."""
        return getattr(self, 'labels', {})

    def get_messages(self) -> Any:
        """Get all messages."""
        return getattr(self, 'messages', [])

    def get_message_by_id(self, msg_id) -> None:
        """Get message by ID."""
        messages = getattr(self, 'messages', [])
        for m in messages:
            if m.get('id') == msg_id:
                return m
        return None

    def get_rule(self, index) -> Any:
        """Get rule at index."""
        rules = getattr(self, 'rules', [])
        return rules[index] if index < len(rules) else None

    def get_rules(self) -> Any:
        """Get all rules."""
        return getattr(self, 'rules', [])

    def process_rules(self) -> "PyfficeMailBox":
        """Apply all rules to inbox."""
        rules = getattr(self, 'rules', [])
        for rule in rules:
            # Placeholder - would apply each rule
            pass
        return self

    def send_mail(self, message) -> "PyfficeMailBox":
        """Send an email message."""
        if not message:
            return self
        # Placeholder - would use SMTP to send
        return self

    def send_message(self) -> Any:
        """Send the current message."""
        return self.send_mail(self.active_message) if self.active_message else self

    def store_mail(self, message) -> "PyfficeMailBox":
        """Store a message in the mailbox."""
        self.messages = getattr(self, 'messages', [])
        self.messages.append(message)
        return self

    def write_message(self, subject, body, recipients=None) -> "PyfficeMailBox":
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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
