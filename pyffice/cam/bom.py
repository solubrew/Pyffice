"""Pyffice BOM Module

Provides Bill of Materials generation and management.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PyfficeBOM:
    """Bill of Materials handler.

    Manages component lists for manufacturing and assembly.

    Attributes:
        project_name: Name of the associated project.
        items: List of BOM items.
        revision: BOM revision number.
    """

    project_name: str = "Untitled"
    items: list[dict[str, Any]] = field(default_factory=list)
    revision: str = "A"

    def add_item(
        self,
        part_number: str,
        description: str,
        quantity: int = 1,
        **kwargs: Any
    ) -> "PyfficeBOM":
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
            **kwargs
        }
        self.items.append(item)
        return self

    def remove_item(self, part_number: str) -> bool:
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

    def get_item(self, part_number: str) -> Optional[dict[str, Any]]:
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

    def total_quantity(self) -> int:
        """Get total quantity of all items.

        Returns:
            Sum of all item quantities.
        """
        return sum(item.get("quantity", 1) for item in self.items)

    def to_dict(self) -> dict[str, Any]:
        """Export BOM as dictionary.

        Returns:
            BOM data as dictionary.
        """
        return {
            "project_name": self.project_name,
            "revision": self.revision,
            "items": self.items,
            "total_quantity": self.total_quantity()
        }


@dataclass
class PyfficeSoftwareBOM:
    """Software Bill of Materials handler.

    Tracks software dependencies and components.

    Attributes:
        project_name: Name of the software project.
        packages: List of software packages.
        version: SBOM version format.
    """

    project_name: str = "Untitled"
    packages: list[dict[str, Any]] = field(default_factory=list)
    version: str = "SPDX"

    def add_package(
        self,
        name: str,
        version: str,
        license_: Optional[str] = None,
        **kwargs: Any
    ) -> "PyfficeSoftwareBOM":
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
            **kwargs
        }
        self.packages.append(pkg)
        return self

    def remove_package(self, name: str) -> bool:
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

    def get_package(self, name: str) -> Optional[dict[str, Any]]:
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

    def to_dict(self) -> dict[str, Any]:
        """Export SBOM as dictionary.

        Returns:
            SBOM data as dictionary.
        """
        return {
            "project_name": self.project_name,
            "version": self.version,
            "packages": self.packages
        }
