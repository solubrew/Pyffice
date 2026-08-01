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
from typing import Any

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "cam.yaml")


class PyfficeCAM(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """Initialize the CAM handler."""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeCAM")).override(cfg)
        # CAM project state. Merged from the deleted
        # pyffice/cam/cam.py @dataclass: the dataclass was a
        # phantom duplicate of this class, but the project /
        # tool / unit-management logic it carried is real and
        # belongs on the canonical PyfficeDocument-based class.
        self.name: str = "Untitled"
        self.units: str = "mm"
        self._tools: list[dict[str, Any]] = []

    def load(self, file_path):
        """Load CAM file.

        Args:
            file_path: Path to CAM file.

        Returns:
            Self for chaining.
        """
        self.file_path = file_path
        return self

    def save_cam(self, file_path=None):
        """Save CAM file.

        Args:
            file_path: Optional path, uses ``self.file_path``
                if None.

        Returns:
            Self for chaining.
        """
        target = file_path or getattr(self, "file_path", None)
        if not target:
            return self
        self.file_path = target
        return self

    def add_tool(self, tool):
        """Add a tool to the tool list.

        Args:
            tool: Tool definition dictionary.

        Returns:
            Self for chaining.
        """
        self._tools.append(tool)
        return self

    def get_tools(self):
        """Get all tools.

        Returns:
            List of tool definitions.
        """
        return list(self._tools)

    def set_units(self, units):
        """Set measurement units.

        Args:
            units: ``'mm'`` or ``'inch'``.

        Returns:
            Self for chaining.
        """
        if units not in ("mm", "inch"):
            return self
        self.units = units
        return self
class PyfficeCAMManager(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """Initialize the CAM manager."""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeCAMManager")).override(cfg)
        # Project registry. Merged from the deleted
        # pyffice/cam/cam.py PyfficeCAMManager class.
        self._projects: dict[str, PyfficeCAM] = {}

    def create(self, project_name, **kwargs):
        """Create a new CAM project.

        Args:
            project_name: Project name.
            **kwargs: Additional CAM parameters.

        Returns:
            New :class:`PyfficeCAM` instance.
        """
        cam = PyfficeCAM(**kwargs)
        cam.name = project_name
        self._projects[project_name] = cam
        return cam

    def get(self, name):
        """Get CAM project by name.

        Args:
            name: Project name.

        Returns:
            :class:`PyfficeCAM` instance or None if not found.
        """
        return self._projects.get(name)

    def list_projects(self):
        """List all project names.

        Returns:
            List of project names.
        """
        return list(self._projects.keys())

    def remove(self, project_name):
        """Remove CAM project.

        Args:
            project_name: Project name.

        Returns:
            True if removed, False if not found.
        """
        if project_name in self._projects:
            del self._projects[project_name]
            return True
        return False

    def clear(self):
        """Clear all projects."""
        self._projects.clear()
# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
