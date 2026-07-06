"""Pyffice CAM Module

Provides Computer-Aided Manufacturing capabilities including:
- CAM file handling
- Bill of Materials (BOM) generation
- G-code generation
"""

from pyffice.cam.cam import PyfficeCAM, PyfficeCAMManager
from pyffice.cam.bom import PyfficeBOM, PyfficeSoftwareBOM
from pyffice.cam.gcode import PyfficeGCode

__all__ = [
    "PyfficeCAM",
    "PyfficeCAMManager",
    "PyfficeBOM",
    "PyfficeSoftwareBOM",
    "PyfficeGCode",
]
