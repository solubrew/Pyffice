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
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "cam.yaml")


class PyfficeCAM(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """Initialize the CAM handler."""
        logma.debug(f"PyfficeCAM.__init__ called")
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

    def load(self, file_path) -> Self:
        """Load CAM file.

        Args:
            file_path: Path to CAM file.

        Returns:
            Self for chaining.
        """
        self.file_path = file_path
        return self

    def save_cam(self, file_path=None) -> Self:
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

    def add_tool(self, tool) -> Self:
        """Add a tool to the tool list.

        Args:
            tool: Tool definition dictionary.

        Returns:
            Self for chaining.
        """
        self._tools.append(tool)
        return self

    def get_tools(self) -> list:
        """Get all tools.

        Returns:
            List of tool definitions.
        """
        return list(self._tools)

    def set_units(self, units) -> Self:
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

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "file_path" in content:
                setattr(self, "file_path", content["file_path"])
            if "units" in content:
                setattr(self, "units", content["units"])
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
            "file_path": getattr(self, "file_path", None),
            "units": getattr(self, "units", None),
        }
        doc = {
            "did": self.did,
            "meta_data": {"schema_version": list(self.SERIALIZATION_VERSION)},
            "data": {
                "content": attrs,
                "document_type": "cam",
            },
        }
        return self._canonicalize(doc)


class PyfficeCAMManager(PyfficeDocumentManager):
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """Initialize the CAM manager."""
        logma.debug(f"PyfficeCAMManager.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeCAMManager")).override(cfg)
        # Project registry. Merged from the deleted
        # pyffice/cam/cam.py PyfficeCAMManager class.
        self._projects: dict[str, PyfficeCAM] = {}

    def create(self, project_name, **kwargs) -> None:
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

    def get(self, name) -> Any:
        """Get CAM project by name.

        Args:
            name: Project name.

        Returns:
            :class:`PyfficeCAM` instance or None if not found.
        """
        return self._projects.get(name)

    def list_projects(self) -> list:
        """List all project names.

        Returns:
            List of project names.
        """
        return list(self._projects.keys())

    def remove(self, project_name) -> bool:
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

    def clear(self) -> None:
        """Clear all projects."""
        self._projects.clear()

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "file_path" in content:
                setattr(self, "file_path", content["file_path"])
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
            "file_path": getattr(self, "file_path", None),
        }
        doc = {
            "did": self.did,
            "meta_data": {"schema_version": list(self.SERIALIZATION_VERSION)},
            "data": {
                "content": attrs,
                "document_type": "cammanager",
            },
        }
        return self._canonicalize(doc)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
