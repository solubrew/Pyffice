# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid:
    name:
    description: >
        A BOM is a workflow because in its ultimate form the needs of that BOM are placed on a timeline of events.
    version: 0.0.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt
from typing import Any, Optional

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "_data_", "bom.yaml")


class PyfficeBOM(PyfficeDocumentManager):
    """Bill of Materials handler.

    Manages component lists for manufacturing and assembly.
    The item-management logic (``add_item``, ``remove_item``,
    ``get_item``, ``total_quantity``, ``to_dict``) was merged
    from the deleted ``pyffice/cam/bom.py`` @dataclass — the
    dataclass was a phantom duplicate of this class, but its
    domain logic is real and belongs on the canonical
    PyfficeDocumentManager-based class.
    """

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """Initialize the BOM handler."""
        self.config = kahndor.Instruct(pxcfg).override("PyfficeBOM")
        super().__init__(self)
        self.config.override(cfg)
        self.project_name: str = "Untitled"
        self.revision: str = "A"
        self.items: list[dict[str, Any]] = []

    def add_part(self, part):
        """Add a part.

        Args:
            part: Parameter.

        Returns:
            Self for chaining.
        """
        super().add_document(part)

    def add_item(self, part_number, description, quantity=1, **kwargs):
        """Add item to BOM.

        Args:
            part_number: Part identifier.
            description: Part description.
            quantity: Number of units.
            **kwargs: Additional item properties.

        Returns:
            Self for chaining.
        """
        item = {
            "part_number": part_number,
            "description": description,
            "quantity": quantity,
            **kwargs,
        }
        self.items.append(item)
        return self

    def remove_item(self, part_number):
        """Remove item by part number.

        Args:
            part_number: Part identifier.

        Returns:
            True if removed, False if not found.
        """
        for i, item in enumerate(self.items):
            if item.get("part_number") == part_number:
                self.items.pop(i)
                return True
        return False

    def get_item(self, part_number):
        """Get item by part number.

        Args:
            part_number: Part identifier.

        Returns:
            Item dictionary or None.
        """
        for item in self.items:
            if item.get("part_number") == part_number:
                return item
        return None

    def total_quantity(self):
        """Get total quantity of all items.

        Returns:
            Sum of all item quantities.
        """
        return sum(item.get("quantity", 1) for item in self.items)

    def load_document(self, document):
        """Load document into this document.

        Args:
            document: Parameter.

        Returns:
            Self for chaining.
        """
        super().load_document(document)
        return self

    def to_dict(self):
        """Convert this document to dict.

        Returns:
            BOM data as a dictionary.
        """
        doc = super().to_dict()
        doc["data"]["bom"] = {
            "project_name": self.project_name,
            "revision": self.revision,
            "items": self.items,
            "total_quantity": self.total_quantity(),
        }
        return doc


class PyfficeSoftwareBOM(PyfficeBOM):
    """Software Bill of Materials handler.

    Tracks software dependencies and components. Domain logic
    (``add_package``, ``remove_package``, ``get_package``,
    ``to_dict``) merged from the deleted
    ``pyffice/cam/bom.py`` ``PyfficeSoftwareBOM`` @dataclass.
    """

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """Initialize the Software BOM handler."""
        self.config = kahndor.Instruct(pxcfg).override("PyfficeSoftwareBOM")
        super().__init__(self)
        self.config.override(cfg)
        self.version: str = "SPDX"
        self.packages: list[dict[str, Any]] = []

    def add_part(self, part):
        """Add a part.

        Args:
            part: Parameter.

        Returns:
            Self for chaining.
        """
        super().add_part(part)

    def add_package(self, name, version, license_=None, **kwargs):
        """Add package to SBOM.

        Args:
            name: Package name.
            version: Package version.
            license_: Package license.
            **kwargs: Additional package properties.

        Returns:
            Self for chaining.
        """
        pkg = {
            "name": name,
            "version": version,
            "license": license_,
            **kwargs,
        }
        self.packages.append(pkg)
        return self

    def remove_package(self, name):
        """Remove package by name.

        Args:
            name: Package name.

        Returns:
            True if removed, False if not found.
        """
        for i, pkg in enumerate(self.packages):
            if pkg.get("name") == name:
                self.packages.pop(i)
                return True
        return False

    def get_package(self, name):
        """Get package by name.

        Args:
            name: Package name.

        Returns:
            Package dictionary or None.
        """
        for pkg in self.packages:
            if pkg.get("name") == name:
                return pkg
        return None

    def load_document(self, document):
        """Load document into this document.

        Args:
            document: Parameter.

        Returns:
            Self for chaining.
        """
        super().load_document(document)
        return self

    def to_dict(self):
        """Convert this document to dict.

        Returns:
            SBOM data as a dictionary.
        """
        doc = super().to_dict()
        doc["data"]["sbom"] = {
            "project_name": self.project_name,
            "version": self.version,
            "packages": self.packages,
        }
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
