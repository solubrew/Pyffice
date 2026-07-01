"""
Pyffice Text Module

Text handling for documents: fonts, styles, paragraphs, and runs.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class TextAlignment(Enum):
    """Text alignment options."""
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'
    JUSTIFY = 'justify'


class TextCase(Enum):
    """Text case options."""
    UPPER = 'upper'
    LOWER = 'lower'
    TITLE = 'title'
    SENTENCE = 'sentence'
    TOGGLE = 'toggle'


@dataclass
class PyfficeFont:
    """Font definition for text formatting."""
    name: str = 'Arial'
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
            'name': self.name,
            'size': self.size,
            'bold': self.bold,
            'italic': self.italic,
            'underline': self.underline,
            'strikethrough': self.strikethrough,
            'color': self.color,
            'highlight': self.highlight,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PyfficeFont':
        """Create font from dictionary."""
        return cls(
            name=data.get('name', 'Arial'),
            size=data.get('size', 11.0),
            bold=data.get('bold', False),
            italic=data.get('italic', False),
            underline=data.get('underline', False),
            strikethrough=data.get('strikethrough', False),
            color=data.get('color'),
            highlight=data.get('highlight'),
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
        return ''.join(run.text for run in self.runs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert paragraph to dictionary."""
        return {
            'text': self.text,
            'runs': [
                {'text': r.text, 'font': r.font.to_dict() if r.font else None}
                for r in self.runs
            ],
            'alignment': self.alignment.value,
            'spacing': {
                'before': self.spacing_before,
                'after': self.spacing_after,
                'line': self.line_spacing,
            },
            'indent': {
                'left': self.indent_left,
                'right': self.indent_right,
                'first_line': self.first_line_indent,
            },
            'style': self.style,
            'numbering': self.numbering,
        }


@dataclass
class PyfficeText:
    """Container for text content with paragraphs."""
    paragraphs: List[PyfficeParagraph] = field(default_factory=list)
    default_font: PyfficeFont = field(default_factory=PyfficeFont)

    def add_paragraph(
        self,
        text: str = '',
        alignment: TextAlignment = TextAlignment.LEFT,
        font: Optional[PyfficeFont] = None,
    ) -> PyfficeParagraph:
        """Add a new paragraph."""
        para = PyfficeParagraph(alignment=alignment)
        if text:
            para.add_run(text, font or self.default_font)
        self.paragraphs.append(para)
        return para

    def add_text(
        self,
        text: str,
        font: Optional[PyfficeFont] = None,
        alignment: TextAlignment = TextAlignment.LEFT,
    ) -> 'PyfficeText':
        """Add text as a new paragraph (fluent interface)."""
        self.add_paragraph(text, alignment, font)
        return self

    @property
    def text(self) -> str:
        """Get full text content."""
        return '\n'.join(para.text for para in self.paragraphs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert text to dictionary."""
        return {
            'paragraphs': [p.to_dict() for p in self.paragraphs],
            'default_font': self.default_font.to_dict(),
        }

    def to_markdown(self) -> str:
        """Convert to Markdown format."""
        lines = []
        for para in self.paragraphs:
            text = para.text
            if para.alignment == TextAlignment.CENTER:
                text = f'<center>{text}</center>'
            elif para.alignment == TextAlignment.RIGHT:
                text = f'<right>{text}</right>'
            lines.append(text)
        return '\n\n'.join(lines)


class PyfficeTextDocument:
    """Text document with full formatting support."""

    def __init__(self):
        self.text = PyfficeText()
        self.metadata: Dict[str, Any] = {}

    def add_heading(
        self,
        text: str,
        level: int = 1,
    ) -> PyfficeParagraph:
        """Add a heading paragraph."""
        sizes = {1: 24.0, 2: 20.0, 3: 16.0, 4: 14.0, 5: 12.0, 6: 11.0}
        font = PyfficeFont(size=sizes.get(level, 14.0), bold=True)
        return self.text.add_paragraph(text, font=font)

    def add_paragraph(
        self,
        text: str,
        style: Optional[str] = None,
    ) -> PyfficeParagraph:
        """Add a regular paragraph."""
        para = self.text.add_paragraph(text)
        para.style = style
        return para

    def add_bullet(
        self,
        text: str,
        level: int = 0,
    ) -> PyfficeParagraph:
        """Add a bullet point."""
        para = self.text.add_paragraph(text)
        para.numbering = {'type': 'bullet', 'level': level}
        return para

    def add_numbered(
        self,
        text: str,
        number: int,
        level: int = 0,
    ) -> PyfficeParagraph:
        """Add a numbered item."""
        para = self.text.add_paragraph(text)
        para.numbering = {'type': 'number', 'number': number, 'level': level}
        return para

    def __str__(self) -> str:
        """Return plain text representation."""
        return self.text.text


__all__ = [
    'TextAlignment',
    'TextCase',
    'PyfficeFont',
    'PyfficeRun',
    'PyfficeParagraph',
    'PyfficeText',
    'PyfficeTextDocument',
]
