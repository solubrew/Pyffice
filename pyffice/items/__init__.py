"""Pyffice items module.

This module provides document item abstractions for the Pyffice framework.
"""

from typing import TYPE_CHECKING
from typing_extensions import Self

if TYPE_CHECKING:
    from pyffice.core.document import Document

from kahndor.logma import Logma

logma = Logma(__name__)
logma.off()

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
    
    def __init__(self, item_type: str, properties: dict | None = None) -> None:
        self.item_type = item_type
        logma.debug(f"Item.__init__ called")
        self.properties = properties or {}
        self._parent: "Item | None" = None
    
    @property
    def parent(self) -> "Item | None":
        """Parent.
        
        Returns:
            Self for chaining.
        """
        return self._parent
    
    @parent.setter
    def parent(self, value: "Item | None") -> None:
        """Parent.
        
        Args:
            value: Parameter.
        
        Returns:
            Self for chaining.
        """
        self._parent = value
    
    def to_dict(self) -> dict:
        """Convert item to dictionary representation."""
        return {
            "type": self.item_type,
            "properties": self.properties,
            "parent": self.parent.item_type if self.parent else None
        }
    
    def from_dict(self, data: dict) -> Self:
        """Reconstruct item from dictionary."""
        self.item_type = data.get("type", self.item_type)
        self.properties = data.get("properties", {})
        return self
