"""
Pyffice Diagrams Ports - Import/Export converters for diagram formats.
"""

from pyffice.diagrams.diagrams import PyfficeDiagram


class MermaidPort:
    """Port for Mermaid diagram format."""
    
    @staticmethod
    def to_pyffice(mermaid_code: str) -> PyfficeDiagram:
        return PyfficeDiagram(format='mermaid', code=mermaid_code)
    
    @staticmethod
    def from_pyffice(diagram: PyfficeDiagram) -> str:
        return diagram.code


class PlantUMLPort:
    """Port for PlantUML diagram format."""
    
    @staticmethod
    def to_pyffice(plantuml_code: str) -> PyfficeDiagram:
        return PyfficeDiagram(format='plantuml', code=plantuml_code)
    
    @staticmethod
    def from_pyffice(diagram: PyfficeDiagram) -> str:
        return diagram.code


class GraphMLPort:
    """Port for GraphML diagram format."""
    
    @staticmethod
    def to_pyffice(graphml_data: str) -> PyfficeDiagram:
        return PyfficeDiagram(format='graphml', data=graphml_data)
    
    @staticmethod
    def from_pyffice(diagram: PyfficeDiagram) -> str:
        return diagram.data


class DOTPort:
    """Port for DOT/Graphviz diagram format."""
    
    @staticmethod
    def to_pyffice(dot_code: str) -> PyfficeDiagram:
        return PyfficeDiagram(format='dot', code=dot_code)
    
    @staticmethod
    def from_pyffice(diagram: PyfficeDiagram) -> str:
        return diagram.code


class DrawIOPort:
    """Port for Draw.io diagram format."""
    
    @staticmethod
    def to_pyffice(drawio_xml: str) -> PyfficeDiagram:
        return PyfficeDiagram(format='drawio', data=drawio_xml)
    
    @staticmethod
    def from_pyffice(diagram: PyfficeDiagram) -> str:
        return diagram.data


class PortRegistry:
    """Registry of all diagram ports."""
    
    PORTS = {
        'mermaid': MermaidPort,
        'plantuml': PlantUMLPort,
        'graphml': GraphMLPort,
        'dot': DOTPort,
        'drawio': DrawIOPort,
    }
    
    @classmethod
    def get_port(cls, format: str):
        return cls.PORTS.get(format.lower())
    
    @classmethod
    def list_formats(cls):
        return list(cls.PORTS.keys())
