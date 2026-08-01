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
        """"""
        super().load_document(document)
        # TODO implement method
        return self

    def open_file(self, file_=None):
        """"""
        super().open_file(file_)
        # TODO implement method
        return self

    def save(self, path=None, format_=None, encrypt=None):
        """"""
        super().save(path, format_, encrypt)
        # TODO implement method
        return self

    def to_dict(self):
        # TODO implement method
        super().to_dict()
        return self
