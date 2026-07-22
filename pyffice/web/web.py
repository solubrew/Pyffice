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
from copy import deepcopy
import json as j

# ======================================3rd Party Library Modules=====================================================||
from collections import deque

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.contacts.contacts import PyfficeContact, PyfficeRolodex
from pyffice.document import PyfficeDocument, PyfficeDocumentManager, PyfficeDeque
from pyffice.web.url import PyfficeURL, PyfficeURLLibrary
from pycurity.pyhash import text_hashing_function, encode64, decode64

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = False
logma = Logma(__name__)
if not log:
    logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "web.yaml")


class PyfficeWebBrowser(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeWebBrowser")).override(cfg)
        self.document = self.config.select("template").override(self.config.select("document").dikt)
        self.active_page = None
        self.active_profile = None
        self.home_page = None
        self.library = None
        # self.page = None
        self.pages = None
        self.profile_manager = None
        self.doc_type = "browser"

    def add_page(self, page):
        """"""
        if isinstance(page, PyfficeWebPage):
            page = page
        else:
            page = PyfficeWebPage({"page": page})
            page.load_document()
        if self.pages is None:
            self.pages = []
        self.pages.append(page)
        return self

    def add_profile(self, profile):
        """"""
        if isinstance(profile, PyfficeWebProfile):
            profile = profile
        else:
            profile = PyfficeWebProfile(profile)
            profile.load_document()
        logma.info(f"Profile: {profile}")
        self.profile_manager.add_profile(profile)
        return self

    def del_page(self):
        """"""
        return self

    def del_profile(self, name):
        """"""
        return self

    def get_active_profile(self):
        """"""
        return self.profile_manager.active_profile

    def get_active_page(self):
        """"""
        return self.pages.get_active_page()

    def is_pinned(self):
        """"""
        return self.active_page.is_pinned()

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if isinstance(document, str):
            document = j.loads(document)
        document = self.document.override(document).dikt
        logma.info(f"Load Document {document}")
        super().load_document(document)
        # self.set_url_home(document.get("home_url", None))
        self.set_page_home(document.get("home_url", None))
        # url = document.get("data", {}).get("unit", {}).get("original_path", self.home_page.active_url)
        # logma.info(f"Active {url}")
        # self.set_url_active(url)
        logma.info(f"URL Home")
        self.set_library(document.get("library", None))
        self.set_profile_manager(document.get("profile_manager", None))
        self.set_profile_active(document.get("active_profile", None))
        self.set_pages(document.get("pages", None))
        self.set_page_active(document.get("active_page", None))
        return self

    def set_library(self, library):
        """"""
        cfg = {"library": library}
        library = PyfficeURLLibrary(cfg)
        library.load_document()
        if library != self.library:
            self.add_change("library", self.library, library)
            self.library = library
        return self

    def set_page_active(self, page):
        """"""
        if isinstance(page, str):
            url = PyfficeURL(page)
            url.load_unit()
            page = {"active_url": url, "home_url": self.home_page.active_url}
        if page is None:
            page = self.pages[0]
        if isinstance(page, dict):
            page = PyfficeWebPage(page)
            page.load_document()
            if page != self.active_page:
                self.add_change("active_page", self.active_page, page)
                self.active_page = page
        elif isinstance(page, PyfficeWebPage):
            if page != self.active_page:
                self.add_change("active_page", self.active_page, page)
                self.active_page = page
        else:
            raise ValueError(f"page: {page}")
        return self

    def set_page_home(self, page):
        """"""
        if not isinstance(page, PyfficeWebPage):
            page = PyfficeWebPage(page)
            page.load_document()
        if page != self.home_page:
            self.add_change("home_page", self.home_page, page)
            self.home_page = page
        return self

    def set_pages(self, pages):
        """"""
        if pages is None:
            pages = [{"page": self.home_page}]  # , "profile": self.active_profile.did}]
        page_objs = []
        for page in pages:
            page = PyfficeWebPage(page)
            page.load_document()
            page_objs.append(page)
        if page_objs != self.pages:
            self.add_change("pages", self.pages, page_objs)
            self.pages = page_objs
        return self

    def set_pinned(self, pin):
        """"""
        self.pinned = pin
        return self

    def set_profile_active(self, profile):
        """"""
        cfg = {"profile": profile}
        profile = PyfficeWebProfile(cfg)
        profile.load_document()
        if self.active_page is None:
            if len(self.profile_manager.profiles) == 0:
                self.add_profile(profile)
            profile = self.profile_manager.profiles[0]
        if profile != self.active_profile:
            self.add_change("active_profile", self.active_profile, profile)
            self.active_profile = profile
        return self

    def set_profile_manager(self, profiles):
        """"""
        cfg = {"profiles": profiles}
        profile_manager = PyfficeWebProfileManager(cfg)
        profile_manager.load_document()
        logma.info(f"profile_manager: {profile_manager}")
        if profile_manager != self.profile_manager:
            logma.info(f"profile_manager: {profile_manager}")
            self.add_change("profile_manager", self.profile_manager, profile_manager)
            self.profile_manager = profile_manager
        return self

    def set_refresh_time(self):
        """"""
        self.update_document_time()
        return self

    # def set_url_active(self, url):
    #     """"""
    #     logma.info(f"set_url_active: {url}")
    #     active_url = PyfficeURL({"unit": {"original_path": url, "given_url": url}})
    #     active_url.load_unit()
    #     logma.info(f"set_url_active: {active_url.to_dict()}")
    #     if active_url != self.active_url:
    #         self.add_change("active_url", self.active_url, active_url)
    #         self.active_url = active_url
    #     logma.info(f"set_url_active: {self.active_url.to_dict()}")
    #     return self
    #
    # def set_url_home(self, url):
    #     """"""
    #     home_url = PyfficeURL({"unit": {"original_path": url, "given_url": url}})
    #     home_url.load_unit()
    #     if home_url != self.home_url:
    #         self.add_change("home_url", self.home_url, home_url)
    #         self.home_url = home_url
    #     return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["data"]["profile_manager"] = self.profile_manager.to_dict()
        doc["data"]["library"] = self.library.to_dict()
        # doc["data"]["unit"] = self.active_url.to_dict()["unit"]
        # doc["data"]["home_page"] = self.home_page.to_dict()
        if self.active_profile is not None:
            doc["data"]["active_profile"] = self.active_profile.to_dict()
        doc["data"]["page"] = self.active_page.to_dict()
        # doc["data"]["pages"] = [x.to_dict() for x in self.pages]
        return doc


class PyfficeWebPage(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeWebPage")).override(cfg)
        self.active_url = None
        self.active_profile = None
        self.history = None
        self.snapshots = None
        self.versions = None
        self.is_pinned = None
        self.pinned_on_dttm = None
        self.last_refresh = None
        self.trust = None

    def add_history(self, url):
        """"""
        self.add_change("history", deepcopy(self.history), url, "add")
        self.history.append(url)
        return self

    def add_snapshot(self, snapshot):
        """"""
        hash_ = self.get_finger_print(snapshot)
        snapshot = {"path": None, "hash": hash_, "content_enc64": encode64(snapshot)}
        self.add_change("snapshots", self.snapshots, snapshot, "add")
        self.snapshots.append(snapshot)
        return self

    def add_version(self, content):
        """"""
        hash_ = self.get_finger_print(content)
        version = {"path": None, "hash": hash_, "content_enc64": encode64(content)}
        self.add_change("versions", deepcopy(self.versions), version, "add")
        self.versions.append(version)
        return self

    def load_document(self, document=None):
        """"""
        if document is None:
            document = {}
        super().load_document(document)
        self.set_history(document.get("history", None), document.get("max_items", 10))
        self.set_url(document.get("url", None))
        self.set_snapshots(document.get("snapshots", []))
        self.set_versions(document.get("versions", []))
        self.set_page_pinned(document.get("pinned", None))
        self.set_level_of_trust(document.get("level_of_trust", 0))
        return self

    def get_finger_print(self, content):
        """"""
        return text_hashing_function(content)

    def set_history(self, history, max_items):
        """"""
        cfg = {"max_items": max_items, "history": history}
        history = PyfficeDeque(cfg)
        if history != self.history:
            self.add_change("history", deepcopy(self.history), deepcopy(history))
            self.history = history
        return self

    def set_page_pinned(self, pinned=None):
        """"""
        if pinned is None:
            pinned_on_dttm = dt.datetime.now().isoformat()
        else:
            pinned_on_dttm = pinned["pinned_on_dttm"]
        if pinned_on_dttm != self.pinned_on_dttm:
            self.add_change("pinned_on", self.pinned_on_dttm, pinned_on_dttm)
            self.pinned_on_dttm = pinned_on_dttm
        return self

    def set_page_unpinned(self):
        """"""
        pinned_on_dttm = None
        if pinned_on_dttm != self.pinned_on_dttm:
            self.add_change("pinned_on", self.pinned_on_dttm, pinned_on_dttm)
            self.pinned_on_dttm = pinned_on_dttm
        return self

    # def set_profile_active(self, profile):
    #     """"""
    #     # if profile is None:
    #     #     cfg = {"profile": profile}
    #     #     profile = PyfficeWebProfile(cfg)
    #     if profile != self.active_profile:
    #         self.add_change("active_profile", self.active_profile, profile)
    #         self.active_profile = profile
    #     return self

    def set_refresh_time(self):
        """"""
        self.last_refresh = dt.datetime.now().isoformat()
        return self

    def set_level_of_trust(self, level):
        """"""
        if level > 32:
            level = 0
        elif level < 0:
            level = 0
        if level != self.trust:
            self.add_change("level_of_trust", self.trust, level)
            self.trust = level
        return self

    def set_snapshots(self, snapshots):
        """"""
        if snapshots != self.snapshots:
            self.add_change("snapshots", deepcopy(self.snapshots), deepcopy(snapshots))
            self.snapshots = snapshots
        return self

    def set_url(self, url):
        """"""
        if self.pinned_on_dttm is None:
            active_url = PyfficeURL(url)
            if active_url != self.active_url:
                self.add_history(self.active_url)
                self.add_change("url", self.active_url, active_url)
                self.active_url = active_url
        return self

    def set_versions(self, versions):
        """"""
        if versions != self.versions:
            self.add_change("versions", deepcopy(self.versions), deepcopy(versions))
            self.versions = versions
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["data"] = {
            "pinned_on": self.pinned_on_dttm,
            "last_refresh": self.last_refresh,
            "history": self.history.to_dict(),
            "snapshots": self.snapshots,
            "versions": self.versions,
            "level_of_trust": self.trust,
        }
        doc["data"]["url"] = self.active_url.to_dict()

        # doc["data"]["profile"] = self.active_profile.to_dict()
        doc["data"]["source"] = None
        return doc


class PyfficeWebProfile(PyfficeContact):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeWebProfile")).override(cfg)

    def load_document(self, document=None):
        """"""
        if document is None:
            document = {}
        super().load_document(document)
        self.add_group("profile")
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeWebProfileManager(PyfficeRolodex):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["group"] = "profile"
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeWebProfileManager")).override(cfg)
        self.active_profile = None
        self.profiles = None

    def add_profile(self, profile):
        """"""
        if profile is None:
            cfg = {}
            profile = PyfficeWebProfile(cfg)
        self.add_change("profiles", deepcopy(self.profiles), deepcopy(profile))
        self.profiles.append(profile)
        self.add_contact(profile, "profile")
        return self

    def add_profiles(self, profiles):
        """"""
        for profile in profiles:
            self.add_profile(profile)
        return self

    def del_profile(self, name):
        """"""
        self.del_contact(name)
        return self

    def get_count(self):
        """"""
        return len(self.profiles)

    def get_profile(self, name):
        """"""
        return self.get_contact(name)

    def get_current_profile(self):
        """"""
        return self.active_profile

    def load_document(self, document=None):
        """"""
        if document is None:
            document = {}
        super().load_document(document)
        self.set_profiles(document.get("profiles", None))
        self.set_profile_active(document.get("active_profile", None))
        return self

    def set_profile_active(self, profile):
        """"""
        if profile is None:
            return self
        profile = self.profiles[profile.did]
        if profile != self.active_profile:
            self.add_change("active_profile", self.active_profile, profile)
            self.active_profile = profile
        return self

    def set_profiles(self, profiles):
        """"""
        if profiles is None:
            profiles = []
        if profiles != self.profiles:
            self.add_change("profiles", self.profiles, profiles)
            self.profiles = profiles
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["data"]["profiles"] = [x.to_dict() for x in self.profiles]
        if self.active_profile is not None:
            doc["data"]["active_profile"] = self.active_profile.to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
