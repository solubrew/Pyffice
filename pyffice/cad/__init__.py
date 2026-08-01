"""
Cad module for pyffice.
"""

# Lazy __getattr__ proxy to break circular imports when
# subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    "PyfficeBLEND": ("pyffice.cad.blend", "PyfficeBLEND"),
    "load": ("pyffice.cad.stl", "load"),
    "read": ("pyffice.cad.stl", "read"),
    "write": ("pyffice.cad.stl", "write"),
    "dump": ("pyffice.cad.step", "dump"),
    "PyfficeCADAssembly": ("pyffice.cad.cad", "PyfficeCADAssembly"),
    "PyfficeCADManager": ("pyffice.cad.cad", "PyfficeCADManager"),
    "PyfficeCADPart": ("pyffice.cad.cad", "PyfficeCADPart"),
    "PyfficeBOM": ("pyffice.cad.cad_bom", "PyfficeBOM"),
    "PyfficeSoftwareBOM": ("pyffice.cad.cad_bom", "PyfficeSoftwareBOM"),
    "PyfficeCAM": ("pyffice.cad.cad_cam", "PyfficeCAM"),
    "PyfficeCAMManager": ("pyffice.cad.cad_cam", "PyfficeCAMManager"),
    "PyfficeGCode": ("pyffice.cad.cad_gcode", "PyfficeGCode"),
    "PyfficeDWG": ("pyffice.cad.dwg", "PyfficeDWG"),
    "load": ("pyffice.cad.stl", "load"),
    "read": ("pyffice.cad.stl", "read"),
    "write": ("pyffice.cad.stl", "write"),
    "dump": ("pyffice.cad.step", "dump"),
    "PyfficeDXF": ("pyffice.cad.dxf", "PyfficeDXF"),
    "load": ("pyffice.cad.stl", "load"),
    "read": ("pyffice.cad.stl", "read"),
    "write": ("pyffice.cad.stl", "write"),
    "dump": ("pyffice.cad.step", "dump"),
    "PyfficeFBX": ("pyffice.cad.fbx", "PyfficeFBX"),
    "load": ("pyffice.cad.stl", "load"),
    "read": ("pyffice.cad.stl", "read"),
    "write": ("pyffice.cad.stl", "write"),
    "dump": ("pyffice.cad.step", "dump"),
    "PyfficeGLTF": ("pyffice.cad.gltf", "PyfficeGLTF"),
    "load": ("pyffice.cad.stl", "load"),
    "read": ("pyffice.cad.stl", "read"),
    "write": ("pyffice.cad.stl", "write"),
    "dump": ("pyffice.cad.step", "dump"),
    "PyfficeIGES": ("pyffice.cad.iges", "PyfficeIGES"),
    "load": ("pyffice.cad.stl", "load"),
    "read": ("pyffice.cad.stl", "read"),
    "write": ("pyffice.cad.stl", "write"),
    "dump": ("pyffice.cad.step", "dump"),
    # NOTE: PyfficeShape is NOT re-exported here. The canonical
    # implementation lives at pyffice.items.shapes:PyfficeShape
    # (PyfficeUnit base, used by matrix.py). The phantom
    # PyfficeDocument-based PyfficeShape in cad/items.py is
    # unused and was removed.
    "PyfficeOBJ": ("pyffice.cad.obj", "PyfficeOBJ"),
    "read": ("pyffice.cad.stl", "read"),
    "load": ("pyffice.cad.stl", "load"),
    "write": ("pyffice.cad.stl", "write"),
    "PyfficeSCAD": ("pyffice.cad.scad", "PyfficeSCAD"),
    "PyfficeSTEP": ("pyffice.cad.step", "PyfficeSTEP"),
    "load": ("pyffice.cad.stl", "load"),
    "read": ("pyffice.cad.stl", "read"),
    "write": ("pyffice.cad.stl", "write"),
    "dump": ("pyffice.cad.step", "dump"),
    "PyfficeSTL": ("pyffice.cad.stl", "PyfficeSTL"),
    "read": ("pyffice.cad.stl", "read"),
    "load": ("pyffice.cad.stl", "load"),
    "write": ("pyffice.cad.stl", "write"),
}

def __getattr__(name: str) -> None:
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.cad' has no attribute " + repr(name)
    )


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficeBLEND",
    "load",
    "read",
    "write",
    "dump",
    "PyfficeCADAssembly",
    "PyfficeCADManager",
    "PyfficeCADPart",
    "PyfficeBOM",
    "PyfficeSoftwareBOM",
    "PyfficeCAM",
    "PyfficeCAMManager",
    "PyfficeGCode",
    "PyfficeDWG",
    "load",
    "read",
    "write",
    "dump",
    "PyfficeDXF",
    "load",
    "read",
    "write",
    "dump",
    "PyfficeFBX",
    "load",
    "read",
    "write",
    "dump",
    "PyfficeGLTF",
    "load",
    "read",
    "write",
    "dump",
    "PyfficeIGES",
    "load",
    "read",
    "write",
    "dump",
    "PyfficeOBJ",
    "read",
    "load",
    "write",
    "PyfficeSCAD",
    "PyfficeSTEP",
    "load",
    "read",
    "write",
    "dump",
    "PyfficeSTL",
    "read",
    "load",
    "write",
]
