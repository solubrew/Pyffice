"""
Pyffice OpenSCAD Script Handler
"""

from pathlib import Path
from typing import Optional


def create(scad_path: str) -> None:
    """Create empty OpenSCAD script."""
    with open(scad_path, "w") as f:
        f.write("// OpenSCAD Script\n\n")
        f.write("module demo() {\n")
        f.write("    cube([10, 10, 10]);\n")
        f.write("}\n\n")
        f.write("demo();\n")


def read(scad_path: str) -> str:
    """Read OpenSCAD script."""
    with open(scad_path, "r") as f:
        return f.read()


def write(scad_path: str, code: str) -> None:
    """Write OpenSCAD script."""
    with open(scad_path, "w") as f:
        f.write(code)


def render(scad_path: str, output: str, backend: str = "cgal") -> None:
    """Render OpenSCAD to STL."""
    import subprocess
    cmd = ["openscad", "-o", output, f"--backend={backend}", scad_path]
    subprocess.run(cmd, check=True, capture_output=True)


def add_cube(scad_path: str, size: float = 10, center: bool = False) -> None:
    """Add cube to script."""
    with open(scad_path, "a") as f:
        f.write(f"cube({size}, center={str(center).lower()});\n")


def add_sphere(scad_path: str, radius: float = 10) -> None:
    """Add sphere to script."""
    with open(scad_path, "a") as f:
        f.write(f"sphere({radius});\n")


def add_cylinder(scad_path: str, h: float = 10, r: float = 5) -> None:
    """Add cylinder to script."""
    with open(scad_path, "a") as f:
        f.write(f"cylinder(h={h}, r={r});\n")
