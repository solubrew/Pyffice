"""Pyffice media module.

Provides media processing capabilities for documents.
"""

from typing import Any
from dataclasses import dataclass
from enum import Enum

from kahndor.logma import Logma

logma = Logma(__name__)
logma.off()

__all__ = ["Media", "MediaType", "MediaProcessor", "MediaError"]


class MediaType(Enum):
    """Supported media types."""
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    EMBEDDED = "embedded"


class MediaError(Exception):
    """Media processing error."""
    pass


@dataclass
class Media:
    """Represents a media asset."""
    media_type: MediaType
    source: str
    data: bytes | None = None
    metadata: dict | None = None
    
    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def is_loaded(self) -> bool:
        """Check if media data is loaded."""
        return self.data is not None
    
    def load(self) -> bytes:
        """Load media data from source."""
        if self.data is not None:
            return self.data
        if self.source.startswith(("http://", "https://")):
            import urllib.request
            with urllib.request.urlopen(self.source) as response:
                self.data = response.read()
        else:
            with open(self.source, "rb") as f:
                self.data = f.read()
        return self.data
    
    def unload(self) -> None:
        """Unload media data to free memory."""
        self.data = None


class MediaProcessor:
    """Processes media assets for documents."""
    
    def __init__(self) -> None:
        self._handlers: dict[MediaType, callable] = {}
        logma.debug(f"MediaProcessor.__init__ called")
    
    def register_handler(self, media_type: MediaType, handler: callable) -> None:
        """Register a handler for a media type."""
        self._handlers[media_type] = handler
    
    def process(self, media: Media, **options: Any) -> Any:
        """Process a media asset."""
        handler = self._handlers.get(media.media_type)
        if handler is None:
            raise MediaError(f"No handler for media type: {media.media_type}")
        return handler(media, **options)
    
    def extract_audio(self, media: Media) -> bytes:
        """Extract audio from media."""
        if media.media_type == MediaType.AUDIO:
            return media.load()
        raise MediaError(f"Cannot extract audio from {media.media_type}")
    
    def extract_thumbnail(self, media: Media, size: tuple[int, int] = (128, 128)) -> bytes:
        """Extract thumbnail from media."""
        if media.media_type == MediaType.IMAGE:
            return media.load()
        raise MediaError(f"Cannot extract thumbnail from {media.media_type}")
