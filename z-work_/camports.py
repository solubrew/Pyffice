"""
Pyffice Cam Ports - External format converters for camera/capture data.
"""
from pyffice.cam.cam import PyfficeCam
from pyffice.ports.ports import PyfficePort


class MP4Port(PyfficePort):
    """Port for MP4 video format."""

    def read(self, file_path: str) -> PyfficeCam:
        """Read MP4 file and convert to PyfficeCam."""
        pass

    def write(self, cam: PyfficeCam, file_path: str) -> None:
        """Write PyfficeCam to MP4 file."""
        pass


class AVIPort(PyfficePort):
    """Port for AVI video format."""

    def read(self, file_path: str) -> PyfficeCam:
        """Read AVI file and convert to PyfficeCam."""
        pass

    def write(self, cam: PyfficeCam, file_path: str) -> None:
        """Write PyfficeCam to AVI file."""
        pass


class MKVPort(PyfficePort):
    """Port for MKV video format."""

    def read(self, file_path: str) -> PyfficeCam:
        """Read MKV file and convert to PyfficeCam."""
        pass

    def write(self, cam: PyfficeCam, file_path: str) -> None:
        """Write PyfficeCam to MKV file."""
        pass
