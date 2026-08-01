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
from typing import Any
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeGCode(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """Initialize the G-code generator."""
        logma.debug(f"PyfficeGCode.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("GCodeDocument")).override(cfg)
        # G-code generation state. Merged from the deleted
        # pyffice/cam/gcode.py @dataclass (Sprint 18 review):
        # the dataclass was a phantom duplicate of this class,
        # but the G-code generation logic it carried is real and
        # belongs on the canonical PyfficeDocument-based class.
        self.feed_rate: float = 100.0
        self.spindle_speed: float = 1000.0
        self.tool_number: int = 1
        self.units: str = "mm"
        self._code_lines: list[str] = []
        self._initialize()

    # ----- G-code generation (merged from cam/gcode.py) -----

    def _initialize(self) -> None:
        """Send initialization codes."""
        self._add("G21")  # Metric units
        if self.units == "inch":
            self._add("G20")
        self._add("G90")  # Absolute positioning
        self._add("M3")  # Start spindle

    def _add(self, code: str) -> None:
        """Add a G-code line."""
        self._code_lines.append(code)

    def rapid_move(self, x=None, y=None, z=None) -> Self:
        """Generate rapid move (G0).

        Args:
            x: Optional X coordinate.
            y: Optional Y coordinate.
            z: Optional Z coordinate.

        Returns:
            Self for chaining.
        """
        cmd = "G0"
        if x is not None:
            cmd += f" X{x}"
        if y is not None:
            cmd += f" Y{y}"
        if z is not None:
            cmd += f" Z{z}"
        self._add(cmd)
        return self

    def linear_move(self, x=None, y=None, z=None) -> Self:
        """Generate linear move (G1).

        Args:
            x: Optional X coordinate.
            y: Optional Y coordinate.
            z: Optional Z coordinate.

        Returns:
            Self for chaining.
        """
        cmd = "G1"
        if x is not None:
            cmd += f" X{x}"
        if y is not None:
            cmd += f" Y{y}"
        if z is not None:
            cmd += f" Z{z}"
        cmd += f" F{self.feed_rate}"
        self._add(cmd)
        return self

    def arc_cw(self, x, y, i, j) -> Self:
        """Generate clockwise arc (G2).

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            i: X offset from start.
            j: Y offset from start.

        Returns:
            Self for chaining.
        """
        self._add(f"G2 X{x} Y{y} I{i} J{j} F{self.feed_rate}")
        return self

    def arc_ccw(self, x, y, i, j) -> Self:
        """Generate counter-clockwise arc (G3).

        Args:
            x: Target X coordinate.
            y: Target Y coordinate.
            i: X offset from start.
            j: Y offset from start.

        Returns:
            Self for chaining.
        """
        self._add(f"G3 X{x} Y{y} I{i} J{j} F{self.feed_rate}")
        return self

    def set_feed_rate(self, rate) -> Self:
        """Set feed rate.

        Args:
            rate: New feed rate.

        Returns:
            Self for chaining.
        """
        self.feed_rate = rate
        return self

    def set_spindle_speed(self, rpm) -> Self:
        """Set spindle speed.

        Args:
            rpm: Spindle speed in RPM.

        Returns:
            Self for chaining.
        """
        self.spindle_speed = rpm
        self._add(f"S{rpm}")
        return self

    def tool_change(self, tool) -> Self:
        """Change tool.

        Args:
            tool: Tool number.

        Returns:
            Self for chaining.
        """
        self.tool_number = tool
        self._add(f"M6 T{tool}")
        return self

    def pause(self) -> Self:
        """Add program pause.

        Returns:
            Self for chaining.
        """
        self._add("M0")
        return self

    def end(self) -> Self:
        """End program.

        Returns:
            Self for chaining.
        """
        self._add("M5")  # Stop spindle
        self._add("M30")  # End program
        return self

    def to_string(self) -> Any:
        """Return G-code as a single string.

        Returns:
            Newline-joined G-code lines.
        """
        return "\n".join(self._code_lines)

    def save_gcode(self, filepath=None) -> Self:
        """Save G-code to file.

        Args:
            filepath: Destination path. Falls back to
                ``self.file_path`` if None.

        Returns:
            Self for chaining.
        """
        target = filepath or getattr(self, "file_path", None)
        if not target:
            return self
        with open(target, "w") as f:
            f.write(self.to_string())
        return self

    def load_document(self, document=None) -> Self:
        logma.debug(f"{self.__class__.__name__}.load_document called")
        super().load_document(document)
        if not isinstance(document, dict):
            return self
        data = document.get("data", {}) or {}
        content = data.get("content", {}) or {}
        if isinstance(content, dict):
            if "feed_rate" in content:
                setattr(self, "feed_rate", content["feed_rate"])
            if "spindle_speed" in content:
                setattr(self, "spindle_speed", content["spindle_speed"])
            if "tool_number" in content:
                setattr(self, "tool_number", content["tool_number"])
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
