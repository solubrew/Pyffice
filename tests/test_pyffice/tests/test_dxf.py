"""Test DXF CAD file handling."""
import pytest
import tempfile
import os
from pathlib import Path


def test_read_dxf():
    """Test reading DXF files."""
    # Create a minimal DXF file for testing
    dxf_content = """0
SECTION
2
ENTITIES
0
LINE
8
0
10
0.0
20
0.0
30
0.0
11
10.0
21
10.0
31
0.0
0
ENDSEC
0
EOF
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.dxf', delete=False) as f:
        f.write(dxf_content)
        temp_path = f.name
    
    try:
        from pyffice.cad.dxf import read_dxf
        # Test reading the DXF file
        entities = read_dxf(temp_path)
        assert entities is not None
    finally:
        os.unlink(temp_path)


def test_write_dxf():
    """Test writing DXF files."""
    from pyffice.cad.dxf import write_dxf
    
    entities = [
        {"type": "LINE", "start": (0, 0, 0), "end": (10, 10, 0), "layer": "0"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.dxf', delete=False) as f:
        temp_path = f.name
    
    try:
        write_dxf(entities, temp_path)
        assert os.path.exists(temp_path)
        assert os.path.getsize(temp_path) > 0
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
