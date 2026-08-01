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
from pyffice.document import PyfficeUnit
from pyffice.items.colors import PyfficeColor
from pyffice.items.text import PyfficeText
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "shapes.yaml")


class PyfficeShape(PyfficeUnit):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeShape")).override(cfg)
        self.background_color = None
        self.corner = None
        self.origin = None
        self.shapes = None
        self.size = None
        self.texts = None

    def add_shape(self, shape) -> Self:
        """Add a shape.
        
        Args:
            shape: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {}
        self.shapes[shape] = PyfficeShape(cfg)
        return self

    def add_text(self, text, position=None) -> Self:
        """Add a text.
        
        Args:
            text: Parameter.
            position: Parameter.
        
        Returns:
            Self for chaining.
        """
        if position is None:
            position = self.origin
        text = PyfficeText({"text": text, "position": position})
        if text != self.texts.get(str(position), None):
            self.add_change("text", self.texts.get(position, None), text)
        self.texts[str(position)] = text
        return self

    def load_unit(self, unit=None) -> Self:
        """Load a unit dict into this document.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Load Unit {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        self.set_background(unit.get("background", None))
        self.set_origin(unit.get("origin", [0, 0]))
        self.set_size(unit.get("size", [100, 100]))
        self.set_shapes(unit.get("shapes", []))
        return self

    def mirror_shape(self, axis) -> Self:
        """Mirror shape.
        
        Args:
            axis: Parameter.
        
        Returns:
            Self for chaining.
        """
        if axis == "x":
            self.set_origin([-self.origin[0], self.origin[1]])
            self.set_size([-self.size[0], self.size[1]])
        elif axis == "y":
            self.set_origin([self.origin[0], -self.origin[1]])
            self.set_size([self.size[0], -self.size[1]])
        return self

    def mirror_text(self) -> Self:
        """Mirror text horizontally."""
        self.text_flipped = not getattr(self, 'text_flipped', False)
        return self

    def move_shape(self, x, y) -> Self:
        """Move shape by offset."""
        self.set_origin([self.origin[0] + x, self.origin[1] + y])
        return self

    def move_text(self, x, y) -> Self:
        """Move text by offset."""
        self.text_offset = (x, y)
        return self

    def rotate_shape(self, axis, angle) -> Self:
        """Rotate shape."""
        if axis == "x":
            self.set_origin([-self.origin[1], self.origin[0]])
            self.set_size([-self.size[1], self.size[0]])
        elif axis == "y":
            self.set_origin([self.origin[0], -self.origin[1]])
            self.set_size([self.size[0], -self.size[1]])
        return self

    def rotate_text(self, axis, angle) -> Self:
        """Rotate text."""
        self.text_rotation = angle
        return self

    def set_background(self, background, item=Self) -> "PyfficeShape":
        """Set the background.
        
        Args:
            background: Parameter.
            item: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {"color": background}
        background_color = PyfficeColor(cfg)
        if item == "0":
            if background_color != self.background_color:
                self.add_change("background_color", self.background_color, background_color)
            self.background_color = background_color
        else:
            if self.shapes[item].background_color != background_color:
                self.add_change(
                    f"background_color", self.shapes[item].background_color, background_color, "assign", {"key": item}
                )
            self.shapes[item].background_color = background_color
        return self

    def set_origin(self, origin) -> Self:
        """Set the origin.
        
        Args:
            origin: Parameter.
        
        Returns:
            Self for chaining.
        """
        if origin != self.origin:
            self.add_change("origin", self.origin, origin)
        self.origin = origin
        corner = [self.origin[0] + self.size[0], self.origin[1] + self.size[1]]
        self._set_envelope(self.origin, corner)
        return self

    def set_shapes(self, shapes) -> Self:
        """Set the shapes.
        
        Args:
            shapes: Parameter.
        
        Returns:
            Self for chaining.
        """
        for shape in shapes:
            match shape:
                case "rectangle":
                    self.shape_origin = self.origin
                    self.shape_corner = self.corner
                case "circle":
                    self.shape_origin = [self.origin / 2, self.origin / 2]
                    self.shape_size = self.corner[0] - self.shape_origin[0]
                case "ellipse":
                    self.shape_origin = [self.origin / 2, self.origin / 2]
                    self.shape_size = self.corner[0] - self.shape_origin[0]
                case "triangle":
                    self.shape_origin = [self.origin / 2, self.origin / 2]
                    self.shape_size = self.corner[0] - self.shape_origin[0]
                case "polygon":
                    self.shape_origin = [self.origin / 2, self.origin / 2]
                    self.shape_size = self.corner[0] - self.shape_origin[0]
                case "trapezoid":
                    self.shape_origin = [self.origin / 2, self.origin / 2]
                    self.shape_size = self.corner[0] - self.shape_origin[0]
                case "parallelogram":
                    self.shape_origin = [self.origin / 2, self.origin / 2]
                    self.shape_size = self.corner[0] - self.shape_origin[0]
        return self

    def set_size(self, size) -> Self:
        """Set the size.
        
        Args:
            size: Parameter.
        
        Returns:
            Self for chaining.
        """
        if size != self.size:
            self.add_change("size", self.size, size)
        self.size = size
        corner = [self.origin[0] + self.size[0], self.origin[1] + self.size[1]]
        self._set_envelope(self.origin, corner)
        return self
    def _set_envelope(self, top_left, bottom_right) -> Self:
        """"""
        self.origin = top_left
        self.corner = bottom_right
        self._update_shape_sizes()
        return self

    def _update_shape_sizes(self) -> None:
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
