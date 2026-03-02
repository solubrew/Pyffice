"""
Pyffice STL 3D Model Handler
"""

from pathlib import Path
from typing import List, Tuple


def read(stl_path: str) -> dict:
    """Read STL file and return vertices and faces."""
    vertices = []
    faces = []
    
    with open(stl_path, "r") as f:
        content = f.read()
    
    if "solid" in content.lower() and "facet" in content.lower():
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.strip().startswith("vertex"):
                parts = line.strip().split()
                if len(parts) >= 4:
                    try:
                        vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
                    except:
                        pass
    else:
        with open(stl_path, "rb") as f:
            f.read(80)
            num_triangles = int.from_bytes(f.read(4), "little")
            for _ in range(num_triangles):
                f.read(12)
                attr = f.read(2)
    
    return {"vertices": vertices, "faces": [list(range(i*3, i*3+3)) for i in range(len(vertices)//3)]}


def write(stl_path: str, data: dict, ascii: bool = False) -> None:
    """Write STL file from data dictionary."""
    vertices = data.get("vertices", [])
    faces = data.get("faces", [])
    
    with open(stl_path, "w") as f:
        f.write("solid model\n")
        for face in faces:
            v0, v1, v2 = [vertices[i] for i in face[:3]]
            f.write(f"  facet normal 0 0 1\n")
            f.write(f"    outer loop\n")
            f.write(f"      vertex {v0[0]} {v0[1]} {v0[2]}\n")
            f.write(f"      vertex {v1[0]} {v1[1]} {v1[2]}\n")
            f.write(f"      vertex {v2[0]} {v2[1]} {v2[2]}\n")
            f.write(f"    endloop\n")
            f.write(f"  endfacet\n")
        f.write("endsolid model\n")
