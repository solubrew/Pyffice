"""
Pyffice XML Module - Read/Write XML files
"""

import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class PyfficeXML:
    """Handle XML file operations"""
    
    SUPPORTED_EXTENSIONS = ['.xml', '.xhtml', '.svg']
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = Path(file_path)
        self.encoding = encoding
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.MAX_SIZE:
            raise ValueError(f"File exceeds {self.MAX_SIZE}MB limit")
    
    def read(self) -> ET.Element:
        """Read and parse XML file"""
        return ET.parse(self.file_path).getroot()
    
    def read_string(self) -> str:
        """Read raw XML string"""
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            return f.read()
    
    def write(self, root: ET.Element, indent: bool = True):
        """Write Element to XML file"""
        if indent:
            self._indent(root)
        tree = ET.ElementTree(root)
        tree.write(self.file_path, encoding=self.encoding, xml_declaration=True)
    
    def write_string(self, root: ET.Element) -> str:
        """Convert Element to XML string"""
        if hasattr(root, 'tag'):
            return ET.tostring(root, encoding=self.encoding)
        return str(root)
    
    def _indent(self, elem: ET.Element, level: int = 0):
        """Add indentation to XML tree"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


def read_xml(file_path: str) -> ET.Element:
    """Convenience function to read XML"""
    return PyfficeXML(file_path).read()


def write_xml(file_path: str, root: ET.Element, **kwargs):
    """Convenience function to write XML"""
    PyfficeXML(file_path).write(root, **kwargs)


def element_to_dict(element: ET.Element) -> Dict:
    """Convert XML Element to dictionary"""
    result = {}
    if element.attrib:
        result['@attributes'] = element.attrib
    if element.text and element.text.strip():
        if len(element) == 0:
            return element.text.strip()
        result['#text'] = element.text.strip()
    for child in element:
        child_data = element_to_dict(child)
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
    return result
