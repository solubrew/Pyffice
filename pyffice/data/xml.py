"""
Pyffice XML Data Handler
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Any


def parse(filepath: str) -> ET.Element:
    """Parse XML file and return root element."""
    tree = ET.parse(filepath)
    return tree.getroot()


def read(filepath: str) -> Dict[str, Any]:
    """Read XML file and convert to dictionary."""
    root = parse(filepath)
    return _element_to_dict(root)


def write(filepath: str, data: Dict[str, Any], root_tag: str = "root") -> None:
    """Write dictionary to XML file."""
    root = _dict_to_element(root_tag, data)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(filepath, encoding="utf-8", xml_declaration=True)


def create(root_tag: str = "root") -> ET.Element:
    """Create new XML root element."""
    return ET.Element(root_tag)


def add_child(parent: ET.Element, tag: str, text: str = "", attrib: Dict = None) -> ET.Element:
    """Add child element to parent."""
    child = ET.SubElement(parent, tag, attrib or {})
    child.text = text
    return child


def _element_to_dict(element: ET.Element) -> Dict:
    """Convert XML element to dictionary."""
    result = {}
    if element.attrib:
        result["@attributes"] = element.attrib
    if element.text and element.text.strip():
        result["#text"] = element.text.strip()
    for child in element:
        child_data = _element_to_dict(child)
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
    return result if result else (element.text.strip() if element.text else "")


def _dict_to_element(tag: str, data: Any) -> ET.Element:
    """Convert dictionary to XML element."""
    element = ET.Element(tag)
    if isinstance(data, dict):
        if "@attributes" in data:
            element.attrib.update(data["@attributes"])
        for key, value in data.items():
            if key == "@attributes":
                continue
            if isinstance(value, list):
                for item in value:
                    child = _dict_to_element(key, item)
                    element.append(child)
            else:
                child = _dict_to_element(key, value)
                element.append(child)
    else:
        element.text = str(data)
    return element
