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
from copy import deepcopy

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||
from collections import deque

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from sympy.sets.sets import set_function

from pyffice.contacts.contacts import PyfficeContact, PyfficeRolodex
from pyffice.document import PyfficeDocument, PyfficeDocumentManager, PyfficeDeque
from pyffice.web.url import PyfficeURL, PyfficeURLLibrary

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "web.yaml")


class PyfficeWebBrowser(PyfficeDocument):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeWebBrowser")).override(cfg)
        self.active_page = None
        self.active_profile = None
        self.active_url = None
        self.library = None
        self.home_url = None
        self.pages = None
        self.profile_manager = None
        self.doc_type = "browser"

    def add_page(self, page):
        """"""
        if isinstance(page, PyfficeWebPage):
            page = page
        else:
            page = PyfficeWebPage(page)
            page.load_document()
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

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_url_home(document.get("home_url", None))
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
        if page is None:
            page = self.pages[0]
        if isinstance(page, dict):
            self.add_page(page)
            page = self.pages[-1]
        if page != self.active_page:
            self.add_change("active_page", self.active_page, page)
            self.active_page = page
            self.active_url = page.active_url
            self.active_profile = page.active_profile
        return self

    def set_pages(self, pages):
        """"""
        if pages is None:
            pages = [{"page": self.home_url.active_url}]  # , "profile": self.active_profile.did}]
        page_objs = []
        for page in pages:
            page = PyfficeWebPage(page)
            page.load_document()
            page_objs.append(page)
        if page_objs != self.pages:
            self.add_change("pages", self.pages, page_objs)
            self.pages = page_objs
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

    def set_url_home(self, url):
        """"""
        home_url = PyfficeURL({"url": url})
        home_url.load_unit()
        if home_url != self.home_url:
            self.add_change("home_url", self.home_url, home_url)
            self.home_url = home_url
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["document"]["profile_manager"] = self.profile_manager.to_dict()
        doc["document"]["library"] = self.library.to_dict()
        doc["document"]["active_url"] = self.active_url.to_dict()
        doc["document"]["home_url"] = self.home_url.to_dict()
        doc["document"]["pages"] = [x.to_dict() for x in self.pages]
        return doc


class PyfficeWebPage(PyfficeDocument):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeWebPage")).override(cfg)
        self.active_url = None
        self.active_profile = None
        self.history = None
        self.snapshots = None
        self.versions = None
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
        snapshot = {"path": None, "hash": hash_, "content_enc64": self.encode64(snapshot)}
        self.add_change("snapshots", self.snapshots, snapshot, "add")
        self.snapshots.append(snapshot)
        return self

    def add_version(self, version):
        """"""
        hash_ = self.get_finger_print(version)
        version = {"path": None, "hash": hash_, "content_enc64": self.encode64(version)}
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
        self.set_snapshots(document.get("snapshots", None))
        self.set_versions(document.get("versions", None))
        self.set_page_pinned(document.get("pinned", None))
        self.set_level_of_trust(document.get("level_of_trust", 0))
        return self

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
        doc["document"] = {
            "pinned_on": self.pinned_on_dttm,
            "last_refresh": self.last_refresh,
            "history": self.history,
            "snapshots": self.snapshots,
            "versions": self.versions,
            "level_of_trust": self.trust,
        }
        doc["document"]["url"] = self.active_url.to_dict()
        return doc


class PyfficeWebProfile(PyfficeContact):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeWebProfile")).override(cfg)

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

    def __init__(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["group"] = "profile"
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeWebProfileManager")).override(cfg)
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
        self.active_profile = self.get_contact(name)
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
        doc["document"]["profiles"] = [x.to_dict() for x in self.profiles]
        if self.active_profile is not None:
            doc["document"]["active_profile"] = self.active_profile.to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
