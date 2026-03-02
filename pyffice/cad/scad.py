"""
Pyffice SCAD Module - Handle OpenSCAD files
"""

from typing import Dict, Any, List
from pathlib import Path
import re


class PyfficeSCAD:
    """Handle OpenSCAD 3D model files"""
    
    SUPPORTED_EXTENSIONS = ['.scad']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self) -> Dict[str, Any]:
        """Read SCAD file and extract structure"""
        with open(self.file_path, 'r') as f:
            content = f.read()
        
        return {
            'content': content,
            'modules': self._extract_modules(content),
            'variables': self._extract_variables(content),
            'operations': self._extract_operations(content),
        }
    
    def _extract_modules(self, content: str) -> List[Dict[str, Any]]:
        """Extract module definitions"""
        modules = []
        pattern = r'module\s+(\w+)\s*\(([^)]*)\)\s*\{([^}]*)\}'
        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            modules.append({
                'name': match.group(1),
                'params': match.group(2),
                'body': match.group(3).strip(),
            })
        return modules
    
    def _extract_variables(self, content: str) -> Dict[str, Any]:
        """Extract variable assignments"""
        variables = {}
        pattern = r'(\w+)\s*=\s*([^;]+);'
        for match in re.finditer(pattern, content):
            var_name = match.group(1)
            var_value = match.group(2).strip()
            try:
                variables[var_name] = eval(var_value)
            except:
                variables[var_name] = var_value
        return variables
    
    def _extract_operations(self, content: str) -> List[str]:
        """Extract 3D operations"""
        operations = ['cube', 'sphere', 'cylinder', 'rotate', 'translate', 
                       'scale', 'union', 'difference', 'intersection', 'linear_extrude',
                       'rotate_extrude', 'import', 'render', 'color', 'multmatrix']
        found = []
        for op in operations:
            if re.search(rf'\b{op}\s*\(', content):
                found.append(op)
        return found
    
    def write(self, content: str, output_path: str = None):
        """Write content to SCAD file"""
        output = Path(output_path) if output_path else self.file_path
        with open(output, 'w') as f:
            f.write(content)
    
    def render(self, output_path: str = None) -> bytes:
        """Render SCAD to STL (requires OpenSCAD)"""
        import subprocess
        output = output_path or str(self.file_path.with_suffix('.stl'))
        cmd = ['openscad', '-o', output, str(self.file_path)]
        subprocess.run(cmd, check=True, capture_output=True)
        return output


def read_scad(file_path: str) -> Dict[str, Any]:
    """Convenience function to read SCAD"""
    return PyfficeSCAD(file_path).read()


def write_scad(file_path: str, content: str):
    """Convenience function to write SCAD"""
    PyfficeSCAD(file_path).write(content)
