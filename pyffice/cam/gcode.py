"""G-code generator for CAM operations."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PyfficeGCode:
    """G-code generator for CNC operations.
    
    Provides utilities for generating and manipulating G-code for CNC machines.
    """
    
    feed_rate: float = 100.0
    spindle_speed: float = 1000.0
    tool_number: int = 1
    units: str = "mm"
    _code_lines: list[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Initialize G-code generator."""
        self._initialize()
    
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
    
    def rapid_move(self, x: float | None = None, y: float | None = None, z: float | None = None) -> "PyfficeGCode":
        """Generate rapid move (G0)."""
        cmd = "G0"
        if x is not None:
            cmd += f" X{x}"
        if y is not None:
            cmd += f" Y{y}"
        if z is not None:
            cmd += f" Z{z}"
        self._add(cmd)
        return self
    
    def linear_move(self, x: float | None = None, y: float | None = None, z: float | None = None) -> "PyfficeGCode":
        """Generate linear move (G1)."""
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
    
    def arc_cw(self, x: float, y: float, i: float, j: float) -> "PyfficeGCode":
        """Generate clockwise arc (G2)."""
        self._add(f"G2 X{x} Y{y} I{i} J{j} F{self.feed_rate}")
        return self
    
    def arc_ccw(self, x: float, y: float, i: float, j: float) -> "PyfficeGCode":
        """Generate counter-clockwise arc (G3)."""
        self._add(f"G3 X{x} Y{y} I{i} J{j} F{self.feed_rate}")
        return self
    
    def set_feed_rate(self, rate: float) -> "PyfficeGCode":
        """Set feed rate."""
        self.feed_rate = rate
        return self
    
    def set_spindle_speed(self, rpm: float) -> "PyfficeGCode":
        """Set spindle speed."""
        self.spindle_speed = rpm
        self._add(f"S{rpm}")
        return self
    
    def tool_change(self, tool: int) -> "PyfficeGCode":
        """Change tool."""
        self.tool_number = tool
        self._add(f"M6 T{tool}")
        return self
    
    def pause(self) -> "PyfficeGCode":
        """Add program pause."""
        self._add("M0")
        return self
    
    def end(self) -> "PyfficeGCode":
        """End program."""
        self._add("M5")  # Stop spindle
        self._add("M30")  # End program
        return self
    
    def to_string(self) -> str:
        """Return G-code as string."""
        return "\n".join(self._code_lines)
    
    def save(self, filepath: str) -> None:
        """Save G-code to file."""
        with open(filepath, 'w') as f:
            f.write(self.to_string())
