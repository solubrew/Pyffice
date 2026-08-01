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
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.tags.tags import PyfficeTag
from typing_extensions import Self


# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeReference(PyfficeTag):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficeReference.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeReference")).override(cfg)
        self.author = None
        self.date = None
        self.doi = None
        self.edition = None
        self.issue = None
        self.media_type = None
        self.page_range = None
        self.publisher = None
        self.style = None

    def load_tag(self, tag) -> Self:
        """Load tag into this document.
        
        Args:
            tag: Parameter.
        
        Returns:
            Self for chaining.
        """
        if tag is None:
            tag = self.config.dikt.get("tag", {})
        super().load_tag(tag)
        self.set_label("reference")
        self.set_description("Bibliography Reference")
        self.set_author(tag.get("author", []))
        self.set_date(*tag.get("date", []))
        self.set_media_type(tag.get("media_type", None))
        self.set_publisher(tag.get("publisher", None))
        self.set_style(tag.get("style", None))
        self.set_title(tag.get("title", None))
        self.set_volume(tag.get("volume", None))
        self.set_page_range(tag.get("page_range", None))
        self.set_issue(tag.get("issue", None))
        self.set_edition(tag.get("edition", None))
        return self

    def set_author(self, author) -> Self:
        """Set the document author.
        
        Args:
            author: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.author = author
        return self

    def set_date(self, year, month=None, day=None) -> Self:
        """Set publication date."""
        self.date = (year, month, day)
        return self

    def set_doi(self, doi) -> Self:
        """Set DOI."""
        self.doi = doi
        return self

    def set_edition(self, edition) -> Self:
        """Set the edition.
        
        Args:
            edition: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.edition = edition
        return self

    def set_issue(self, issue) -> Self:
        """Set the issue.
        
        Args:
            issue: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.issue = issue
        return self

    def set_media_type(self, media_type) -> None:
        """Set the media type.
        
        Args:
            media_type: Parameter.
        
        Returns:
            Self for chaining.
        """
        from pyffice.pyffice import UnknownMediaTypeError
        match media_type:
            case "book":
                pass
            case "journal":
                pass
            case "newspaper":
                pass
            case "podcast":
                pass
            case "website":
                pass
            case "video":
                pass
            case "audio":
                pass
            case _:
                raise UnknownMediaTypeError(f"Media Type Unknown {media_type}")

    def set_page_range(self, page_range=None) -> Self:
        """Set the page range.
        
        Args:
            page_range: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.page_range = page_range
        return self

    def set_publisher(self, publisher) -> Self:
        """Set the publisher.
        
        Args:
            publisher: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.publisher = publisher
        return self

    def set_style(self, style) -> Self:
        """Set the style.
        
        Args:
            style: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.style = style
        return self

    def set_title(self, title) -> Self:
        """Set the title.
        
        Args:
            title: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.title = title
        return self

    def set_volume(self, volume) -> Self:
        """Set the volume.
        
        Args:
            volume: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.volume = volume
        return self

    def set_url(self, url) -> Self:
        """Set the url.
        
        Args:
            url: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.url = url
        return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
