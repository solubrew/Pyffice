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
from condor import condor
from ogma.logma import Logma
from pyffice.tags.tags import PyfficeTag

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeReference(PyfficeTag):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeReference")).override(cfg)
        self.author = None
        self.date = None
        self.doi = None
        self.edition = None
        self.issue = None
        self.media_type = None
        self.page_range = None
        self.publisher = None
        self.style = None

    def load_tag(self, tag):
        """"""
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

    def set_author(self, author):
        """"""
        self.author = author
        return self

    def set_date(self, year, month=None, day=None):
        """"""

    def set_doi(self, doi):
        """"""
        return self

    def set_edition(self, edition):
        """"""
        self.edition = edition
        return self

    def set_issue(self, issue):
        """"""
        self.issue = issue
        return self

    def set_media_type(self, media_type):
        """"""
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
                raise Exception(f"Media Type Unknown {media_type}")

    def set_page_range(self, page_range=None):
        """"""
        self.page_range = page_range
        return self

    def set_publisher(self, publisher):
        """"""
        self.publisher = publisher
        return self

    def set_style(self, style):
        """"""
        self.style = style
        return self

    def set_title(self, title):
        """"""
        self.title = title
        return self

    def set_volume(self, volume):
        """"""
        self.volume = volume
        return self

    def set_url(self, url):
        """"""
        self.url = url
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"]["author"] = self.author
        doc["unit"]["title"] = self.title
        doc["unit"]["volume"] = self.volume
        doc["unit"]["page_range"] = self.page_range
        doc["unit"]["issue"] = self.issue
        doc["unit"]["edition"] = self.edition
        doc["unit"]["publisher"] = self.publisher
        doc["unit"]["style"] = self.style
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
