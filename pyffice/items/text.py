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
from condor import condor
from ogma.logma import Logma
from pyffice.document import PyfficeUnit
from pyffice.items.colors import PyfficeColor

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()
# ====================================================================================================================||
pxcfg = join(here, "_data_", "text.yaml")


class PyfficeText(PyfficeUnit):
    """Pyffice Text object consists of one string of text that can be formated in various ways by setting the selections"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeText")).override(cfg)
        self.alignment = None
        self.color = None
        self.color_background = None
        self.color_foreground = None
        self.data_format = None
        self.font = None
        self.horizontal = None
        self.html = None
        self.position = None
        self.reference = None
        self.value = None
        self.vertical = None

    def load_unit(self, unit=None):
        """"""
        logma.info(f"Load Unit {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        logma.info(f"Load PyfficeText {unit}")
        super().load_unit(unit)
        self.set_alignment(unit.get("alignment", self.config.dikt.get("alignment", {})))
        self.set_data_format(unit.get("data_format", self.config.dikt.get("data_format", {})))
        self.set_font(unit.get("font", self.config.dikt.get("font", {})))
        self.set_html(unit.get("html", self.config.dikt.get("html", {})))
        text = unit.get("unit", {}).get("value", None)
        if text is None:
            text = unit.get("value", "")
        self.set_text(text)
        return self

    def set_alignment(self, horizontal=None, vertical=None):
        """"""
        if horizontal is None:
            horizontal = self.config.dikt.get("alignment", {}).get("horizontal", None)
        self.horizontal = horizontal
        if vertical is None:
            vertical = self.config.dikt.get("alignment", {}).get("vertical", None)
        self.vertical = vertical
        return self

    def set_data_format(self, data_format):
        """"""
        if data_format != self.data_format:
            self.add_change("data_format", self.data_format, data_format)
            self.data_format = data_format
        return self

    def set_font(self, font):
        """Set the Default font for the Text"""
        self.set_font_color(font)
        self.set_color_background(font)
        self.set_color_foreground(font)
        font = {
            "size": font.get("size", self.config.dikt["font"].get("size", None)),
            "color": self.color,
            "background": self.color_background,
            "highlight": self.color_foreground,
            "style": font.get("style", self.config.dikt["font"].get("style", None)),
            "bold": font.get("bold", self.config.dikt["font"].get("bold", None)),
            "italic": font.get("italic", self.config.dikt["font"].get("italic", None)),
            "underline": font.get("underline", self.config.dikt["font"].get("underline", None)),
            "subscript": font.get("subscript", self.config.dikt["font"].get("subscript", None)),
            "superscript": font.get("superscript", self.config.dikt["font"].get("superscript", None)),
        }
        if font != self.font:
            # logma.info(f"Set Font: {font}")
            self.add_change("font", self.font, font)
            self.font = font if font is not None else self.config.dikt.get("font", {})
        return self

    def set_font_color(self, font=None):
        """"""
        cfg = {"color": font.get("color", self.config.dikt["font"].get("color", None))}
        color = PyfficeColor(cfg)
        color.load_unit()
        if color != self.color:
            self.add_change("color", self.color, color)
            self.color = color
        return self

    def set_color_background(self, font):
        """"""
        cfg = {"color": font.get("color", self.config.dikt["font"].get("color", None))}
        color = PyfficeColor(cfg)
        color.load_unit()
        if color != self.color:
            self.add_change("color", self.color, color)
            self.color_background = color
        return self

    def set_color_foreground(self, font):
        """"""
        cfg = {"color": font.get("color", self.config.dikt["font"].get("color", None))}
        color = PyfficeColor(cfg)
        color.load_unit()
        if color != self.color:
            self.add_change("color", self.color, color)
            self.color_foreground = color
        return self

    def set_html(self, value):
        """"""
        if value != self.html:
            self.add_change("html", self.html, value)
            self.html = value
        return self

    def set_text(self, text):
        """"""
        if text != self.value:
            self.add_change("value", self.value, text)
            self.value = text
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        self.font["color"] = self.color.to_dict()
        self.font["background"] = self.color_background.to_dict()
        self.font["highlight"] = self.color_foreground.to_dict()
        doc["unit"] = {
            "data_format": self.data_format,
            "font": self.font,
            "html": "",  # self.to_html(),
            "value": self.value,
            "alignment": {
                "horizontal": self.horizontal,
                "vertical": self.vertical,
            },
        }
        return doc

    def to_html(self):
        """"""
        text = f"<font size={self.font['size']} color={self.font['color'].to_html()} " + ">" + self.value + "</font>"
        self.html = text
        return self.html


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
