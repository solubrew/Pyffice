"""
Pyffice DXF Module - Handle DXF CAD files
"""

from typing import Dict, Any, List
from pathlib import Path
import re


class PyfficeDXF:
    """Handle DXF CAD files"""
    
    SUPPORTED_EXTENSIONS = ['.dxf']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self) -> Dict[str, Any]:
        """Read DXF file and extract entities"""
        with open(self.file_path, 'r') as f:
            lines = [line.rstrip() for line in f]
        
        entities = []
        i = 0
        current_entity = {}
        
        while i < len(lines) - 1:
            try:
                code = int(lines[i].strip())
                value = lines[i + 1].strip()
                
                if code == 0:
                    if current_entity:
                        entities.append(current_entity)
                    current_entity = {'type': value}
                elif code == 62:
                    current_entity['color'] = value
                elif code == 8:
                    current_entity['layer'] = value
                elif code in [10, 20, 30]:
                    if 'point' not in current_entity:
                        current_entity['point'] = [0, 0, 0]
                    current_entity['point'][code // 10 - 1] = float(value)
                elif code in [11, 21, 31]:
                    if 'endpoint' not in current_entity:
                        current_entity['endpoint'] = [0, 0, 0]
                    current_entity['endpoint'][code // 11 - 1] = float(value)
                elif code in [12, 22, 32]:
                    if 'center' not in current_entity:
                        current_entity['center'] = [0, 0, 0]
                    current_entity['center'][code // 12 - 1] = float(value)
                elif code == 40:
                    current_entity['radius'] = float(value)
                elif code == 70:
                    current_entity['flags'] = int(value)
                else:
                    current_entity[f'code_{code}'] = value
                
                i += 2
            except (ValueError, IndexError):
                i += 1
        
        if current_entity:
            entities.append(current_entity)
        
        return {
            'entities': entities,
            'entity_count': len(entities),
            'layers': list(set(e.get('layer', '0') for e in entities)),
        }
    
    def write(self, entities: List[Dict[str, Any]], output_path: str = None):
        """Write entities to DXF file"""
        output = Path(output_path) if output_path else self.file_path
        
        with open(output, 'w') as f:
            # Header
            f.write("0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1006\n0\nENDSEC\n")
            
            # Tables
            f.write("0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n70\n0\n0\nENDTAB\n0\nENDSEC\n")
            
            # Entities
            f.write("0\nSECTION\n2\nENTITIES\n")
            
            for entity in entities:
                f.write(f"0\n{entity.get('type', 'LINE')}\n")
                
                if 'layer' in entity:
                    f.write(f"8\n{entity['layer']}\n")
                if 'color' in entity:
                    f.write(f"62\n{entity['color']}\n")
                if 'point' in entity:
                    f.write(f"10\n{entity['point'][0]}\n20\n{entity['point'][1]}\n30\n{entity['point'][2]}\n")
                if 'endpoint' in entity:
                    f.write(f"11\n{entity['endpoint'][0]}\n21\n{entity['endpoint'][1]}\n31\n{entity['endpoint'][2]}\n")
                if 'radius' in entity:
                    f.write(f"40\n{entity['radius']}\n")
            
            f.write("0\nENDSEC\n0\nEOF\n")


def read_dxf(file_path: str) -> Dict[str, Any]:
    """Convenience function to read DXF"""
    return PyfficeDXF(file_path).read()


def write_dxf(file_path: str, entities: List[Dict[str, Any]]):
    """Convenience function to write DXF"""
    PyfficeDXF(file_path).write(entities)
