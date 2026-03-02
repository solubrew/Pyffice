"""
Pyffice PPTX Module - Read/Write PowerPoint files
"""

from typing import List, Dict, Any, Optional
from pathlib import Path


class PyfficePPTX:
    """Handle PowerPoint file operations"""
    
    SUPPORTED_EXTENSIONS = ['.pptx', '.pptm']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate()
        self._presentation = None
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def _import_pptx(self):
        """Lazy import python-pptx"""
        try:
            from pptx import Presentation
            from pptx.util import Inches, Pt
            return Presentation
        except ImportError:
            raise ImportError("python-pptx required: pip install python-pptx")
    
    def read(self) -> Dict[str, Any]:
        """Read PPTX and return structured data"""
        Presentation = self._import_pptx()
        prs = Presentation(self.file_path)
        
        slides_data = []
        for i, slide in enumerate(prs.slides):
            slide_data = {
                'slide_number': i + 1,
                'shapes': []
            }
            for shape in slide.shapes:
                shape_data = {
                    'type': shape.shape_type,
                    'name': shape.name,
                }
                if hasattr(shape, 'text'):
                    shape_data['text'] = shape.text
                if hasattr(shape, 'top'):
                    shape_data['top'] = shape.top
                    shape_data['left'] = shape.left
                    shape_data['width'] = shape.width
                    shape_data['height'] = shape.height
                slide_data['shapes'].append(shape_data)
            slides_data.append(slide_data)
        
        return {'slides': slides_data, 'slide_count': len(slides_data)}
    
    def write(self, slides_data: List[Dict[str, Any]], output_path: Optional[str] = None):
        """Write data to PPTX file"""
        Presentation = self._import_pptx()
        prs = Presentation()
        
        for slide_data in slides_data:
            slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
            
            for shape_data in slide_data.get('shapes', []):
                from pptx.util import Inches, Pt
                from pptx.enum.shapes import MSO_SHAPE
                
                if 'text' in shape_data:
                    textbox = slide.shapes.add_textbox(
                        Inches(shape_data.get('left', 1)),
                        Inches(shape_data.get('top', 1)),
                        Inches(shape_data.get('width', 4)),
                        Inches(shape_data.get('height', 1))
                    )
                    textbox.text = shape_data['text']
        
        output = Path(output_path) if output_path else self.file_path
        prs.save(str(output))
    
    def extract_text(self) -> List[str]:
        """Extract all text from presentation"""
        Presentation = self._import_pptx()
        prs = Presentation(self.file_path)
        
        texts = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, 'text'):
                    texts.append(shape.text)
        return texts


def read_pptx(file_path: str) -> Dict[str, Any]:
    """Convenience function to read PPTX"""
    return PyfficePPTX(file_path).read()


def write_pptx(file_path: str, slides_data: List[Dict[str, Any]], **kwargs):
    """Convenience function to write PPTX"""
    PyfficePPTX(file_path).write(slides_data, **kwargs)


def extract_pptx_text(file_path: str) -> List[str]:
    """Convenience function to extract text from PPTX"""
    return PyfficePPTX(file_path).extract_text()
