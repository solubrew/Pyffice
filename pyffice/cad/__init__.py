"""
CAD file format support (OBJ, STL, DWG, DXF, STEP, IGES, etc.).
Uses pyffice.ports.cadports for format conversion.
"""

from pyffice.cad.obj import PyfficeOBJ
from pyffice.cad.stl import PyfficeSTL
from pyffice.cad.scad import PyfficeSCAD
from pyffice.cad.cad import PyfficeCADPart, PyfficeCADManager, PyfficeCADAssembly

# Import ports for format conversion
from pyffice.ports.cadports import (
    CADPort,
    STLPort,
    OBJPort,
    STEPPort,
    DWGPort,
    DXFPort,
    FBXPort,
    GLTFPort,
    IGESPort,
    BLENDPort,
    SCADPort,
    CADPortsManager,
    get_ports_manager,
    import_cad,
    export_cad,
    convert_cad,
)

__all__ = [
    # Pyffice CAD classes
    "PyfficeOBJ",
    "PyfficeSTL",
    "PyfficeSCAD",
    "PyfficeCADPart",
    "PyfficeCADManager",
    "PyfficeCADAssembly",
    # Ports - external CAD format converters
    "CADPort",
    "STLPort",
    "OBJPort",
    "STEPPort",
    "DWGPort",
    "DXFPort",
    "FBXPort",
    "GLTFPort",
    "IGESPort",
    "BLENDPort",
    "SCADPort",
    "CADPortsManager",
    "get_ports_manager",
    "import_cad",
    "export_cad",
    "convert_cad",
]
