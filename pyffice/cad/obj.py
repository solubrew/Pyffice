"""
Pyffice OBJ 3D Model Handler
"""

from pathlib import Path
from typing import List, Tuple, Optional
import struct


def read(obj_path: str) -> dict:
    """Read OBJ file and return vertices, normals, textures, faces."""
    vertices = []
    normals = []
    textures = []
    faces = []
    
    with open(obj_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            cmd = parts[0]
            if cmd == "v":
                vertices.append(tuple(map(float, parts[1:4])))
            elif cmd == "vn":
                normals.append(tuple(map(float, parts[1:4])))
            elif cmd == "vt":
                textures.append(tuple(map(float, parts[1:3])))
            elif cmd == "f":
                face = []
                for pt in parts[1:]:
                    indices = pt.split("/")
                    face.append(tuple(int(i) if i else 0 for i in indices))
                faces.append(face)
    
    return {"vertices": vertices, "normals": normals, "textures": textures, "faces": faces}


def write(obj_path: str, data: dict) -> None:
    """Write OBJ file from data dictionary."""
    with open(obj_path, "w") as f:
        for v in data.get("vertices", []):
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for vt in data.get("textures", []):
            f.write(f"vt {vt[0]} {vt[1]}\n")
        for vn in data.get("normals", []):
            f.write(f"vn {vn[0]} {vn[1]} {vn[2]}\n")
        for face in data.get("faces", []):
            face_str = " ".join("/".join(str(i) for i in pt) for pt in face)
            f.write(f"f {face_str}\n")


def create_box(width: float, height: float, depth: float) -> dict:
    """Create simple box OBJ data."""
    w, h, d = width/2, height/2, depth/2
    vertices = [
        (-w, -h, d), (w, -h, d), (w, h, d), (-w, h, d),
        (-w, -h, -d), (w, -h, -d), (w, h, -d), (-w, h, -d)
    ]
    faces = [
        (1, 2, 3, 4), (5, 8, 7, 6), (1, 5, 6, 2),
        (2, 6, 7, 3), (3, 7, 8, 4), (1, 4, 8, 5)
    ]
    return {"vertices": vertices, "faces": faces}
