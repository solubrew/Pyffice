"""Pyffice items module.

This module provides document item abstractions for the Pyffice framework.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyffice.core.document import Document

__all__ = ["Item", "ItemType", "Document"]


class ItemType:
    """Enumeration of supported item types."""
    CELL = "cell"
    SHAPE = "shape"
    SLIDE = "slide"
    SHEET = "sheet"
    PARAGRAPH = "paragraph"
    CHART = "chart"
    TABLE = "table"
    IMAGE = "image"
    MEDIA = "media"
    ANNOTATION = "annotation"


class Item:
    """Base class for all document items."""
    
    def __init__(self, item_type: str, properties: dict | None = None):
        self.item_type = item_type
        self.properties = properties or {}
        self._parent: "Item | None" = None
    
    @property
    def parent(self) -> "Item | None":
        return self._parent
    
    @parent.setter
    def parent(self, value: "Item | None"):
        self._parent = value
    
    def to_dict(self) -> dict:
        """Convert item to dictionary representation."""
        return {
            "type": self.item_type,
            "properties": self.properties,
            "parent": self.parent.item_type if self.parent else None
        }
    
    def from_dict(self, data: dict) -> "Item":
        """Reconstruct item from dictionary."""
        self.item_type = data.get("type", self.item_type)
        self.properties = data.get("properties", {})
        return self
