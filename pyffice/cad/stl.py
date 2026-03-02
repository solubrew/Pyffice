"""
Pyffice STL Module - Handle STL 3D model files
"""

from typing import Dict, Any, List
from pathlib import Path
import struct
import numpy as np


class PyfficeSTL:
    """Handle STL 3D model files (ASCII and Binary)"""
    
    SUPPORTED_EXTENSIONS = ['.stl']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self) -> Dict[str, Any]:
        """Read STL file and return structured data"""
        with open(self.file_path, 'rb') as f:
            header = f.read(80)
        
        if b'solid' in header[:6].lower():
            return self._read_ascii()
        else:
            return self._read_binary()
    
    def _read_ascii(self) -> Dict[str, Any]:
        """Read ASCII STL"""
        vertices = []
        normals = []
        
        with open(self.file_path, 'r') as f:
            current_normal = None
            current_facet = []
            
            for line in f:
                line = line.strip()
                if line.startswith('facet normal'):
                    parts = line.split()[2:]
                    current_normal = [float(x) for x in parts]
                elif line.startswith('vertex'):
                    parts = line.split()[1:]
                    current_facet.append([float(x) for x in parts])
                elif line.startswith('endfacet'):
                    if current_normal and len(current_facet) == 3:
                        normals.append(current_normal)
                        vertices.extend(current_facet)
                    current_normal = None
                    current_facet = []
        
        return self._build_result(vertices, normals)
    
    def _read_binary(self) -> Dict[str, Any]:
        """Read binary STL"""
        vertices = []
        normals = []
        
        with open(self.file_path, 'rb') as f:
            f.read(80)  # skip header
            triangle_count = struct.unpack('<I', f.read(4))[0]
            
            for _ in range(triangle_count):
                normal = struct.unpack('<3f', f.read(12))
                for _ in range(3):
                    vertex = struct.unpack('<3f', f.read(12))
                    vertices.append(list(vertex))
                normals.append(list(normal))
                f.read(2)  # attribute byte count
        
        return self._build_result(vertices, normals)
    
    def _build_result(self, vertices: List, normals: List) -> Dict[str, Any]:
        """Build result dict from vertices and normals"""
        return {
            'vertices': vertices,
            'normals': normals,
            'vertex_count': len(vertices),
            'face_count': len(normals),
        }
    
    def write_binary(self, data: Dict[str, Any], output_path: str = None):
        """Write data as binary STL"""
        output = Path(output_path) if output_path else self.file_path
        
        with open(output, 'wb') as f:
            f.write(b' ' * 80)  # header
            
            faces = data.get('faces', [])
            normals = data.get('normals', [])
            vertices = data.get('vertices', [])
            
            f.write(struct.pack('<I', len(faces)))
            
            for i, face in enumerate(faces):
                normal = normals[i] if i < len(normals) else [0, 0, 1]
                f.write(struct.pack('<3f', *normal))
                
                for vi in face:
                    v = vertices[vi] if vi < len(vertices) else [0, 0, 0]
                    f.write(struct.pack('<3f', *v))
                
                f.write(struct.pack('<H', 0))


def read_stl(file_path: str) -> Dict[str, Any]:
    """Convenience function to read STL"""
    return PyfficeSTL(file_path).read()


def write_stl(file_path: str, data: Dict[str, Any]):
    """Convenience function to write STL"""
    PyfficeSTL(file_path).write_binary(data)
