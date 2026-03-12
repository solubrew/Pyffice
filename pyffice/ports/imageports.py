# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Image Ports Module
	description: >
		External image format ports - converts all external image formats to/from
		PyfficeImage. Includes PNG, JPEG, GIF, BMP, WebP, TIFF, SVG and other formats.
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
from PIL import Image

# ======================================Solutions Brewer Library Modules==============================================||
from pyffice.images.images import PyfficeImage
from pyffice.document import PyfficeDocument


# ====================================================================================================================||


class ImagePort(ABC):
    """Abstract base class for image format ports"""
    
    EXTENSIONS: set = set()
    
    @abstractmethod
    def import_file(self, file_path: str) -> PyfficeImage:
        """Import image file to PyfficeImage"""
        pass
    
    @abstractmethod
    def export_file(self, image: PyfficeImage, file_path: str) -> None:
        """Export PyfficeImage to image file format"""
        pass


class PNGPort(ImagePort):
    """Portable Network Graphics (PNG) format port"""
    
    EXTENSIONS = {'.png', '.PNG'}
    
    def import_file(self, file_path: str) -> PyfficeImage:
        """Import PNG to PyfficeImage"""
        path = Path(file_path)
        
        img = Image.open(path)
        
        image = PyfficeImage({'path': str(path)})
        image.create_new_document(path.stem)
        
        image.document['width'] = img.width
        image.document['height'] = img.height
        image.document['mode'] = img.mode
        image.document['format'] = 'PNG'
        image.document['source_format'] = 'png'
        
        return image
    
    def export_file(self, image: PyfficeImage, file_path: str) -> None:
        """Export PyfficeImage to PNG"""
        path = Path(file_path)
        
        if image.image:
            image.image.save(str(path), 'PNG')


class JPEGPort(ImagePort):
    """Joint Photographic Experts Group (JPEG) format port"""
    
    EXTENSIONS = {'.jpg', '.jpeg', '.JPG', '.JPEG'}
    
    def import_file(self, file_path: str) -> PyfficeImage:
        """Import JPEG to PyfficeImage"""
        path = Path(file_path)
        
        img = Image.open(path)
        
        image = PyfficeImage({'path': str(path)})
        image.create_new_document(path.stem)
        
        image.document['width'] = img.width
        image.document['height'] = img.height
        image.document['mode'] = img.mode
        image.document['format'] = 'JPEG'
        image.document['source_format'] = 'jpeg'
        
        return image
    
    def export_file(self, image: PyfficeImage, file_path: str) -> None:
        """Export PyfficeImage to JPEG"""
        path = Path(file_path)
        
        if image.image:
            image.image.save(str(path), 'JPEG')


class GIFPort(ImagePort):
    """Graphics Interchange Format (GIF) port"""
    
    EXTENSIONS = {'.gif', '.GIF'}
    
    def import_file(self, file_path: str) -> PyfficeImage:
        """Import GIF to PyfficeImage"""
        path = Path(file_path)
        
        img = Image.open(path)
        
        image = PyfficeImage({'path': str(path)})
        image.create_new_document(path.stem)
        
        image.document['width'] = img.width
        image.document['height'] = img.height
        image.document['mode'] = img.mode
        image.document['format'] = 'GIF'
        image.document['source_format'] = 'gif'
        
        return image
    
    def export_file(self, image: PyfficeImage, file_path: str) -> None:
        """Export PyfficeImage to GIF"""
        path = Path(file_path)
        
        if image.image:
            image.image.save(str(path), 'GIF')


class BMPPort(ImagePort):
    """Bitmap (BMP) format port"""
    
    EXTENSIONS = {'.bmp', '.BMP'}
    
    def import_file(self, file_path: str) -> PyfficeImage:
        """Import BMP to PyfficeImage"""
        path = Path(file_path)
        
        img = Image.open(path)
        
        image = PyfficeImage({'path': str(path)})
        image.create_new_document(path.stem)
        
        image.document['width'] = img.width
        image.document['height'] = img.height
        image.document['mode'] = img.mode
        image.document['format'] = 'BMP'
        image.document['source_format'] = 'bmp'
        
        return image
    
    def export_file(self, image: PyfficeImage, file_path: str) -> None:
        """Export PyfficeImage to BMP"""
        path = Path(file_path)
        
        if image.image:
            image.image.save(str(path), 'BMP')


class WebPPort(ImagePort):
    """WebP format port"""
    
    EXTENSIONS = {'.webp', '.WEBP'}
    
    def import_file(self, file_path: str) -> PyfficeImage:
        """Import WebP to PyfficeImage"""
        path = Path(file_path)
        
        img = Image.open(path)
        
        image = PyfficeImage({'path': str(path)})
        image.create_new_document(path.stem)
        
        image.document['width'] = img.width
        image.document['height'] = img.height
        image.document['mode'] = img.mode
        image.document['format'] = 'WEBP'
        image.document['source_format'] = 'webp'
        
        return image
    
    def export_file(self, image: PyfficeImage, file_path: str) -> None:
        """Export PyfficeImage to WebP"""
        path = Path(file_path)
        
        if image.image:
            image.image.save(str(path), 'WEBP')


class TIFFPort(ImagePort):
    """Tagged Image File Format (TIFF) port"""
    
    EXTENSIONS = {'.tiff', '.tif', '.TIFF', '.TIF'}
    
    def import_file(self, file_path: str) -> PyfficeImage:
        """Import TIFF to PyfficeImage"""
        path = Path(file_path)
        
        img = Image.open(path)
        
        image = PyfficeImage({'path': str(path)})
        image.create_new_document(path.stem)
        
        image.document['width'] = img.width
        image.document['height'] = img.height
        image.document['mode'] = img.mode
        image.document['format'] = 'TIFF'
        image.document['source_format'] = 'tiff'
        
        return image
    
    def export_file(self, image: PyfficeImage, file_path: str) -> None:
        """Export PyfficeImage to TIFF"""
        path = Path(file_path)
        
        if image.image:
            image.image.save(str(path), 'TIFF')


class SVGBPort(ImagePort):
    """Scalable Vector Graphics (SVG) format port"""
    
    EXTENSIONS = {'.svg', '.SVG'}
    
    def import_file(self, file_path: str) -> PyfficeImage:
        """Import SVG to PyfficeImage"""
        path = Path(file_path)
        
        image = PyfficeImage({'path': str(path)})
        image.create_new_document(path.stem)
        
        image.document['source_format'] = 'svg'
        
        # SVG is vector - read as text
        with open(path, 'r') as f:
            image.document['svg_content'] = f.read()
        
        return image
    
    def export_file(self, image: PyfficeImage, file_path: str) -> None:
        """Export PyfficeImage to SVG"""
        path = Path(file_path)
        
        svg_content = image.document.get('svg_content', '')
        with open(path, 'w') as f:
            f.write(svg_content)


class ImagePortsManager:
    """Manages all image format ports and conversions"""
    
    def __init__(self):
        self.ports: Dict[str, ImagePort] = {}
        self._register_default_ports()
    
    def _register_default_ports(self):
        """Register all default image ports"""
        self.ports['png'] = PNGPort()
        self.ports['jpg'] = JPEGPort()
        self.ports['jpeg'] = JPEGPort()
        self.ports['gif'] = GIFPort()
        self.ports['bmp'] = BMPPort()
        self.ports['webp'] = WebPPort()
        self.ports['tiff'] = TIFFPort()
        self.ports['tif'] = TIFFPort()
        self.ports['svg'] = SVGBPort()
    
    def register_port(self, format_name: str, port: ImagePort) -> None:
        """Register a new image format port"""
        self.ports[format_name] = port
    
    def get_port(self, format_name: str) -> Optional[ImagePort]:
        """Get port for a specific format"""
        return self.ports.get(format_name.lower())
    
    def import_file(self, file_path: str) -> PyfficeImage:
        """Import any supported image file to PyfficeImage"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for port in self.ports.values():
            if ext in port.EXTENSIONS:
                return port.import_file(str(path))
        
        raise ValueError(f"Unsupported image format: {ext}")
    
    def export_file(self, image: PyfficeImage, file_path: str, format_name: str = None) -> None:
        """Export PyfficeImage to specified format"""
        path = Path(file_path)
        
        if format_name is None:
            format_name = path.suffix.lower().lstrip('.')
        
        port = self.ports.get(format_name.lower())
        if port is None:
            raise ValueError(f"Unsupported image format: {format_name}")
        
        port.export_file(image, str(path))
    
    def convert(self, input_path: str, output_path: str) -> PyfficeImage:
        """Convert between image formats"""
        img = self.import_file(input_path)
        self.export_file(img, output_path)
        return img
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported format extensions"""
        formats = set()
        for port in self.ports.values():
            formats.update(port.EXTENSIONS)
        return sorted(list(formats))


# Global port manager instance
_port_manager = None

def get_ports_manager() -> ImagePortsManager:
    """Get global image ports manager instance"""
    global _port_manager
    if _port_manager is None:
        _port_manager = ImagePortsManager()
    return _port_manager


def import_image(file_path: str) -> PyfficeImage:
    """Convenience function to import image file"""
    return get_ports_manager().import_file(file_path)


def export_image(image: PyfficeImage, file_path: str) -> None:
    """Convenience function to export image file"""
    get_ports_manager().export_file(image, file_path)


def convert_image(input_path: str, output_path: str) -> PyfficeImage:
    """Convenience function to convert between image formats"""
    return get_ports_manager().convert(input_path, output_path)


# ====================================================================================================================||
