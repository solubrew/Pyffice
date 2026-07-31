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
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, Dict, List, Any

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeUnit
from pyffice.items.colors import PyfficeColor

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()
# ====================================================================================================================||
pxcfg = join(here, "_data_", "script.yaml")


class TextAlignment(Enum):
    """Text alignment options."""

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class TextCase(Enum):
    """Text case options."""

    UPPER = "upper"
    LOWER = "lower"
    TITLE = "title"
    SENTENCE = "sentence"
    TOGGLE = "toggle"


@dataclass
class PyfficeFont:
    """Font definition for text formatting."""

    name: str = "Arial"
    size: float = 11.0
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False
    color: Optional[str] = None
    highlight: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert font to dictionary."""
        return {
            "name": self.name,
            "size": self.size,
            "bold": self.bold,
            "italic": self.italic,
            "underline": self.underline,
            "strikethrough": self.strikethrough,
            "color": self.color,
            "highlight": self.highlight,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PyfficeFont":
        """Create font from dictionary."""
        return cls(
            name=data.get("name", "Arial"),
            size=data.get("size", 11.0),
            bold=data.get("bold", False),
            italic=data.get("italic", False),
            underline=data.get("underline", False),
            strikethrough=data.get("strikethrough", False),
            color=data.get("color"),
            highlight=data.get("highlight"),
        )


@dataclass
class PyfficeRun:
    """A text run with formatting."""

    text: str
    font: Optional[PyfficeFont] = None
    style: Optional[str] = None

    def __post_init__(self):
        if self.font is None:
            self.font = PyfficeFont()


@dataclass
class PyfficeParagraph:
    """A paragraph with text runs."""

    runs: List[PyfficeRun] = field(default_factory=list)
    alignment: TextAlignment = TextAlignment.LEFT
    spacing_before: float = 0.0
    spacing_after: float = 0.0
    line_spacing: float = 1.0
    indent_left: float = 0.0
    indent_right: float = 0.0
    first_line_indent: float = 0.0
    style: Optional[str] = None
    numbering: Optional[Dict[str, Any]] = None

    def add_run(self, text: str, font: Optional[PyfficeFont] = None) -> PyfficeRun:
        """Add a text run to this paragraph."""
        run = PyfficeRun(text=text, font=font)
        self.runs.append(run)
        return run

    @property
    def text(self) -> str:
        """Get full text of paragraph."""
        return "".join(run.text for run in self.runs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert paragraph to dictionary."""
        return {
            "text": self.text,
            "runs": [{"text": r.text, "font": r.font.to_dict() if r.font else None} for r in self.runs],
            "alignment": self.alignment.value,
            "spacing": {
                "before": self.spacing_before,
                "after": self.spacing_after,
                "line": self.line_spacing,
            },
            "indent": {
                "left": self.indent_left,
                "right": self.indent_right,
                "first_line": self.first_line_indent,
            },
            "style": self.style,
            "numbering": self.numbering,
        }


class PyfficeText(PyfficeUnit):
    SERIALIZATION_VERSION = (1, 0, 0)
    """Pyffice Text object consists of one string of text that can be formated in various ways by setting the selections"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeText")).override(cfg)
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
            "size": font.get("size", self.config.dikt.get("font", {}).get("size", None)),
            "color": self.color,
            "background": self.color_background,
            "highlight": self.color_foreground,
            "style": font.get("style", self.config.dikt.get("font", {}).get("style", None)),
            "bold": font.get("bold", self.config.dikt.get("font", {}).get("bold", None)),
            "italic": font.get("italic", self.config.dikt.get("font", {}).get("italic", None)),
            "underline": font.get("underline", self.config.dikt.get("font", {}).get("underline", None)),
            "subscript": font.get("subscript", self.config.dikt.get("font", {}).get("subscript", None)),
            "superscript": font.get("superscript", self.config.dikt.get("font", {}).get("superscript", None)),
        }
        if font != self.font:
            # logma.info(f"Set Font: {font}")
            self.add_change("font", self.font, font)
            self.font = font if font is not None else self.config.dikt.get("font", {})
        return self

    def set_font_color(self, font=None):
        """"""
        cfg = {"color": font.get("color", self.config.dikt.get("font", {}).get("color", None))}
        color = PyfficeColor(cfg)
        color.load_unit()
        if color != self.color:
            self.add_change("color", self.color, color)
            self.color = color
        return self

    def set_color_background(self, font):
        """"""
        cfg = {"color": font.get("color", self.config.dikt.get("font", {}).get("color", None))}
        color = PyfficeColor(cfg)
        color.load_unit()
        if color != self.color:
            self.add_change("color", self.color, color)
            self.color_background = color
        return self

    def set_color_foreground(self, font):
        """"""
        cfg = {"color": font.get("color", self.config.dikt.get("font", {}).get("color", None))}
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
        if self.color is None:
            self.color = PyfficeColor("black")
        if self.font is None:
            self.font = {}
        self.font["color"] = self.color.to_dict()
        if self.color_background is None:
            self.color_background = PyfficeColor("white")
        self.font["background"] = self.color_background.to_dict()
        if self.color_foreground is None:
            self.color_foreground = PyfficeColor("white")
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

    # def add_text(
    #     self,
    #     text: str,
    #     font: Optional[PyfficeFont] = None,
    #     alignment: TextAlignment = TextAlignment.LEFT,
    # ) -> "PyfficeText":
    #     """Add text as a new paragraph (fluent interface)."""
    #     self.add_paragraph(text, alignment, font)
    #     return self
    #
    # @property
    # def text(self) -> str:
    #     """Get full text content."""
    #     return "\n".join(para.text for para in self.paragraphs)
    #
    # def to_dict(self) -> Dict[str, Any]:
    #     """Convert text to dictionary."""
    #     return {
    #         "paragraphs": [p.to_dict() for p in self.paragraphs],
    #         "default_font": self.default_font.to_dict(),
    #     }

    def to_markdown(self) -> str:
        """Convert to Markdown format."""
        lines = []
        for para in self.paragraphs:
            text = para.text
            if para.alignment == TextAlignment.CENTER:
                text = f"<center>{text}</center>"
            elif para.alignment == TextAlignment.RIGHT:
                text = f"<right>{text}</right>"
            lines.append(text)
        return "\n\n".join(lines)


class PyfficeHTML(PyfficeText):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("")).override(cfg)


class PyfficePage(PyfficeUnit):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(pxcfg).select("PyfficePage").override(cfg)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
