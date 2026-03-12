"""
CAD file format support (OBJ, STL, DWG, DXF, STEP, IGES, etc.).
Uses pyffice.ports.cad for format conversion.
"""

from pyffice.cad.obj import PyfficeOBJ
from pyffice.cad.stl import PyfficeSTL
from pyffice.cad.scad import PyfficeSCAD

# Import ports for format conversion
from pyffice.ports.cad import (
    NchantdCADPart,
    CADPort,
    STLPort,
    OBJPort,
    STEPPort,
    CADPortManager,
    get_port_manager,
    import_cad,
    export_cad,
    convert_cad
)

__all__ = [
    # Direct CAD handlers
    "PyfficeOBJ",
    "PyfficeSTL",
    "PyfficeSCAD",
    # Ports - universal CAD format
    "NchantdCADPart",
    "CADPort",
    "STLPort",
    "OBJPort",
    "STEPPort",
    "CADPortManager",
    "get_port_manager",
    "import_cad",
    "export_cad",
    "convert_cad",
]
