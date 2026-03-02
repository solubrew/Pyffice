# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
Pyffice Presentation Module.

This module provides the PyfficePresentation class for handling PowerPoint (.pptx) files
within the Pyffice framework.

Key Classes:
    - PyfficePresentation: Main class for presentation documents
    - PyfficeSlideShow: Container for multiple presentations
    
Features:
    - Load and save .pptx files
    - Add slides with titles and content
    - Add images, shapes, and tables
    - JSON Schema support for AI agents
"""

__all__ = ["PyfficePresentation", "PyfficeSlideShow"]

from os.path import abspath, dirname, join
from typing import Any, Optional

# ======================================3rd Party Library Modules=====================================================||
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pyffice.document import PyfficeDocument

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "presentation.yaml")


class PyfficeSlideShow:
    """Container for multiple presentations (slideshow)."""
    
    VERSION = "0.0.1.0.1.0"
    
    def __init__(self, cfg=None):
        """Initialize a slideshow container.
        
        Args:
            cfg: Optional configuration dictionary.
        """
        self.cfg = cfg or {}
        self.presentations = {}
        self.active_presentation = None
    
    def add_presentation(self, name: str, presentation: "PyfficePresentation") -> "PyfficeSlideShow":
        """Add a presentation to the slideshow.
        
        Args:
            name: Name for the presentation.
            presentation: PyfficePresentation instance.
        
        Returns:
            self: For method chaining.
        """
        self.presentations[name] = presentation
        return self
    
    def get_presentation(self, name: str) -> Optional["PyfficePresentation"]:
        """Get a presentation by name.
        
        Args:
            name: Name of the presentation.
        
        Returns:
            PyfficePresentation or None.
        """
        return self.presentations.get(name)


class PyfficePresentation(PyfficeDocument):
    """Pyffice Presentation handles PowerPoint (.pptx) files within the Pyffice framework.
    
    This class provides methods for creating, loading, and manipulating presentation
    documents. It supports adding slides, text, images, shapes, and tables.
    
    Attributes:
        VERSION: Version string for the class format.
        pptx: The underlying python-pptx Presentation object.
        slides: List of slide data dictionaries.
        file_path: Path to the .pptx file.
    
    Example:
        >>> pres = PyfficePresentation()
        >>> pres.set_name("My Presentation")
        >>> pres.add_slide(title="Welcome", content="Hello World!")
        >>> pres.save("presentation.pptx")
    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """Initialize a new PyfficePresentation.
        
        Args:
            cfg: Optional configuration dictionary. Defaults to None.
        """
        super().__init__(cfg)
        self.config = condor.Instruct(pxcfg).select("PyfficeSlideShow").override(cfg or {})
        self.pptx = None
        self.slides = []
        self.file_path = None
        self.slide_width = Inches(10)
        self.slide_height = Inches(7.5)
        self._initialize_pptx()

    def _initialize_pptx(self):
        """Initialize a new blank presentation."""
        self.pptx = Presentation()
        self.pptx.slide_width = self.slide_width
        self.pptx.slide_height = self.slide_height

    def add_image(self, slide_index: int, image_path: str, 
                  left: float = 1, top: float = 1, 
                  width: float = 4, height: float = 3) -> "PyfficePresentation":
        """Add an image to a slide.
        
        Args:
            slide_index: Index of the slide (0-based).
            image_path: Path to the image file.
            left: Left position in inches. Defaults to 1.
            top: Top position in inches. Defaults to 1.
            width: Width in inches. Defaults to 4.
            height: Height in inches. Defaults to 3.
        
        Returns:
            self: Returns self for method chaining.
        """
        slide = self.pptx.slides[slide_index]
        slide.shapes.add_picture(
            image_path,
            Inches(left), Inches(top),
            width=Inches(width), height=Inches(height)
        )
        return self

    def add_slide(self, title: str = None, content: str = None,
                  layout_index: int = 1) -> int:
        """Add a new slide to the presentation.
        
        Args:
            title: Optional title for the slide. Defaults to None.
            content: Optional content/text for the slide. Defaults to None.
            layout_index: Slide layout index (0=title only, 1=title+content, etc.)
        
        Returns:
            int: Index of the newly added slide.
        
        Example:
            >>> pres = PyfficePresentation()
            >>> pres.add_slide(title="Welcome", content="Hello everyone!")
            >>> pres.add_slide(title="Agenda", content="- Item 1\\n- Item 2")
        """
        slide_layout = self.pptx.slide_layouts[layout_index]
        slide = self.pptx.slides.add_slide(slide_layout)
        
        # Set title if provided
        if title and slide.shapes.title:
            slide.shapes.title.text = title
        
        # Set content if provided
        if content:
            content_shape = slide.placeholders[1]
            content_shape.text = content
        
        slide_index = len(self.pptx.slides) - 1
        self.slides.append({
            "index": slide_index,
            "title": title,
            "content": content,
        })
        
        return slide_index

    def add_table(self, slide_index: int, data: list,
                  left: float = 1, top: float = 2,
                  width: float = 8, height: float = 3) -> "PyfficePresentation":
        """Add a table to a slide.
        
        Args:
            slide_index: Index of the slide (0-based).
            data: List of lists representing table rows and cells.
            left: Left position in inches. Defaults to 1.
            top: Top position in inches. Defaults to 2.
            width: Width in inches. Defaults to 8.
            height: Height in inches. Defaults to 3.
        
        Returns:
            self: Returns self for method chaining.
        
        Example:
            >>> pres.add_table(0, [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]])
        """
        if not data:
            return self
        
        rows = len(data)
        cols = len(data[0]) if data else 0
        
        slide = self.pptx.slides[slide_index]
        table = slide.shapes.add_table(rows, cols, Inches(left), Inches(top),
                                       Inches(width), Inches(height)).table
        
        # Populate table cells
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                table.cell(i, j).text = str(cell)
        
        return self

    def add_text_box(self, slide_index: int, text: str,
                     left: float = 1, top: float = 1,
                     width: float = 8, height: float = 1) -> "PyfficePresentation":
        """Add a text box to a slide.
        
        Args:
            slide_index: Index of the slide (0-based).
            text: Text content for the text box.
            left: Left position in inches. Defaults to 1.
            top: Top position in inches. Defaults to 1.
            width: Width in inches. Defaults to 8.
            height: Height in inches. Defaults to 1.
        
        Returns:
            self: Returns self for method chaining.
        """
        slide = self.pptx.slides[slide_index]
        txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                         Inches(width), Inches(height))
        tf = txBox.text_frame
        tf.text = text
        return self

    def get_slide(self, index: int) -> Optional[dict]:
        """Get slide data by index.
        
        Args:
            index: Slide index (0-based).
        
        Returns:
            dict: Slide data including title and content, or None if not found.
        """
        if 0 <= index < len(self.slides):
            return self.slides[index]
        return None

    def get_slide_count(self) -> int:
        """Get the number of slides in the presentation.
        
        Returns:
            int: Number of slides.
        """
        return len(self.pptx.slides)

    def load_document(self, document: Optional[dict] = None) -> "PyfficePresentation":
        """Load presentation data from a dictionary.
        
        Args:
            document: Dictionary containing presentation data. Defaults to None.
        
        Returns:
            self: Returns self for method chaining.
        """
        super().load_document(document)
        
        if document:
            self.slides = document.get("slides", [])
            self.file_path = document.get("file_path", None)
            
            # Load from file if path provided
            if self.file_path:
                self.open_file(self.file_path)
        
        return self

    def open_file(self, file_path: str) -> "PyfficePresentation":
        """Open and load a .pptx file.
        
        Args:
            file_path: Path to the .pptx file.
        
        Returns:
            self: Returns self for method chaining.
        
        Raises:
            FileNotFoundError: If the file does not exist.
        """
        self.file_path = file_path
        self.pptx = Presentation(file_path)
        
        # Rebuild slides list
        self.slides = []
        for i, slide in enumerate(self.pptx.slides):
            title = ""
            content = ""
            
            if slide.shapes.title:
                title = slide.shapes.title.text
            
            # Try to get content from placeholder
            if len(slide.placeholders) > 1:
                content = slide.placeholders[1].text
            
            self.slides.append({
                "index": i,
                "title": title,
                "content": content,
            })
        
        return self

    def save(self, path: str = None, format_: str = None) -> "PyfficePresentation":
        """Save the presentation to a file.
        
        Args:
            path: File path to save to. Defaults to self.file_path.
            format_: Format type (currently ignored, .pptx is default).
        
        Returns:
            self: Returns self for method chaining.
        """
        save_path = path or self.file_path
        
        if save_path:
            self.pptx.save(save_path)
            self.file_path = save_path
            self.set_saved(True)
        
        return self

    def set_title_slide(self, title: str, subtitle: str = None) -> "PyfficePresentation":
        """Add a title slide to the presentation.
        
        Args:
            title: Main title text.
            subtitle: Optional subtitle text.
        
        Returns:
            self: Returns self for method chaining.
        """
        slide_layout = self.pptx.slide_layouts[0]  # Title slide layout
        slide = self.pptx.slides.add_slide(slide_layout)
        
        if slide.shapes.title:
            slide.shapes.title.text = title
        
        if subtitle and len(slide.placeholders) > 1:
            slide.placeholders[1].text = subtitle
        
        return self

    def to_dict(self) -> dict:
        """Convert the presentation to a dictionary.
        
        Returns:
            dict: Dictionary representation of the presentation.
        """
        doc = super().to_dict()
        doc["document_type"] = "presentation"
        doc["slides"] = self.slides
        doc["slide_count"] = self.get_slide_count()
        return doc

    def to_json_schema(self) -> dict:
        """Convert the presentation to JSON Schema format.
        
        Returns:
            dict: JSON Schema representation of the presentation.
        """
        schema = super().to_json_schema()
        schema["title"] = self.name or "PyfficePresentation"
        schema["properties"].update({
            "slides": {
                "type": "array",
                "description": "List of slides in the presentation",
                "items": {
                    "type": "object",
                    "properties": {
                        "index": {"type": "integer"},
                        "title": {"type": "string"},
                        "content": {"type": "string"},
                    }
                }
            },
            "slide_count": {"type": "integer", "description": "Number of slides"},
        })
        return schema


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
