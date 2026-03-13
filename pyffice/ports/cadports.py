# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: CAD Ports Module
	description: >
		External CAD format ports - converts all external CAD formats to/from
		PyfficeCADPart. Includes STL, OBJ, STEP, DWG, DXF, FBX, GLTF, IGES, 
		BLEND, SCAD and other formats.
	version: 0.0.1.0.1.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from __future__ import annotations
from typing import List, Dict, Any, Optional, Tuple, Union, TYPE_CHECKING
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from pathlib import Path

# ======================================3rd Party Library Modules=====================================================||
# ======================================Solutions Brewer Library Modules==============================================||
# Use TYPE_CHECKING to avoid circular import at runtime
if TYPE_CHECKING:
    from pyffice.cad.cad import PyfficeCADPart
    from pyffice.document import PyfficeDocument


# ====================================================================================================================||


class CADPort(ABC):
    """Abstract base class for CAD format ports"""
    
    EXTENSIONS: set = set()
    
    @abstractmethod
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import CAD file to PyfficeCADPart"""
        pass
    
    @abstractmethod
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to CAD file format"""
        pass


class STLPort(CADPort):
    """STL (Stereolithography) CAD format port"""
    
    EXTENSIONS = {'.stl', '.STL'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import STL to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        from pyffice.cad.stl import PyfficeSTL
        path = Path(file_path)
        stl = PyfficeSTL(str(path))
        data = stl.read()
        
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        vertices = []
        faces = []
        normals = []
        
        for face in data.get('faces', []):
            verts = face.get('vertices', [])
            if len(verts) >= 3:
                start_idx = len(vertices)
                for v in verts:
                    vertices.append(v)
                faces.append([start_idx, start_idx+1, start_idx+2])
                normals.append(face.get('normal', (0, 0, 1)))
        
        # Store in document
        part.document['vertices'] = vertices
        part.document['faces'] = faces
        part.document['normals'] = normals
        part.document['source_format'] = 'stl'
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to STL"""
        from pyffice.cad.stl import PyfficeSTL
        
        vertices = cad_part.document.get('vertices', [])
        faces = cad_part.document.get('faces', [])
        normals = cad_part.document.get('normals', [])
        
        out_faces = []
        for i, face_indices in enumerate(faces):
            if len(face_indices) >= 3:
                face_verts = [vertices[idx] for idx in face_indices[:3]]
                normal = normals[i] if i < len(normals) else (0, 0, 1)
                out_faces.append({'normal': normal, 'vertices': face_verts})
        
        stl = PyfficeSTL(str(file_path))
        stl.write({'faces': out_faces})


class OBJPort(CADPort):
    """OBJ (Wavefront) CAD format port"""
    
    EXTENSIONS = {'.obj', '.OBJ'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import OBJ to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        from pyffice.cad.obj import PyfficeOBJ
        path = Path(file_path)
        obj = PyfficeOBJ(str(path))
        data = obj.read()
        
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        part.document['vertices'] = list(data.get('vertices', []))
        part.document['normals'] = list(data.get('normals', []))
        part.document['faces'] = [list(f) for f in data.get('faces', [])]
        part.document['source_format'] = 'obj'
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to OBJ"""
        from pyffice.cad.obj import PyfficeOBJ
        
        obj_data = {
            'vertices': cad_part.document.get('vertices', []),
            'normals': cad_part.document.get('normals', []),
            'faces': cad_part.document.get('faces', [])
        }
        
        obj = PyfficeOBJ(str(file_path))
        obj.write(obj_data)


class STEPPort(CADPort):
    """STEP (Standard for the Exchange of Product model data) CAD format port"""
    
    EXTENSIONS = {'.step', '.stp', '.STEP', '.STP'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import STEP to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        from pyffice.cad.step import PyfficeSTEP
        path = Path(file_path)
        step = PyfficeSTEP(str(path))
        content = step.read()
        
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        part.document['step_content'] = content
        part.document['source_format'] = 'step'
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to STEP"""
        from pyffice.cad.step import PyfficeSTEP
        
        content = cad_part.document.get('step_content', '')
        step = PyfficeSTEP(str(file_path))
        step.write(content)


class DWGPort(CADPort):
    """Autodesk DWG CAD format port"""
    
    EXTENSIONS = {'.dwg', '.DWG'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import DWG to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        path = Path(file_path)
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        part.document['source_format'] = 'dwg'
        part.document['note'] = 'DWG import requires ODA SDK or ezdxf'
        
        # Try using ezdxf if available
        try:
            import ezdxf
            doc = ezdxf.readfile(str(path))
            msp = doc.modelspace()
            
            edges = []
            vertices = []
            
            for entity in msp:
                if entity.dxftype() == 'LINE':
                    start = entity.dxf.start
                    end = entity.dxf.end
                    edges.append({
                        'start': (start.x, start.y, start.z),
                        'end': (end.x, end.y, end.z)
                    })
                elif entity.dxftype() == 'VERTEX':
                    point = entity.dxf.location
                    vertices.append((point.x, point.y, point.z))
            
            part.document['edges'] = edges
            part.document['vertices'] = vertices
        except ImportError:
            part.document['error'] = 'ezdxf not installed'
        except Exception as e:
            part.document['error'] = str(e)
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to DWG"""
        raise NotImplementedError("DWG export requires Autodesk ODA SDK")


class DXFPort(CADPort):
    """AutoCAD DXF CAD format port"""
    
    EXTENSIONS = {'.dxf', '.DXF'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import DXF to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        path = Path(file_path)
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        part.document['source_format'] = 'dxf'
        
        edges = []
        vertices = []
        faces = []
        
        try:
            import ezdxf
            doc = ezdxf.readfile(str(path))
            msp = doc.modelspace()
            
            for entity in msp:
                if entity.dxftype() == 'LINE':
                    start = entity.dxf.start
                    end = entity.dxf.end
                    edges.append({
                        'start': (start.x, start.y, start.z if hasattr(start, 'z') else 0),
                        'end': (end.x, end.y, end.z if hasattr(end, 'z') else 0)
                    })
                elif entity.dxftype() == 'VERTEX':
                    point = entity.dxf.location
                    vertices.append((point.x, point.y, point.z if hasattr(point, 'z') else 0))
                elif entity.dxftype() == '3DFACE':
                    v_list = []
                    for i in range(4):
                        v = getattr(entity.dxf, f'v{i}', None)
                        if v:
                            v_list.append((v.x, v.y, v.z if hasattr(v, 'z') else 0))
                    if len(v_list) >= 3:
                        start_idx = len(vertices)
                        vertices.extend(v_list[:3])
                        faces.append([start_idx, start_idx+1, start_idx+2])
        except ImportError:
            part.document['error'] = 'ezdxf not installed'
        except Exception as e:
            part.document['error'] = str(e)
        
        part.document['edges'] = edges
        part.document['vertices'] = vertices
        part.document['faces'] = faces
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to DXF"""
        try:
            import ezdxf
            
            doc = ezdxf.new('R2010')
            msp = doc.modelspace()
            
            edges = cad_part.document.get('edges', [])
            for edge in edges:
                start = edge.get('start', (0, 0, 0))
                end = edge.get('end', (0, 0, 0))
                msp.add_line(start[:2], end[:2])
            
            faces = cad_part.document.get('faces', [])
            vertices = cad_part.document.get('vertices', [])
            for face in faces:
                if len(face) >= 3:
                    verts = [vertices[i] for i in face[:3] if i < len(vertices)]
                    if len(verts) >= 3:
                        msp.add_3dface([(v[0], v[1], v[2] if len(v) > 2 else 0) for v in verts])
            
            doc.saveas(str(file_path))
        except ImportError:
            raise ImportError("ezdxf required for DXF export: pip install ezdxf")


class FBXPort(CADPort):
    """Autodesk FBX CAD format port"""
    
    EXTENSIONS = {'.fbx', '.FBX'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import FBX to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        path = Path(file_path)
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        part.document['source_format'] = 'fbx'
        part.document['note'] = 'FBX import requires fbx-sdk or assimp'
        
        try:
            import pyassimp
            scene = pyassimp.load(str(path))
            
            vertices = []
            faces = []
            normals = []
            
            for mesh in scene.meshes:
                offset = len(vertices)
                for i in range(mesh.vertices.shape[0]):
                    v = mesh.vertices[i]
                    vertices.append((float(v[0]), float(v[1]), float(v[2])))
                
                for face in mesh.faces:
                    if len(face) >= 3:
                        faces.append([offset + i for i in face[:3]])
                
                if hasattr(mesh, 'normals') and mesh.normals is not None:
                    for n in mesh.normals:
                        normals.append((float(n[0]), float(n[1]), float(n[2])))
            
            pyassimp.release(scene)
            
            part.document['vertices'] = vertices
            part.document['faces'] = faces
            part.document['normals'] = normals
        except ImportError:
            part.document['error'] = 'pyassimp not installed'
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to FBX"""
        raise NotImplementedError("FBX export requires Autodesk FBX SDK")


class GLTFPort(CADPort):
    """GL Transmission Format (GLTF/GLB) CAD format port"""
    
    EXTENSIONS = {'.gltf', '.glb', '.GLTF', '.GLB'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import GLTF/GLB to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        import json
        path = Path(file_path)
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        is_binary = path.suffix.lower() == '.glb'
        part.document['source_format'] = 'gltf' if not is_binary else 'glb'
        
        if is_binary:
            with open(path, 'rb') as f:
                data = f.read()
            
            if data[:4] == b'glTF':
                part.document['note'] = 'GLB binary format - limited parsing'
        else:
            with open(path, 'r') as f:
                gltf = json.load(f)
            
            part.document['gltf_data'] = gltf
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to GLTF/GLB"""
        import json
        
        path = Path(file_path)
        is_binary = path.suffix.lower() == '.glb'
        
        vertices = cad_part.document.get('vertices', [])
        faces = cad_part.document.get('faces', [])
        
        gltf = {
            "asset": {"version": "2.0", "generator": "Pyffice"},
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0}],
            "meshes": [{
                "primitives": [{
                    "mode": 4,
                    "attributes": {"POSITION": 0}
                }]
            }]
        }
        
        if not is_binary:
            with open(path, 'w') as f:
                json.dump(gltf, f, indent=2)


class IGESPort(CADPort):
    """IGES (Initial Graphics Exchange Specification) CAD format port"""
    
    EXTENSIONS = {'.iges', '.igs', '.IGES', '.IGS'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import IGES to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        path = Path(file_path)
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        part.document['source_format'] = 'iges'
        
        with open(path, 'r') as f:
            content = f.read()
        
        part.document['iges_content'] = content
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to IGES"""
        content = cad_part.document.get('iges_content', '')
        with open(file_path, 'w') as f:
            f.write(content)


class BLENDPort(CADPort):
    """Blender BLEND CAD format port"""
    
    EXTENSIONS = {'.blend', '.BLEND'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import BLEND to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        path = Path(file_path)
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        part.document['source_format'] = 'blend'
        
        try:
            with open(path, 'rb') as f:
                header = f.read(12)
            
            if header[:7] == b'BLENDER':
                part.document['blender_version'] = header[7:].decode('ascii', errors='ignore')
                part.document['note'] = 'Blend file detected'
        except Exception as e:
            part.document['error'] = str(e)
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to BLEND"""
        raise NotImplementedError("BLEND export requires Blender SDK")


class SCADPort(CADPort):
    """OpenSCAD SCAD format port"""
    
    EXTENSIONS = {'.scad', '.SCAD'}
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import SCAD to PyfficeCADPart"""
        from pyffice.cad.cad import PyfficeCADPart  # Lazy import to avoid circular dependency
        import re
        path = Path(file_path)
        part = PyfficeCADPart()
        part.create_new_document(path.stem)
        
        part.document['source_format'] = 'scad'
        
        with open(path, 'r') as f:
            content = f.read()
        
        cubes = re.findall(r'cube\s*\(\s*size\s*=\s*\[([^\]]+)\]', content)
        spheres = re.findall(r'sphere\s*\(\s*r\s*=\s*([0-9.]+)', content)
        cylinders = re.findall(r'cylinder\s*\(\s*r\s*=\s*([0-9.]+)', content)
        
        part.document['cubes'] = cubes
        part.document['spheres'] = spheres
        part.document['cylinders'] = cylinders
        
        return part
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str) -> None:
        """Export PyfficeCADPart to SCAD"""
        from pyffice.cad.scad import PyfficeSCAD
        
        vertices = cad_part.document.get('vertices', [])
        faces = cad_part.document.get('faces', [])
        
        operations = []
        
        for face in faces:
            if len(face) >= 3:
                verts = [vertices[i] for i in face[:3] if i < len(vertices)]
                if verts:
                    ops = f"polyhedron(points={verts}, faces={face})"
                    operations.append(ops)
        
        content = "\n".join(operations)
        
        scad = PyfficeSCAD(str(file_path))
        scad.write(content)


class CADPortsManager:
    """Manages all CAD format ports and conversions"""
    
    def __init__(self):
        self.ports: Dict[str, CADPort] = {}
        self._register_default_ports()
    
    def _register_default_ports(self):
        """Register all default CAD ports"""
        self.ports['stl'] = STLPort()
        self.ports['obj'] = OBJPort()
        self.ports['step'] = STEPPort()
        self.ports['dwg'] = DWGPort()
        self.ports['dxf'] = DXFPort()
        self.ports['fbx'] = FBXPort()
        self.ports['gltf'] = GLTFPort()
        self.ports['glb'] = GLTFPort()
        self.ports['iges'] = IGESPort()
        self.ports['igs'] = IGESPort()
        self.ports['blend'] = BLENDPort()
        self.ports['scad'] = SCADPort()
    
    def register_port(self, format_name: str, port: CADPort) -> None:
        """Register a new CAD format port"""
        self.ports[format_name] = port
    
    def get_port(self, format_name: str) -> Optional[CADPort]:
        """Get port for a specific format"""
        return self.ports.get(format_name.lower())
    
    def import_file(self, file_path: str) -> PyfficeCADPart:
        """Import any supported CAD file to PyfficeCADPart"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for port in self.ports.values():
            if ext in port.EXTENSIONS:
                return port.import_file(str(path))
        
        raise ValueError(f"Unsupported CAD format: {ext}")
    
    def export_file(self, cad_part: PyfficeCADPart, file_path: str, format_name: str = None) -> None:
        """Export PyfficeCADPart to specified format"""
        path = Path(file_path)
        
        if format_name is None:
            format_name = path.suffix.lower().lstrip('.')
        
        port = self.ports.get(format_name.lower())
        if port is None:
            raise ValueError(f"Unsupported CAD format: {format_name}")
        
        port.export_file(cad_part, str(path))
    
    def convert(self, input_path: str, output_path: str) -> PyfficeCADPart:
        """Convert between CAD formats"""
        part = self.import_file(input_path)
        self.export_file(part, output_path)
        return part
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported format extensions"""
        formats = set()
        for port in self.ports.values():
            formats.update(port.EXTENSIONS)
        return sorted(list(formats))


# Global port manager instance
_port_manager = None

def get_ports_manager() -> CADPortsManager:
    """Get global CAD ports manager instance"""
    global _port_manager
    if _port_manager is None:
        _port_manager = CADPortsManager()
    return _port_manager


def import_cad(file_path: str) -> PyfficeCADPart:
    """Convenience function to import CAD file"""
    return get_ports_manager().import_file(file_path)


def export_cad(cad_part: PyfficeCADPart, file_path: str) -> None:
    """Convenience function to export CAD file"""
    get_ports_manager().export_file(cad_part, file_path)


def convert_cad(input_path: str, output_path: str) -> PyfficeCADPart:
    """Convenience function to convert between CAD formats"""
    return get_ports_manager().convert(input_path, output_path)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
