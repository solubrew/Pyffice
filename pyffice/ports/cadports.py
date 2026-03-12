# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: CAD Ports Module
	description: >
		External CAD format ports - converts all external CAD formats to/from
		NchantdCADPart universal format. Includes STL, OBJ, STEP, DWG, DXF, FBX,
		GLTF, IGES, BLEND, SCAD and other proprietary/external formats.
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
from pathlib import Path

# ======================================3rd Party Library Modules=====================================================||
# ======================================Solutions Brewer Library Modules==============================================||
from pyffice.ports.cad import NchantdCADPart, CADPort


# ====================================================================================================================||


class STLPort(CADPort):
    """STL (Stereolithography) CAD format port"""
    
    EXTENSIONS = {'.stl', '.STL'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import STL to NchantdCADPart"""
        from pyffice.cad.stl import PyfficeSTL
        path = Path(file_path)
        stl = PyfficeSTL(str(path))
        data = stl.read()
        
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'stl'
        
        for face in data.get('faces', []):
            verts = face.get('vertices', [])
            if len(verts) >= 3:
                start_idx = len(part.vertices)
                for v in verts:
                    part.vertices.append(v)
                part.faces.append([start_idx, start_idx+1, start_idx+2])
                part.normals.append(face.get('normal', (0, 0, 1)))
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to STL"""
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
        from pyffice.cad.step import PyfficeSTEP
        path = Path(file_path)
        step = PyfficeSTEP(str(path))
        content = step.read()
        
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'step'
        part.metadata['step_content'] = content
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to STEP"""
        from pyffice.cad.step import PyfficeSTEP
        
        content = cad_part.metadata.get('step_content', '')
        step = PyfficeSTEP(str(file_path))
        step.write(content)


class DWGPort(CADPort):
    """Autodesk DWG CAD format port"""
    
    EXTENSIONS = {'.dwg', '.DWG'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import DWG to NchantdCADPart"""
        # DWG is proprietary - requires ODA SDK or ezdxf for conversion
        # This is a placeholder implementation
        path = Path(file_path)
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'dwg'
        part.metadata['note'] = 'DWG import requires ODA SDK or ezdxf'
        
        # Try using ezdxf if available
        try:
            import ezdxf
            doc = ezdxf.readfile(str(path))
            # Convert entities to geometry
            msp = doc.modelspace()
            for entity in msp:
                if entity.dxftype() == 'LINE':
                    # Add line as edge
                    start = entity.dxf.start
                    end = entity.dxf.end
                    part.edges.append((
                        (start.x, start.y, start.z),
                        (end.x, end.y, end.z)
                    ))
        except ImportError:
            pass
        except Exception:
            pass
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to DWG"""
        # DWG export requires ODA SDK - placeholder
        raise NotImplementedError("DWG export requires Autodesk ODA SDK")


class DXFPort(CADPort):
    """AutoCAD DXF CAD format port"""
    
    EXTENSIONS = {'.dxf', '.DXF'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import DXF to NchantdCADPart"""
        path = Path(file_path)
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'dxf'
        
        try:
            import ezdxf
            doc = ezdxf.readfile(str(path))
            msp = doc.modelspace()
            
            for entity in msp:
                if entity.dxftype() == 'LINE':
                    start = entity.dxf.start
                    end = entity.dxf.end
                    part.edges.append((
                        (start.x, start.y, start.z),
                        (end.x, end.y, end.z)
                    ))
                elif entity.dxftype() == 'CIRCLE':
                    # Approximate circle with polygon
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    segments = 32
                    for i in range(segments):
                        angle1 = 2 * 3.14159 * i / segments
                        angle2 = 2 * 3.14159 * (i + 1) / segments
                        part.edges.append((
                            (center.x + radius * 0.5 * 0.5, center.y + radius * 0.5, 0),
                            (center.x + radius * 0.5, center.y, 0)
                        ))
                elif entity.dxftype() == 'VERTEX':
                    # Point vertex
                    point = entity.dxf.location
                    part.vertices.append((point.x, point.y, point.z))
                elif entity.dxftype() == 'POLYLINE':
                    # Polyline - collect vertices
                    pass
                elif entity.dxftype() == '3DFACE':
                    # 3D Face
                    vertices = []
                    for i in range(4):
                        v = getattr(entity.dxf, f'v{i}', None)
                        if v:
                            vertices.append((v.x, v.y, v.z))
                    if len(vertices) >= 3:
                        start_idx = len(part.vertices)
                        part.vertices.extend(vertices[:3])
                        part.faces.append([start_idx, start_idx+1, start_idx+2])
        except ImportError:
            part.metadata['note'] = 'ezdxf not installed - DXF parsing limited'
        except Exception as e:
            part.metadata['error'] = str(e)
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to DXF"""
        try:
            import ezdxf
            from ezdxf.document import Drawing
            
            doc = ezdxf.new('R2010')
            msp = doc.modelspace()
            
            # Add edges as lines
            for edge in cad_part.edges:
                if len(edge) == 2:
                    start, end = edge
                    msp.add_line(
                        (start[0], start[1], start[2] if len(start) > 2 else 0),
                        (end[0], end[1], end[2] if len(end) > 2 else 0)
                    )
            
            # Add faces as 3DFACE
            for face in cad_part.faces:
                if len(face) >= 3:
                    verts = [cad_part.vertices[i] for i in face[:3] if i < len(cad_part.vertices)]
                    if len(verts) >= 3:
                        msp.add_3dface([
                            (v[0], v[1], v[2] if len(v) > 2 else 0) for v in verts
                        ])
            
            doc.saveas(str(file_path))
        except ImportError:
            raise ImportError("ezdxf required for DXF export: pip install ezdxf")


class FBXPort(CADPort):
    """Autodesk FBX CAD format port"""
    
    EXTENSIONS = {'.fbx', '.FBX'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import FBX to NchantdCADPart"""
        path = Path(file_path)
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'fbx'
        part.metadata['note'] = 'FBX import requires fbx-sdk or assimp'
        
        # Try using pyassimp if available
        try:
            import pyassimp
            scene = pyassimp.load(str(path))
            
            for mesh in scene.meshes:
                # Vertices
                offset = len(part.vertices)
                for i in range(mesh.vertices.shape[0]):
                    v = mesh.vertices[i]
                    part.vertices.append((float(v[0]), float(v[1]), float(v[2])))
                
                # Faces
                for face in mesh.faces:
                    if len(face) >= 3:
                        part.faces.append([offset + i for i in face[:3]])
                
                # Normals
                if hasattr(mesh, 'normals') and mesh.normals is not None:
                    for n in mesh.normals:
                        part.normals.append((float(n[0]), float(n[1]), float(n[2])))
            
            pyassimp.release(scene)
        except ImportError:
            pass
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to FBX"""
        raise NotImplementedError("FBX export requires Autodesk FBX SDK")


class GLTFPort(CADPort):
    """GL Transmission Format (GLTF/GLB) CAD format port"""
    
    EXTENSIONS = {'.gltf', '.glb', '.GLTF', '.GLB'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import GLTF/GLB to NchantdCADPart"""
        import json
        path = Path(file_path)
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'gltf'
        
        is_binary = path.suffix.lower() == '.glb'
        
        if is_binary:
            # GLB is binary - parse manually
            with open(path, 'rb') as f:
                data = f.read()
            
            # Check GLB magic
            if data[:4] == b'glTF':
                # Parse GLB chunks
                # This is simplified - full implementation would parse properly
                part.metadata['note'] = 'GLB binary format - limited parsing'
        else:
            # GLTF is JSON
            with open(path, 'r') as f:
                gltf = json.load(f)
            
            # Get accessor data
            buffers = gltf.get('buffers', [])
            buffer_views = gltf.get('bufferViews', [])
            accessors = gltf.get('accessors', [])
            
            # Get mesh data
            meshes = gltf.get('meshes', [])
            for mesh in meshes:
                primitives = mesh.get('primitives', [])
                for prim in primitives:
                    # Position attribute
                    pos_attr = prim.get('attributes', {}).get('POSITION')
                    if pos_attr is not None:
                        accessor = accessors[pos_attr]
                        bv = buffer_views[accessor['bufferView']]
                        # Would need to read binary data
                        part.metadata['mesh_note'] = 'Binary data not parsed'
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to GLTF/GLB"""
        import json
        
        path = Path(file_path)
        is_binary = path.suffix.lower() == '.glb'
        
        # Build GLTF structure
        gltf = {
            "asset": {"version": "2.0", "generator": "Pyffice"},
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0}],
            "meshes": [{
                "primitives": [{
                    "mode": 4,  # TRIANGLES
                    "attributes": {"POSITION": 0},
                    "indices": 1 if cad_part.faces else None
                }.copy()]
            }],
            "accessors": [],
            "bufferViews": [],
            "buffers": [{"byteLength": 0}]
        }
        
        # This is a placeholder - full implementation would write binary data
        part.metadata['note'] = 'GLTF export needs binary buffer implementation'
        
        if not is_binary:
            with open(path, 'w') as f:
                json.dump(gltf, f, indent=2)


class IGESPort(CADPort):
    """IGES (Initial Graphics Exchange Specification) CAD format port"""
    
    EXTENSIONS = {'.iges', '.igs', '.IGES', '.IGS'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import IGES to NchantdCADPart"""
        path = Path(file_path)
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'iges'
        
        # Parse IGES file (text-based format)
        with open(path, 'r') as f:
            lines = f.readlines()
        
        # IGES entities - look for 116 (Copious Data) and 188 (Trimmed Parametric Surface)
        vertices = []
        for line in lines:
            if len(line) > 72:
                try:
                    # Entity type is in chars 64-71
                    entity_type = int(line[63:72].strip())
                    
                    if entity_type == 116:  # Copious Data (points/curves)
                        # Parse coordinate data
                        data = line[72:].strip()
                        # Simplified parsing
                        pass
                    elif entity_type == 188:  # Trimmed Surface
                        part.metadata['has_surfaces'] = True
                except (ValueError, IndexError):
                    pass
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to IGES"""
        # IGES export - placeholder
        raise NotImplementedError("IGES export not yet implemented")


class BLENDPort(CADPort):
    """Blender BLEND CAD format port"""
    
    EXTENSIONS = {'.blend', '.BLEND'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import BLEND to NchantdCADPart"""
        path = Path(file_path)
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'blend'
        part.metadata['note'] = 'BLEND import requires blender-python or io_scene'
        
        # Try using blender-less parser
        try:
            # Blend files have a specific header
            with open(path, 'rb') as f:
                header = f.read(12)
            
            if header[:7] == b'BLENDER':
                part.metadata['blender_version'] = header[7:].decode('ascii', errors='ignore')
                part.metadata['note'] = 'Blend file detected - full parsing needs blender'
        except Exception as e:
            part.metadata['error'] = str(e)
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to BLEND"""
        raise NotImplementedError("BLEND export requires Blender SDK")


class SCADPort(CADPort):
    """OpenSCAD SCAD format port"""
    
    EXTENSIONS = {'.scad', '.SCAD'}
    
    def import_to_common(self, file_path: str) -> NchantdCADPart:
        """Import SCAD to NchantdCADPart"""
        path = Path(file_path)
        part = NchantdCADPart(name=path.stem)
        part.source_format = 'scad'
        
        # Parse OpenSCAD file - look for geometric primitives
        with open(path, 'r') as f:
            content = f.read()
        
        # Very basic parsing - look for known primitives
        import re
        
        # cube(size = [x, y, z])
        cubes = re.findall(r'cube\s*\(\s*size\s*=\s*\[([^\]]+)\]', content)
        for i, cube in enumerate(cubes):
            dims = [float(x.strip()) for x in cube.split(',')]
            if len(dims) >= 3:
                # Add as a box
                part.metadata[f'cube_{i}'] = dims
        
        # sphere(r = radius)
        spheres = re.findall(r'sphere\s*\(\s*r\s*=\s*([0-9.]+)', content)
        part.metadata['spheres'] = spheres
        
        # cylinder(r = radius, h = height)
        cylinders = re.findall(r'cylinder\s*\(\s*r\s*=\s*([0-9.]+)', content)
        part.metadata['cylinders'] = cylinders
        
        # union(), difference(), intersection()
        part.metadata['has_operations'] = 'union' in content or 'difference' in content
        
        return part
    
    def export_from_common(self, cad_part: NchantdCADPart, file_path: str) -> None:
        """Export NchantdCADPart to SCAD"""
        from pyffice.cad.scad import PyfficeSCAD
        
        scad = PyfficeSCAD(str(file_path))
        
        # Convert NchantdCADPart back to SCAD
        # This is a basic implementation
        operations = []
        
        for face in cad_part.faces:
            if len(face) >= 3:
                operations.append(f"polyhedron(points={cad_part.vertices}, faces={face})")
        
        content = "\n".join(operations)
        scad.write(content)


class CADPortsManager:
    """Manages all CAD format ports and conversions"""
    
    def __init__(self):
        self.ports: Dict[str, CADPort] = {
            'stl': STLPort(),
            'obj': OBJPort(),
            'step': STEPPort(),
            'dwg': DWGPort(),
            'dxf': DXFPort(),
            'fbx': FBXPort(),
            'gltf': GLTFPort(),
            'gltf_binary': GLTFPort(),
            'iges': IGESPort(),
            'blend': BLENDPort(),
            'scad': SCADPort(),
        }
    
    def register_port(self, format_name: str, port: CADPort) -> None:
        """Register a new CAD format port"""
        self.ports[format_name] = port
    
    def get_port(self, format_name: str) -> Optional[CADPort]:
        """Get port for a specific format"""
        return self.ports.get(format_name.lower())
    
    def import_file(self, file_path: str) -> NchantdCADPart:
        """Import any supported CAD file to NchantdCADPart"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        # Handle GLTF/GLB
        if ext == '.glb':
            ext = '.gltf_binary'
        
        for format_name, port in self.ports.items():
            if ext in port.EXTENSIONS:
                return port.import_to_common(path)
        
        raise ValueError(f"Unsupported CAD format: {ext}")
    
    def export_file(self, cad_part: NchantdCADPart, file_path: str, format_name: str = None) -> None:
        """Export NchantdCADPart to specified format"""
        path = Path(file_path)
        
        if format_name is None:
            format_name = path.suffix.lower().lstrip('.')
        
        port = self.ports.get(format_name.lower())
        if port is None:
            raise ValueError(f"Unsupported CAD format: {format_name}")
        
        port.export_from_common(cad_part, path)
    
    def convert(self, input_path: str, output_path: str) -> NchantdCADPart:
        """Convert between CAD formats"""
        common = self.import_file(input_path)
        self.export_file(common, output_path)
        return common
    
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


def import_cad(file_path: str) -> NchantdCADPart:
    """Convenience function to import CAD file"""
    return get_ports_manager().import_file(file_path)


def export_cad(cad_part: NchantdCADPart, file_path: str) -> None:
    """Convenience function to export CAD file"""
    get_ports_manager().export_file(cad_part, file_path)


def convert_cad(input_path: str, output_path: str) -> NchantdCADPart:
    """Convenience function to convert between CAD formats"""
    return get_ports_manager().convert(input_path, output_path)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
