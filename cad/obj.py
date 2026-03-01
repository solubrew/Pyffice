"""
Pyffice OBJ Module - Handle Wavefront OBJ files
"""

from typing import Dict, Any, List, Tuple
from pathlib import Path


class PyfficeOBJ:
    """Handle OBJ 3D model files"""
    
    SUPPORTED_EXTENSIONS = ['.obj']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self) -> Dict[str, Any]:
        """Read OBJ file and return structured data"""
        vertices = []
        normals = []
        texcoords = []
        faces = []
        
        with open(self.file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if not parts:
                    continue
                
                if parts[0] == 'v':
                    vertices.append([float(x) for x in parts[1:4]])
                elif parts[0] == 'vn':
                    normals.append([float(x) for x in parts[1:4]])
                elif parts[0] == 'vt':
                    texcoords.append([float(x) for x in parts[1:3]])
                elif parts[0] == 'f':
                    face = []
                    for vertex in parts[1:]:
                        indices = vertex.split('/')
                        face.append({
                            'v': int(indices[0]) - 1 if len(indices) > 0 else 0,
                            'vt': int(indices[1]) - 1 if len(indices) > 1 and indices[1] else None,
                            'vn': int(indices[2]) - 1 if len(indices) > 2 and indices[2] else None,
                        })
                    faces.append(face)
        
        return {
            'vertices': vertices,
            'normals': normals,
            'texcoords': texcoords,
            'faces': faces,
            'vertex_count': len(vertices),
            'face_count': len(faces),
        }
    
    def write(self, data: Dict[str, Any], output_path: str = None):
        """Write data to OBJ file"""
        output = Path(output_path) if output_path else self.file_path
        
        with open(output, 'w') as f:
            f.write(f"# Pyffice OBJ Export\n")
            
            for v in data.get('vertices', []):
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
            
            for vn in data.get('normals', []):
                f.write(f"vn {vn[0]} {vn[1]} {vn[2]}\n")
            
            for vt in data.get('texcoords', []):
                f.write(f"vt {vt[0]} {vt[1]}\n")
            
            for face in data.get('faces', []):
                f.write("f " + " ".join(f"{v['v']+1}//{v['vn']+1}" for v in face) + "\n")


def read_obj(file_path: str) -> Dict[str, Any]:
    """Convenience function to read OBJ"""
    return PyfficeOBJ(file_path).read()


def write_obj(file_path: str, data: Dict[str, Any]):
    """Convenience function to write OBJ"""
    PyfficeOBJ(file_path).write(data)
