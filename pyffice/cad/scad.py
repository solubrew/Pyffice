"""OpenSCAD script format support."""

from typing_extensions import Self
from typing import Any, Optional
import io

from pyffice.document import PyfficeDocument

from kahndor.logma import Logma

logma = Logma(__name__)
logma.off()


class PyfficeSCAD(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """OpenSCAD script document."""

    def __init__(self, path: Optional[str] = None, content: Optional[str] = None) -> None:
        super().__init__(path=path, content=content)
        logma.debug(f"PyfficeSCAD.__init__ called")
        self.doc_type = "scad"

    def load(self, path: str) -> str:
        """Load OpenSCAD script contents."""
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        self.content = content
        return content

    def read(self, path: str) -> str:
        """Read OpenSCAD script contents."""
        return self.load(path)

    def write(self, data: str, path: str) -> None:
        """Write data to OpenSCAD file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

    def dump(self, data: str, path: str) -> None:
        """Dump data to OpenSCAD file."""
        self.write(data, path)

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "doc_type" in content:
                setattr(self, "doc_type", content["doc_type"])
            if "content" in content:
                setattr(self, "content", content["content"])
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
