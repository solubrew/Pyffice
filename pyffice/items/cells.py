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
from os.path import abspath, dirname, join, exists
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeUnit
from pyffice.items.text import PyfficeText
from pyffice.items.colors import PyfficeColor
from pyffice.images.images import PyfficeImage

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "cells.yaml")


class PyfficeBackground(PyfficeUnit):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeBackground")).override(cfg)
        self.file_path = None
        self.image = None
        self.color = None
        self.pattern = None
        self.transparency = None

    def load_unit(self, unit):
        """"""
        logma.info(f"Load Unit {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        self.set_color(unit.get("color", None))
        self.set_image(unit.get("image", None))
        self.set_pattern(unit.get("pattern", None))
        self.set_transparency(unit.get("transparency", None))
        return self

    def set_color(self, color):
        """"""
        cfg = {"color": color}
        color = PyfficeColor(cfg)
        if color != self.color:
            self.add_change("color", self.color, color)
        self.color = color
        return self

    def set_image(self, path):
        """"""
        image = None
        if exists(path):
            cfg = {"file_path": path}
            image = PyfficeImage(cfg)
        if image != self.image:
            self.add_change("image", self.image, image)
        self.image = image
        self.file_path = self.image.file_path
        return self

    def set_pattern(self, pattern):
        """"""
        return self

    def set_transparency(self, transparency):
        """"""
        if transparency != self.transparency:
            self.add_change("transparency", self.transparency, transparency)
        self.transparency = transparency
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"] = {
            "color": self.color.to_dict() if self.color is not None else None,
            "image": self.image.to_dict() if self.image is not None else None,
            "pattern": self.pattern,
            "transparency": self.transparency,
        }
        return doc


class PyfficeCell(PyfficeUnit):
    """"""

    def __init__(self, cfg=None):
        """"""
        logma.info(f"Address Initiated")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeCell")).override(cfg)
        self.parent = self.config.dikt.get("parent", None)
        logma.info(f"Address Initiated")
        self.address = None
        self.background = None
        self.border_style = None
        self.border_size = None
        self.border_color = None
        self.format = None
        self.formula = None
        self.formula_inputs = None
        self.horizontal = None
        self.object = None
        self.value = None
        self.vertical = None
        self.selections = None
        self.transparency = None

    def evaluate(self):
        """"""
        formula = self.get_formula()
        inputs = self.get_inputs()
        self.parent.compiler.evaluate(formula, inputs)

    def get_format(self):
        """
        :return:
        """
        format_ = {
            "font": {"size": self.value.font_size, "color": self.value.font_color, "style": self.value.font_style},
            "selections": self.selections,
            "border": {
                "top": {
                    "style": self.border_style.get("top", None),
                    "size": self.border_size.get("top", None),
                    "color": self.border_color.get("top", None),
                },
                "bottom": {
                    "style": self.border_style.get("bottom", None),
                    "size": self.border_size.get("bottom", None),
                    "color": self.border_color.get("bottom", None),
                },
                "left": {
                    "style": self.border_style.get("left", None),
                    "size": self.border_size.get("left", None),
                    "color": self.border_color.get("left", None),
                },
                "right": {
                    "style": self.border_style.get("right", None),
                    "size": self.border_size.get("right", None),
                    "color": self.border_color.get("right", None),
                },
            },
            "background": {
                "color": self.background.color,
                "transparency": self.background.transparency,
                "pattern": self.background.pattern,
            },
            "alignment": {"horizontal": self.horizontal, "vertical": self.vertical},
            "data_format": self.value.data_format,
        }
        return format_

    def get_formula(self):
        """"""
        return self

    def get_inputs(self):
        """"""
        return self.formula_inputs

    def get_value(self):
        """"""
        return self

    def load_unit(self, unit):
        """"""
        logma.info(f"Load Unit {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        logma.info("Pyffice Cell Loaded")
        self.set_address(unit.get("address", "I|0"))
        self.set_background(unit.get("background", None))
        self.set_border_size(unit.get("border_size", None), unit.get("border_position", None))
        self.set_border_color(unit.get("border_color", None), unit.get("border_position", None))
        self.set_border_style(unit.get("border_style", None), unit.get("border_position", None))
        self.set_format(unit.get("format", None))
        self.set_formula(unit.get("formula", None))
        self.set_value(unit.get("value", None))
        self.set_object(unit.get("object", None))
        logma.info("Pyffice Cell Loaded")
        return self

    def set_address(self, address):
        """"""
        logma.info(self)
        logma.info(f"{self.__dir__()})")
        if address != self.address:
            self.add_change("address", self.address, address)
            self.address = address
        return self

    def set_background(self, background):
        """"""
        cfg = {"background": background}
        background = PyfficeUnit(cfg)
        if background != self.background:
            self.add_change("background", self.background, background)
        self.background = background
        return self

    def set_border_size(self, size, position="top"):
        """"""
        if self.border_size is None:
            self.border_size = {}
        self.add_change("border_size", self.border_size, size, "assign")
        self.border_size[position] = size
        return self

    def set_border_color(self, color, position="top"):
        """"""
        if self.border_color is None:
            self.border_color = {}
        self.add_change("border_color", self.border_color, color, "assign")
        self.border_color[position] = color
        return self

    def set_border_style(self, style, position="top"):
        """"""
        if self.border_style is None:
            self.border_style = {}
        self.add_change("border_size", self.border_style, style, "assign")
        self.border_style[position] = style
        return self

    def set_format(self, format_):
        """"""
        return self

    def set_formula(self, formula, inputs=None):
        """"""
        if formula != self.formula:
            self.add_change("formula", self.formula, formula)
        self.formula = formula
        if inputs != self.formula_inputs:
            self.add_change("formula_inputs", self.formula_inputs, inputs)
        self.formula_inputs = inputs
        return self

    def set_object(self, object_):
        """"""
        return self

    def set_value(self, value, font=None):
        """"""
        value = PyfficeText({"text": value, "font": font})
        if value != self.value:
            self.add_change("value", self.value, value)
        self.value = value
        return self

    def set_transparency(self, transparency):
        """"""
        if transparency != self.transparency:
            self.add_change("transparency", self.transparency, transparency)
        self.transparency = transparency
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"]["address"] = self.address
        doc["unit"]["background"] = self.background.to_dict()
        doc["unit"]["format"] = self.format
        doc["unit"]["formula"] = self.formula
        doc["unit"]["object"] = self.object
        if self.value is not None:
            doc["unit"]["value"] = self.value.to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
