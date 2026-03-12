# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: CAD Ports Module
	description: >
		Common CAD conversion layer - imports various CAD formats to a universal
		NchantdCADPart format and allows export back to other CAD formats.
	version: 0.0.1.0.1.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# ======================================3rd Party Library Modules=====================================================||
# ======================================Solutions Brewer Library Modules==============================================||

# ====================================================================================================================||


@dataclass
class NchantdCADPart:
    """
    Universal CAD Part representation.
    All CAD formats import to this common format and export from it.
    """
    name: str = ""
    vertices: List[Tuple[float, float, float]] = field(default_factory=list)
    faces: List[List[int]] = field(default_factory=list)  # Vertex indices per face
    normals: List[Tuple[float, float, float]] = field(default_factory=list)
    edges: List[Tuple[int, int]] = field(default_factory=list)  # Vertex index pairs
    materials: List[Dict[str, Any]] = field(default_factory=list)
    groups: Dict[str, List[int]] = field(default_factory=dict)  # Named groups of face indices
    transform: List[List[float]] = field(default_factory=lambda: [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_format: str = ""  # Original file format
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'name': self.name,
            'vertices': self.vertices,
            'faces': self.faces,
            'normals': self.normals,
            'edges': self.edges,
            'materials': self.materials,
            'groups': self.groups,
            'transform': self.transform,
            'metadata': self.metadata,
            'source_format': self.source_format
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NchantdCADPart':
        """Create from dictionary"""
        return cls(
            name=data.get('name', ''),
            vertices=data.get('vertices', []),
            faces=data.get('faces', []),
            normals=data.get('normals', []),
            edges=data.get('edges', []),
            materials=data.get('materials', []),
            groups=data.get('groups', {}),
            transform=data.get('transform', [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
            metadata=data.get('metadata', {}),
            source_format=data.get('source_format', '')
        )
    
    def apply_transform(self, matrix: List[List[float]]) -> None:
        """Apply 4x4 transformation matrix to all vertices"""
        new_vertices = []
        for v in self.vertices:
            # Homogeneous coordinates
            x, y, z = v[0], v[1], v[2]
            nx = matrix[0][0]*x + matrix[0][1]*y + matrix[0][2]*z + matrix[0][3]
            ny = matrix[1][0]*x + matrix[1][1]*y + matrix[1][2]*z + matrix[1][3]
            nz = matrix[2][0]*x + matrix[2][1]*y + matrix[2][2]*z + matrix[2][3]
            new_vertices.append((nx, ny, nz))
        self.vertices = new_vertices


class CADPort(ABC):
    """Abstract base class for CAD format ports"""
    
    @abstractmethod
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import CAD file to common NchantdCADPart format"""
        pass
    
    @abstractmethod
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to CAD file format"""
        pass


class STLPort(CADPort):
    """STL (Stereolithography) CAD format port"""
    
    EXTENSIONS = {'.stl', '.STL'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import STL to NchantdCADPart"""
        from pathlib import Path
        from pyffice.cad.stl import PyfficeSTL
        path = Path(file_path)
        stl = PyfficeSTL(str(path))
        data = stl.read()
        
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'stl'
        
        # Convert faces to vertices
        for face in data.get('faces', []):
            verts = face.get('vertices', [])
            if len(verts) >= 3:
                # Add vertices
                start_idx = len(part.vertices)
                for v in verts:
                    part.vertices.append(v)
                # Add face (triangle)
                part.faces.append([start_idx, start_idx+1, start_idx+2])
                # Add normal
                part.normals.append(face.get('normal', (0, 0, 1)))
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to STL"""
        from pathlib import Path
        from pyffice.cad.stl import PyfficeSTL
        
        faces = []
        for i, face_indices in enumerate(cad_part.faces):
            if len(face_indices) >= 3:
                vertices = [cad_part.vertices[idx] for idx in face_indices[:3]]
                normal = cad_part.normals[i] if i < len(cad_part.normals) else (0, 0, 1)
                faces.append({'normal': normal, 'vertices': vertices})
        
        stl = PyfficeSTL(str(file_path))
        stl.write({'faces': faces})


class OBJPort(CADPort):
    """OBJ (Wavefront) CAD format port"""
    
    EXTENSIONS = {'.obj', '.OBJ'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import OBJ to NchantdCADPart"""
        from pathlib import Path
        from pyffice.cad.obj import PyfficeOBJ
        path = Path(file_path)
        obj = PyfficeOBJ(str(path))
        data = obj.read()
        
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'obj'
        part.vertices = list(data.get('vertices', []))
        part.normals = list(data.get('normals', []))
        part.faces = [list(f) for f in data.get('faces', [])]
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to OBJ"""
        from pathlib import Path
        from pyffice.cad.obj import PyfficeOBJ
        
        obj = PyfficeOBJ(str(file_path))
        obj.write({
            'vertices': cad_part.vertices,
            'normals': cad_part.normals,
            'faces': cad_part.faces
        })


class STEPPort(CADPort):
    """STEP (Standard for the Exchange of Product model data) CAD format port"""
    
    EXTENSIONS = {'.step', '.stp', '.STEP', '.STP'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import STEP to NchantdCADPart"""
        from pathlib import Path
        from pyffice.cad.step import PyfficeSTEP
        path = Path(file_path)
        step = PyfficeSTEP(str(path))
        content = step.read()
        
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'step'
        part.metadata['step_content'] = content
        
        # Note: Full STEP parsing is complex - this is a placeholder
        # Real implementation would parse STEP entities to geometry
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to STEP"""
        from pathlib import Path
        from pyffice.cad.step import PyfficeSTEP
        
        content = cad_part.metadata.get('step_content', '')
        step = PyfficeSTEP(str(file_path))
        step.write(content)


class CADPortManager:
    """Manages all CAD format ports and conversions"""
    
    def __init__(self):
        self.ports: Dict[str, CADPort] = {
            'stl': STLPort(),
            'obj': OBJPort(),
            'step': STEPPort(),
        }
    
    def register_port(self, format_name: str, port: CADPort) -> None:
        """Register a new CAD format port"""
        self.ports[format_name] = port
    
    def get_port(self, format_name: str) -> Optional[CADPort]:
        """Get port for a specific format"""
        return self.ports.get(format_name.lower())
    
    def import_file(self, file_path: str) -> NchantdCADPart:
        """Import any supported CAD file to NchantdCADPart"""
        from pathlib import Path
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for format_name, port in self.ports.items():
            if ext in port.EXTENSIONS:
                return port.import_to_common(path)
        
        raise ValueError(f"Unsupported CAD format: {ext}")
    
    def export_file(self, cad_part: NchantdCADPart, file_path: str, format_name: str = None) -> None:
        """Export NchantdCADPart to specified format"""
        from pathlib import Path
        path = Path(file_path)
        
        if format_name is None:
            format_name = path.suffix.lower().lstrip('.')
        
        port = self.ports.get(format_name.lower())
        if port is None:
            raise ValueError(f"Unsupported CAD format: {format_name}")
        
        port.export_from_common(cad_part, path)
    
    def convert(self, input_path: str, output_path: str) -> NchantdCADPart:
        """Convert between CAD formats"""
        # Import to common format
        common = self.import_file(input_path)
        # Export to target format
        self.export_file(common, output_path)
        return common


# Global port manager instance
_port_manager = None

def get_port_manager() -> CADPortManager:
    """Get global CAD port manager instance"""
    global _port_manager
    if _port_manager is None:
        _port_manager = CADPortManager()
    return _port_manager


def import_cad(file_path: str) -> NchantdCADPart:
    """Convenience function to import CAD file"""
    return get_port_manager().import_file(file_path)


def export_cad(cad_part: NchantdCADPart, file_path: str) -> None:
    """Convenience function to export CAD file"""
    get_port_manager().export_file(cad_part, file_path)


def convert_cad(input_path: str, output_path: str) -> NchantdCADPart:
    """Convenience function to convert between CAD formats"""
    return get_port_manager().convert(input_path, output_path)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
