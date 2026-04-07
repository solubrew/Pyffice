"""
Pyffice Images Ports - External format converters for image data.
"""
from pyffice.images.images import PyfficeImage
from pyffice.ports.ports import PyfficePort


class PNGPort(PyfficePort):
    """Port for PNG (.png) format."""

    def read(self, file_path: str) -> PyfficeImage:
        """Read PNG file and convert to PyfficeImage."""
        pass

    def write(self, image: PyfficeImage, file_path: str) -> None:
        """Write PyfficeImage to PNG file."""
        pass


class JPEGPort(PyfficePort):
    """Port for JPEG (.jpg, .jpeg) format."""

    def read(self, file_path: str) -> PyfficeImage:
        """Read JPEG file and convert to PyfficeImage."""
        pass

    def write(self, image: PyfficeImage, file_path: str) -> None:
        """Write PyfficeImage to JPEG file."""
        pass


class GIFPort(PyfficePort):
    """Port for GIF (.gif) format."""

    def read(self, file_path: str) -> PyfficeImage:
        """Read GIF file and convert to PyfficeImage."""
        pass

    def write(self, image: PyfficeImage, file_path: str) -> None:
        """Write PyfficeImage to GIF file."""
        pass


class WEBPPort(PyfficePort):
    """Port for WebP (.webp) format."""

    def read(self, file_path: str) -> PyfficeImage:
        """Read WebP file and convert to PyfficeImage."""
        pass

    def write(self, image: PyfficeImage, file_path: str) -> None:
        """Write PyfficeImage to WebP file."""
        pass


class SVGBPort(PyfficePort):
    """Port for SVG (.svg) format."""

    def read(self, file_path: str) -> PyfficeImage:
        """Read SVG file and convert to PyfficeImage."""
        pass

    def write(self, image: PyfficeImage, file_path: str) -> None:
        """Write PyfficeImage to SVG file."""
        pass


class BMPPort(PyfficePort):
    """Port for BMP (.bmp) format."""

    def read(self, file_path: str) -> PyfficeImage:
        """Read BMP file and convert to PyfficeImage."""
        pass

    def write(self, image: PyfficeImage, file_path: str) -> None:
        """Write PyfficeImage to BMP file."""
        pass


class TIFFPort(PyfficePort):
    """Port for TIFF (.tif, .tiff) format."""

    def read(self, file_path: str) -> PyfficeImage:
        """Read TIFF file and convert to PyfficeImage."""
        pass

    def write(self, image: PyfficeImage, file_path: str) -> None:
        """Write PyfficeImage to TIFF file."""
        pass
