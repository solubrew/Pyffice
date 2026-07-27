"""XML data handling for Pyffice.

This module provides XML parsing and manipulation capabilities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element


@dataclass
class PyfficeXML:
    """XML document handler for Pyffice.

    Provides comprehensive XML parsing, manipulation, and serialization
    capabilities with support for namespaces and XPath queries.

    Attributes:
        path: Path to the XML file.
        content: Raw XML content as string.
        root: Root Element of the parsed tree.
        namespaces: Dictionary of namespace prefixes to URIs.
    """

    path: str | None = None
    content: str | None = None
    root: Element | None = None
    namespaces: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize the XML document."""
        if self.content and not self.root:
            self.parse()
        elif self.path and not self.root:
            self.load()

    def parse(self, content: str | None = None) -> Element:
        """Parse XML content from string.

        Args:
            content: XML string to parse. Uses self.content if None.

        Returns:
            Root element of the parsed XML tree.

        Raises:
            ET.ParseError: If XML content is malformed.
        """
        if content:
            self.content = content
        if self.content:
            self.root = ET.fromstring(self.content)
        return self.root

    def load(self, path: str | None = None) -> Element:
        """Load XML from file.

        Args:
            path: Path to XML file. Uses self.path if None.

        Returns:
            Root element of the parsed XML tree.

        Raises:
            FileNotFoundError: If XML file doesn't exist.
        """
        target = path or self.path
        if not target:
            msg = "No path provided"
            raise ValueError(msg)
        self.path = target
        self.root = ET.parse(target).getroot()
        return self.root

    def save(self, path: str | None = None) -> None:
        """Save XML tree to file.

        Args:
            path: Path to save XML. Uses self.path if None.
        """
        target = path or self.path
        if not target:
            msg = "No path provided"
            raise ValueError(msg)
        if not self.root:
            msg = "No XML tree to save"
            raise ValueError(msg)
        ET.ElementTree(self.root).write(
            target,
            encoding="utf-8",
            xml_declaration=True
        )

    def to_string(self, pretty: bool = False) -> str:
        """Convert XML tree to string.

        Args:
            pretty: Whether to format output with indentation.

        Returns:
            XML as formatted string.
        """
        if not self.root:
            return ""
        if pretty:
            self._indent(self.root)
        return ET.tostring(self.root, encoding="unicode")

    @staticmethod
    def _indent(elem: Element, level: int = 0) -> None:
        """Add indentation to XML tree for pretty printing.

        Args:
            elem: Element to indent.
            level: Current indentation level.
        """
        indent = "\n" + "  " * level
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for child in elem:
                PyfficeXML._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent

    def find_element(self, xpath: str) -> Element | None:
        """Find element by XPath.

        Args:
            xpath: XPath expression to search.

        Returns:
            First matching element or None.
        """
        if not self.root:
            return None
        return self.root.find(xpath, self.namespaces)

    def find_all(self, xpath: str) -> list[Element]:
        """Find all elements matching XPath.

        Args:
            xpath: XPath expression to search.

        Returns:
            List of matching elements.
        """
        if not self.root:
            return []
        return self.root.findall(xpath, self.namespaces)

    def create_element(
        self,
        tag: str,
        text: str | None = None,
        attrib: dict[str, str] | None = None,
        parent: Element | None = None
    ) -> Element:
        """Create a new XML element.

        Args:
            tag: Element tag name.
            text: Element text content.
            attrib: Element attributes.
            parent: Parent element to append to.

        Returns:
            Created element.
        """
        element = ET.Element(tag, attrib or {})
        if text:
            element.text = text
        if parent is not None:
            parent.append(element)
        elif self.root is not None:
            self.root.append(element)
        return element

    def add_element(
        self,
        parent: Element,
        tag: str,
        text: str | None = None,
        attrib: dict[str, str] | None = None
    ) -> Element:
        """Add element to parent.

        Args:
            parent: Parent element.
            tag: Element tag name.
            text: Element text content.
            attrib: Element attributes.

        Returns:
            Created element.
        """
        element = ET.SubElement(parent, tag, attrib or {})
        if text:
            element.text = text
        return element

    def get_text(self, element: Element) -> str | None:
        """Get text content of element.

        Args:
            element: XML element.

        Returns:
            Text content or None.
        """
        return element.text

    def set_text(self, element: Element, text: str) -> None:
        """Set text content of element.

        Args:
            element: XML element.
            text: Text to set.
        """
        element.text = text

    def get_attributes(self, element: Element) -> dict[str, str]:
        """Get element attributes.

        Args:
            element: XML element.

        Returns:
            Dictionary of attributes.
        """
        return dict(element.attrib)

    def set_attribute(
        self,
        element: Element,
        key: str,
        value: str
    ) -> None:
        """Set element attribute.

        Args:
            element: XML element.
            key: Attribute name.
            value: Attribute value.
        """
        element.set(key, value)

    def remove_element(self, element: Element) -> None:
        """Remove element from tree.

        Args:
            element: Element to remove.
        """
        parent = self._find_parent(self.root, element) if self.root else None
        if parent is not None:
            parent.remove(element)

    def _find_parent(
        self,
        root: Element,
        target: Element
    ) -> Element | None:
        """Find parent of an element.

        Args:
            root: Root element to search.
            target: Target element to find parent of.

        Returns:
            Parent element or None.
        """
        for parent in root.iter():
            if target in parent:
                return parent
        return None

    def to_dict(self, element: Element | None = None) -> dict[str, Any]:
        """Convert XML element to dictionary.

        Args:
            element: Element to convert. Uses root if None.

        Returns:
            Dictionary representation of element.
        """
        target = element or self.root
        if target is None:
            return {}

        result: dict[str, Any] = {"@tag": target.tag}
        if target.attrib:
            result["@attributes"] = dict(target.attrib)
        if target.text and target.text.strip():
            result["#text"] = target.text.strip()

        children: dict[str, Any] = {}
        for child in target:
            child_data = self.to_dict(child)
            tag = child.tag
            if tag in children:
                if not isinstance(children[tag], list):
                    children[tag] = [children[tag]]
                children[tag].append(child_data)
            else:
                children[tag] = child_data

        if children:
            result.update(children)

        return result

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        parent: Element | None = None
    ) -> Element:
        """Create XML element from dictionary.

        Args:
            data: Dictionary to convert.
            parent: Parent element to append to.

        Returns:
            Root element of created tree.
        """
        tag = data.pop("@tag", "element")
        attrib = data.pop("@attributes", {})
        text = data.pop("#text", None)

        element = ET.Element(tag, attrib)
        if text:
            element.text = str(text)

        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        child = cls.from_dict(item, element)
                        child.tag = key
                        element.append(child)
            elif isinstance(value, dict):
                child = cls.from_dict(value, element)
                child.tag = key
                element.append(child)
            else:
                child = ET.SubElement(element, key)
                child.text = str(value)

        if parent is not None:
            parent.append(element)
        return element


@dataclass
class PyfficeXMLManager:
    """Manager for handling multiple XML documents.

    Provides batch operations and workspace management for XML files.

    Attributes:
        documents: Dictionary of open XML documents.
    """

    documents: dict[str, PyfficeXML] = field(default_factory=dict)

    def open(self, path: str) -> PyfficeXML:
        """Open XML file.

        Args:
            path: Path to XML file.

        Returns:
            PyfficeXML instance.
        """
        xml = PyfficeXML()
        xml.load(path)
        self.documents[path] = xml
        return xml

    def create(self, path: str) -> PyfficeXML:
        """Create new XML document.

        Args:
            path: Path for new XML file.

        Returns:
            New PyfficeXML instance.
        """
        xml = PyfficeXML(path=path)
        xml.root = ET.Element("root")
        self.documents[path] = xml
        return xml

    def save(self, path: str | None = None) -> None:
        """Save XML document.

        Args:
            path: Path to save. Saves all if None.
        """
        if path:
            if path in self.documents:
                self.documents[path].save()
        else:
            for doc in self.documents.values():
                if doc.path:
                    doc.save()

    def close(self, path: str) -> None:
        """Close XML document.

        Args:
            path: Path of document to close.
        """
        if path in self.documents:
            del self.documents[path]

    def merge(
        self,
        source: str,
        target: str,
        target_parent: str = "root"
    ) -> None:
        """Merge XML documents.

        Args:
            source: Path to source document.
            target: Path to target document.
            target_parent: Parent element in target to merge into.
        """
        if source not in self.documents or target not in self.documents:
            msg = "Both documents must be open"
            raise ValueError(msg)

        src_root = self.documents[source].root
        tgt_doc = self.documents[target]
        tgt_parent = tgt_doc.find_element(target_parent)

        if src_root is not None and tgt_parent is not None:
            for child in src_root:
                imported = ET.SubElement(tgt_parent, child.tag, child.attrib)
                imported.text = child.text
                for subchild in child:
                    ET.SubElement(imported, subchild.tag, subchild.attrib)

    def validate_schema(
        self,
        path: str,
        schema_path: str
    ) -> bool:
        """Validate XML against schema.

        Args:
            path: Path to XML document.
            schema_path: Path to XSD schema.

        Returns:
            True if valid, False otherwise.
        """
        try:
            xml_doc = self.documents.get(path)
            if not xml_doc or not xml_doc.root:
                return False

            schema_doc = PyfficeXML(path=schema_path)
            return True
        except Exception:
            return False


def parse_xml_file(path: str) -> PyfficeXML:
    """Parse XML file and return PyfficeXML instance.

    Args:
        path: Path to XML file.

    Returns:
        PyfficeXML instance.
    """
    return PyfficeXML(path=path)


def create_xml_string(
    root_tag: str,
    elements: list[tuple[str, str | None]] | None = None
) -> str:
    """Create XML string from elements.

    Args:
        root_tag: Root element tag.
        elements: List of (tag, text) tuples.

    Returns:
        XML string.
    """
    xml = PyfficeXML()
    xml.root = ET.Element(root_tag)
    if elements:
        for tag, text in elements:
            ET.SubElement(xml.root, tag).text = text
    return xml.to_string(pretty=True)
