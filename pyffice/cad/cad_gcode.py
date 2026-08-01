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

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeGCode(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None):
        """Initialize the G-code generator."""
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
        self._add("M3")   # Start spindle

    def _add(self, code: str) -> None:
        """Add a G-code line."""
        self._code_lines.append(code)

    def rapid_move(self, x=None, y=None, z=None):
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

    def linear_move(self, x=None, y=None, z=None):
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

    def arc_cw(self, x, y, i, j):
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

    def arc_ccw(self, x, y, i, j):
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

    def set_feed_rate(self, rate):
        """Set feed rate.

        Args:
            rate: New feed rate.

        Returns:
            Self for chaining.
        """
        self.feed_rate = rate
        return self

    def set_spindle_speed(self, rpm):
        """Set spindle speed.

        Args:
            rpm: Spindle speed in RPM.

        Returns:
            Self for chaining.
        """
        self.spindle_speed = rpm
        self._add(f"S{rpm}")
        return self

    def tool_change(self, tool):
        """Change tool.

        Args:
            tool: Tool number.

        Returns:
            Self for chaining.
        """
        self.tool_number = tool
        self._add(f"M6 T{tool}")
        return self

    def pause(self):
        """Add program pause.

        Returns:
            Self for chaining.
        """
        self._add("M0")
        return self

    def end(self):
        """End program.

        Returns:
            Self for chaining.
        """
        self._add("M5")   # Stop spindle
        self._add("M30")  # End program
        return self

    def to_string(self):
        """Return G-code as a single string.

        Returns:
            Newline-joined G-code lines.
        """
        return "\n".join(self._code_lines)

    def save_gcode(self, filepath=None):
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

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
