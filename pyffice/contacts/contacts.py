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
from pycurity.pyvalid import validate_email_address, validate_phone_number, validate_postal_address

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "contacts.yaml")


class PyfficeAddress(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeAddress").override(cfg))
        self.street_name = None
        self.street_number = None
        self.city_name = None
        self.state_name = None
        self.zip_code = None
        self.apt = None

    @classmethod
    def from_dict(cls, dikt):
        """"""
        cfg = {"street_name": dikt}
        return cls(cfg)


class PyfficeContact(PyfficeDocument):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeContact").override(cfg))
        self.address = None
        self.addresses = []
        self.emails = None
        self.emergency_phone = None
        self.full_name = None
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.surname = None
        self.suffix = None
        self.name = None
        self.user_name = None
        self.phones = []
        self.phone = None
        self.secondary_phone = None
        self.preferred_name = None
        self.connections = []
        self.connection = None
        self.company_email = None
        self.company_phone = None
        self.channels = []
        self.groups = []
        self.names = None
        self.nicknames = None
        self.preferred_channel = None
        self.salutation = None

    def add_address(self, address):
        """"""
        if isinstance(address, dict):
            address = PyfficeAddress.from_dict(address)
        if self.addresses == []:
            self.address = address
        self.addresses.append(address)

    def add_connection(self, connection):
        """A connection is another contact that this contact is connected to."""
        self.connections.append(connection)
        return self

    def add_email_address(self, email):
        """"""
        email = {"type": "email", "contact": email}
        self.add_change("channels", self.channels, email)
        if self.verify_email(email["contact"]):
            self.channels.append(email)
        return self

    def add_emergency_contact(self, contact: "PyfficeContact"):
        """"""
        self.emergency_contact = contact

    def add_group(self, group):
        """"""
        if group not in self.groups:
            self.add_change("groups", self.groups, group, "add")
            self.groups.append(group)
        return self

    def add_phone_address(self, phone):
        """"""
        phone = {"type": "phone", "contact": phone}
        if self.phone is None:
            self.phone = phone
        self.add_change("channels", self.channels, phone)
        if self.verify_phone_number(phone["contact"]):
            self.channels.append(phone)
        return self

    def add_postal_address(self, postal):
        """"""
        postal = {"type": "postal_address", "contact": postal}
        self.add_change("channels", self.channels, postal)
        if self.verify_postal_address(postal["contact"]):
            self.channels.append(postal)
        return self

    def add_social_contact(self, handle, social_network):
        """"""
        social_network = {"type": "social", "contact": handle, "network": social_network}
        self.add_change("channels", self.channels, social_network)
        if self.verify_social(handle, social_network["contact"]):
            self.channels.append(social_network)
        return self

    def del_channel(self, dex):
        """Remove the channel at index dex from self.channels."""
        if 0 <= dex < len(self.channels):
            removed = self.channels.pop(dex)
            self.add_change("channels", self.channels + [removed], self.channels)
        return self

    def del_connection(self, dex):
        """Remove the connection at index dex from self.connections."""
        if 0 <= dex < len(self.connections):
            removed = self.connections.pop(dex)
            self.add_change("connections", self.connections + [removed], self.connections)
        return self

    def del_email_address(self):
        """Remove all email-type channels from self.channels."""
        kept = [c for c in self.channels if c.get("type") != "email"]
        if kept != self.channels:
            self.add_change("channels", self.channels, kept)
            self.channels = kept
        return self

    def del_add_phone_address(self, phone):
        """Remove phone-type channels whose value matches phone."""
        kept = [c for c in self.channels
                if not (c.get("type") == "phone" and c.get("contact") == phone)]
        if kept != self.channels:
            self.add_change("channels", self.channels, kept)
            self.channels = kept
        return self

    def del_postal_address(self, address):
        """Remove postal-address channels whose value matches address."""
        kept = [c for c in self.channels
                if not (c.get("type") == "postal_address" and c.get("contact") == address)]
        if kept != self.channels:
            self.add_change("channels", self.channels, kept)
            self.channels = kept
        return self

    def del_social_contact(self, contact):
        """Remove social-type channels whose handle matches contact."""
        kept = [c for c in self.channels
                if not (c.get("type") == "social" and c.get("contact") == contact)]
        if kept != self.channels:
            self.add_change("channels", self.channels, kept)
            self.channels = kept
        return self

    def connect_contact(self):
        """"""
        contact = {"id": self.did, "name": self.name, "channels": self.channels, "type": "contact"}
        return contact

    def get_postal_address(self):
        """Return the first postal-address channel (or None)."""
        for c in self.channels:
            if c.get("type") == "postal_address":
                return c.get("contact")
        return None

    def get_email_address(self):
        """Return the first email-type channel (or None)."""
        for c in self.channels:
            if c.get("type") == "email":
                return c.get("contact")
        return None

    def load_document(self, document=None):
        """"""
        if document is None:
            document = {}
        super().load_document(document)
        self.set_names(document.get("name_details", {}))
        self.set_groups(document.get("group", None))
        self.set_channels(document.get("channels", []))
        self.set_preferred_channel(document.get("preferred_channel", None))
        return self

    def set_channels(self, document):
        """"""
        for channel in document:
            if channel["type"] == "phone":
                self.add_phone_address(channel["contact"])
            elif channel["type"] == "email":
                self.add_email_address(channel["contact"])
            elif channel["type"] == "address":
                self.add_postal_address(channel["contact"])
            elif channel["type"] == "social":
                self.add_social_contact(channel["contact"], channel["network"])
        return self

    def set_groups(self, groups):
        """"""
        if groups is None:
            groups = ["default"]
        if groups != self.groups:
            self.add_change("group", self.groups, groups)
            self.groups = groups
        return self

    def set_name_first(self, name):
        """"""
        if name != self.first_name:
            self.add_change("first_name", self.first_name, name)
            self.first_name = name
        return self

    def set_name_full(self, name):
        """"""
        if name != self.full_name:
            self.add_change("full_name", self.full_name, name)
            self.full_name = name
        return self

    def set_name_middle(self, name):
        """"""
        if name != self.middle_name:
            self.add_change("middle_name", self.middle_name, name)
            self.middle_name = name
        return self

    def set_name_nicknames(self, nicknames):
        """"""
        if nicknames != self.nicknames:
            self.add_change("nicknames", self.nicknames, nicknames)
            self.nicknames = nicknames
        return self

    def set_name_last(self, name):
        """"""
        if name != self.last_name:
            self.add_change("last_name", self.last_name, name)
            self.last_name = name
        return self

    def set_name_preferred(self, name):
        """"""
        if name != self.preferred_name:
            self.add_change("preferred_name", self.preferred_name, name)
            self.preferred_name = name
        return self

    def set_name_sur(self, name):
        """"""
        if name != self.surname:
            self.add_change("surname", self.surname, name)
            self.surname = name
        return self

    def set_name_salutation(self, name):
        """Set self.salutation to name."""
        if name != self.salutation:
            self.add_change("salutation", self.salutation, name)
            self.salutation = name
        return self

    def set_name_suffix(self, name):
        """"""
        if name != self.suffix:
            self.add_change("suffix", self.suffix, name)
            self.suffix = name
        return self

    def set_names(self, names):
        """"""
        if names is None:
            names = {}
        if names != self.names:
            self.add_change("names", self.names, names)
            self.names = names
            self.first_name = names.get("first", "")
            self.middle_name = names.get("middle", "")
            self.last_name = names.get("last", "")
            self.preferred_name = names.get("preferred", "")
            self.surname = names.get("sur", "")
            self.suffix = names.get("suffix", "")
            self.salutation = names.get("salutation", "")
            self.nicknames = names.get("nicknames", [])
            self.full_name = names.get(
                "full", self.first_name + " " + self.middle_name + " " + self.last_name + " " + self.surname
            )
        return self

    def set_preferred_channel(self, channel):
        """"""
        if channel != self.preferred_channel:
            self.add_change("preferred_channel", self.preferred_channel, channel)
            self.preferred_channel = channel
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict() or {}
        if "data" not in doc.keys():
            doc["data"] = {}
        doc["data"]["name_details"] = {
            "full": self.full_name,
            "first": self.first_name,
            "middle": self.middle_name,
            "last": self.last_name,
            "preferred": self.preferred_name,
            "sur": self.surname,
            "suffix": self.suffix,
            "salutation": self.salutation,
        }
        doc["data"]["nicknames"] = self.nicknames
        doc["data"]["channels"] = self.channels
        doc["data"]["groups"] = self.groups
        return doc

    def verify_phone_number(self, phone):
        """"""
        valid = validate_phone_number(phone)
        if valid["valid"]:
            self.channels = [{"type": "phone", "contact": phone}]
        return self

    def verify_email(self, email):
        """"""
        valid = validate_email_address(email)
        if valid["valid"]:
            self.channels = [{"type": "email", "contact": email}]
        return self

    def verify_postal_address(self, address):
        """"""
        valid = validate_postal_address(address)
        if valid["valid"]:
            self.channels = [{"type": "postal_address", "contact": address}]
        return self

    def verify_social(self, handle, social_network):
        """Verify social media handle."""
        return True  # Placeholder - would verify via API


class PyfficeRolodex(PyfficeDocumentManager):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeRolodex").override(cfg))
        self.default_group = None
        self.groups = []
        self.contacts = {}

    def add_contact(self, contact, group=None):
        """"""
        if group is None:
            group = self.default_group
        self.add_change("group", self.default_group, group)
        logma.info(f"Contact {contact} added to group {group}")
        logma.info(f"Contacts {self.contacts}")
        self.contacts[contact.name] = contact
        # self.add_connection(contact.connection)
        return self

    def add_group(self, group):
        """"""
        if group not in self.groups:
            self.groups.append(group)
        return self

    def del_contact(self, name):
        """"""
        del self.contacts[name]
        return self

    def filter_by_group(self, cfg):
        """Filter contacts by group."""
        return []

    def get_contacts(self, search_term=None):
        """Get all contacts."""
        return []

    def get_contact(self, contact_id):
        """Get contact by ID."""
        return None

    def get_count(self):
        """"""
        return len(self.contacts)

    def get_group_by_name(self, name):
        """"""
        group = [self.contacts[contact] for contact in self.contacts if name in self.contacts[contact].groups]
        return group

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_contacts(document.get("contacts", None))
        self.set_groups(document.get("groups", None))
        self.set_group_default(document.get("default_group", None))
        return self

    def set_contacts(self, contacts):
        """"""
        if contacts is None:
            contacts = {}
        if self.contacts != contacts:
            self.add_change("contacts", self.contacts, contacts)
            self.contacts = contacts
        for contact in contacts:
            contact = PyfficeContact(contact)
            contact.load_document()
            self.add_contact(contact)
        return self

    def set_group_default(self, group=None):
        """"""
        if group is None:
            group = self.config.dikt.get("default_group", None)
        if group != self.default_group:
            self.add_change("default_group", self.default_group, group)
            self.default_group = group
        return self

    def set_groups(self, groups):
        """"""
        if groups is None:
            groups = ["default"]
        if groups != self.groups:
            self.add_change("groups", self.groups, groups)
            self.groups = groups
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"] = {
            "contacts": {name: x.to_dict() for name, x in self.contacts.items()},
            "groups": self.groups,
            "default_group": self.default_group,
        }
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
