"""Pyffice CAM Module

Provides Computer-Aided Manufacturing capabilities.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PyfficeCAM:
    """Computer-Aided Manufacturing handler.

    Provides utilities for CAM operations including file handling,
    toolpath generation, and machine control.

    Attributes:
        name: Name of the CAM project.
        file_path: Path to CAM file.
        units: Measurement units (mm or inch).
    """

    name: str = "Untitled"
    file_path: Optional[str] = None
    units: str = "mm"
    _tools: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize CAM handler."""
        pass

    def load(self, file_path: str) -> "PyfficeCAM":
        """Load CAM file.

        Args:
            file_path: Path to CAM file.

        Returns:
            Self for chaining.
        """
        self.file_path = file_path
        return self

    def save(self, file_path: Optional[str] = None) -> "PyfficeCAM":
        """Save CAM file.

        Args:
            file_path: Optional path, uses self.file_path if None.

        Returns:
            Self for chaining.
        """
        target = file_path or self.file_path
        if not target:
            raise ValueError("No file path specified")
        self.file_path = target
        return self

    def add_tool(self, tool: dict[str, Any]) -> "PyfficeCAM":
        """Add a tool to the tool list.

        Args:
            tool: Tool definition dictionary.

        Returns:
            Self for chaining.
        """
        self._tools.append(tool)
        return self

    def get_tools(self) -> list[dict[str, Any]]:
        """Get all tools.

        Returns:
            List of tool definitions.
        """
        return self._tools.copy()

    def set_units(self, units: str) -> "PyfficeCAM":
        """Set measurement units.

        Args:
            units: 'mm' or 'inch'.

        Returns:
            Self for chaining.
        """
        if units not in ("mm", "inch"):
            raise ValueError("Units must be 'mm' or 'inch'")
        self.units = units
        return self


class PyfficeCAMManager:
    """Manager for PyfficeCAM instances.

    Provides factory and management capabilities for multiple CAM projects.
    """

    def __init__(self) -> None:
        """Initialize CAM manager."""
        self._projects: dict[str, PyfficeCAM] = {}

    def create(self, name: str, **kwargs: Any) -> PyfficeCAM:
        """Create a new CAM project.

        Args:
            name: Project name.
            **kwargs: Additional CAM parameters.

        Returns:
            New PyfficeCAM instance.
        """
        cam = PyfficeCAM(name=name, **kwargs)
        self._projects[name] = cam
        return cam

    def get(self, name: str) -> Optional[PyfficeCAM]:
        """Get CAM project by name.

        Args:
            name: Project name.

        Returns:
            PyfficeCAM instance or None if not found.
        """
        return self._projects.get(name)

    def list_projects(self) -> list[str]:
        """List all project names.

        Returns:
            List of project names.
        """
        return list(self._projects.keys())

    def remove(self, name: str) -> bool:
        """Remove CAM project.

        Args:
            name: Project name.

        Returns:
            True if removed, False if not found.
        """
        if name in self._projects:
            del self._projects[name]
            return True
        return False

    def clear(self) -> None:
        """Clear all projects."""
        self._projects.clear()
