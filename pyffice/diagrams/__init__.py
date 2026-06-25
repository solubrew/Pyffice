# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid:
    name:
    description: >
    version: 0.0.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||

# ======================================3rd Party Library Modules=====================================================||
# from PIL import Image, ImageDraw, ImageFont

# ======================================Solutions Brewer Library Modules==============================================||

# ====================================================================================================================||

from pyffice.diagrams.diagrams import PyfficeEdge, PyfficeLayer, PyfficeNode, PyfficeSketch, PyfficeSketchConnection

# PyfficeDiagram alias for PyfficeSketch (backward compatibility)
PyfficeDiagram = PyfficeSketch

# Diagram format converters
from pyffice.diagrams.formats import (
    DiagramConverter,
    DiaConverter,
    DotConverter,
    GraphMLConverter,
    SVGConverter,
    DrawIOConverter,
    FreemindConverter,
    VSDXConverter,
    XMindConverter,
    BPMNConverter,
    MindManagerConverter,
    get_converter,
    load_diagram,
    save_diagram,
    DIAGRAM_FORMATS,
)

# ====================================================================================================================||

__all__ = [
    # Core diagram classes
    "PyfficeEdge",
    "PyfficeLayer",
    "PyfficeNode",
    "PyfficeSketch",
    "PyfficeSketchConnection",
    "PyfficeDiagram",  # Alias for PyfficeSketch
    # Converters
    "DiagramConverter",
    "DiaConverter",
    "DotConverter",
    "GraphMLConverter",
    "SVGConverter",
    "DrawIOConverter",
    "FreemindConverter",
    "VSDXConverter",
    "XMindConverter",
    "BPMNConverter",
    "MindManagerConverter",
    # Utilities
    "get_converter",
    "load_diagram",
    "save_diagram",
    "DIAGRAM_FORMATS",
]

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
