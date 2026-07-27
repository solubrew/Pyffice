# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Presentation Ports Module
	description: >
		External presentation format ports - converts all external presentation formats to/from
		PyfficePresentation. Includes PPTX, PPT, ODP, Key and other formats.
	version: 0.0.1.0.1.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from typing import Dict, Any, Optional, List
from pathlib import Path
from abc import ABC, abstractmethod

# ======================================3rd Party Library Modules=====================================================||
from pptx import Presentation
from pptx.util import Inches

# ======================================Solutions Brewer Library Modules==============================================||
from pyffice.presentation.presentation import PyfficePresentation
from pyffice.document import PyfficeDocument


# ====================================================================================================================||


class PresentationPort(ABC):
    """Abstract base class for presentation format ports"""
    
    EXTENSIONS: set = set()
    
    @abstractmethod
    def import_file(self, file_path: str) -> PyfficePresentation:
        """Import presentation file to PyfficePresentation"""
        pass
    
    @abstractmethod
    def export_file(self, presentation: PyfficePresentation, file_path: str) -> None:
        """Export PyfficePresentation to presentation file format"""
        pass


class PPTXPort(PresentationPort):
    """Microsoft PowerPoint PPTX format port"""
    
    EXTENSIONS = {'.pptx', '.PPTX'}
    
    def import_file(self, file_path: str) -> PyfficePresentation:
        """Import PPTX to PyfficePresentation"""
        path = Path(file_path)
        
        pres = PyfficePresentation()
        pres.open_file(str(path))
        pres.document['source_format'] = 'pptx'
        
        return pres
    
    def export_file(self, presentation: PyfficePresentation, file_path: str) -> None:
        """Export PyfficePresentation to PPTX"""
        path = Path(file_path)
        
        # Use the underlying pptx object
        if presentation.pptx:
            presentation.pptx.save(str(path))


class PptPort(PresentationPort):
    """Microsoft PowerPoint PPT (legacy) format port"""
    
    EXTENSIONS = {'.ppt', '.PPT'}
    
    def import_file(self, file_path: str) -> PyfficePresentation:
        """Import PPT to PyfficePresentation"""
        path = Path(file_path)
        
        pres = PyfficePresentation()
        pres.document['source_format'] = 'ppt'
        pres.document['note'] = 'PPT legacy format - convert to PPTX for full support'
        
        # Note: python-pptx only supports .pptx, not legacy .ppt
        # For full support, would need python-ppt or unoconv
        
        return pres
    
    def export_file(self, presentation: PyfficePresentation, file_path: str) -> None:
        """Export PyfficePresentation to PPT"""
        path = Path(file_path)
        
        # Export as PPTX first, then convert if needed
        # For now, save as PPTX
        pptx_path = str(path).replace('.ppt', '.pptx')
        if presentation.pptx:
            presentation.pptx.save(pptx_path)


class ODPPort(PresentationPort):
    """OpenDocument Presentation format port"""
    
    EXTENSIONS = {'.odp', '.ODP'}
    
    def import_file(self, file_path: str) -> PyfficePresentation:
        """Import ODP to PyfficePresentation"""
        path = Path(file_path)
        
        pres = PyfficePresentation()
        pres.create_new_document(path.stem)
        
        pres.document['source_format'] = 'odp'
        pres.document['note'] = 'ODP import requires odfpy'
        
        try:
            from odf import text, style
            from odf.opendocument import load
            
            doc = load(str(path))
            
            slides = []
            for para in doc.getElementsByType(text.P):
                if para.firstChild:
                    slides.append({'content': para.firstChild.data})
            
            pres.document['slides'] = slides
        except ImportError:
            pres.document['error'] = 'odfpy not installed'
        
        return pres
    
    def export_file(self, presentation: PyfficePresentation, file_path: str) -> None:
        """Export PyfficePresentation to ODP"""
        path = Path(file_path)
        
        try:
            from odf.opendocument import OpenDocumentPresentation
            from odf.text import P
            
            doc = OpenDocumentPresentation()
            
            # Add slides
            for slide_data in presentation.slides:
                p = P()
                if slide_data.get('title'):
                    p.addText(slide_data['title'])
                if slide_data.get('content'):
                    p.addText('\n' + slide_data['content'])
                doc.text.addElement(p)
            
            doc.save(str(path))
        except ImportError:
            raise ImportError("odfpy required for ODP export: pip install odfpy")


class KeyPort(PresentationPort):
    """Apple Keynote format port"""
    
    EXTENSIONS = {'.key', '.KEY'}
    
    def import_file(self, file_path: str) -> PyfficePresentation:
        """Import Keynote to PyfficePresentation"""
        path = Path(file_path)
        
        pres = PyfficePresentation()
        pres.create_new_document(path.stem)
        
        pres.document['source_format'] = 'key'
        pres.document['note'] = 'Keynote import requires apple-keynote or unoconv'
        
        # Keynote is a bundle, complex to parse
        # Would need unoconv or similar
        
        return pres
    
    def export_file(self, presentation: PyfficePresentation, file_path: str) -> None:
        """Export PyfficePresentation to Keynote"""
        # Export as PPTX - Keynote can import PPTX
        pptx_path = str(path).replace('.key', '.pptx')
        if presentation.pptx:
            presentation.pptx.save(pptx_path)


class PresentationPortsManager:
    """Manages all presentation format ports and conversions"""
    
    def __init__(self):
        self.ports: Dict[str, PresentationPort] = {}
        self._register_default_ports()
    
    def _register_default_ports(self):
        """Register all default presentation ports"""
        self.ports['pptx'] = PPTXPort()
        self.ports['ppt'] = PptPort()
        self.ports['odp'] = ODPPort()
        self.ports['key'] = KeyPort()
    
    def register_port(self, format_name: str, port: PresentationPort) -> None:
        """Register a new presentation format port"""
        self.ports[format_name] = port
    
    def get_port(self, format_name: str) -> Optional[PresentationPort]:
        """Get port for a specific format"""
        return self.ports.get(format_name.lower())
    
    def import_file(self, file_path: str) -> PyfficePresentation:
        """Import any supported presentation file to PyfficePresentation"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for port in self.ports.values():
            if ext in port.EXTENSIONS:
                return port.import_file(str(path))
        
        raise ValueError(f"Unsupported presentation format: {ext}")
    
    def export_file(self, presentation: PyfficePresentation, file_path: str, format_name: str = None) -> None:
        """Export PyfficePresentation to specified format"""
        path = Path(file_path)
        
        if format_name is None:
            format_name = path.suffix.lower().lstrip('.')
        
        port = self.ports.get(format_name.lower())
        if port is None:
            raise ValueError(f"Unsupported presentation format: {format_name}")
        
        port.export_file(presentation, str(path))
    
    def convert(self, input_path: str, output_path: str) -> PyfficePresentation:
        """Convert between presentation formats"""
        pres = self.import_file(input_path)
        self.export_file(pres, output_path)
        return pres
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported format extensions"""
        formats = set()
        for port in self.ports.values():
            formats.update(port.EXTENSIONS)
        return sorted(list(formats))


# Global port manager instance
_port_manager = None

def get_ports_manager() -> PresentationPortsManager:
    """Get global presentation ports manager instance"""
    global _port_manager
    if _port_manager is None:
        _port_manager = PresentationPortsManager()
    return _port_manager


def import_presentation(file_path: str) -> PyfficePresentation:
    """Convenience function to import presentation file"""
    return get_ports_manager().import_file(file_path)


def export_presentation(presentation: PyfficePresentation, file_path: str) -> None:
    """Convenience function to export presentation file"""
    get_ports_manager().export_file(presentation, file_path)


def convert_presentation(input_path: str, output_path: str) -> PyfficePresentation:
    """Convenience function to convert between presentation formats"""
    return get_ports_manager().convert(input_path, output_path)


# ====================================================================================================================||
