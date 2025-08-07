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
from urllib.parse import urlparse, urljoin, urlencode

# ======================================3rd Party Library Modules=====================================================||
import furl

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from twof.twofdns import TwoFDNS
from subtrix.subtrix import uuid
from pyffice.document import PyfficeUnit, PyfficeDocumentManager
from pycurity.pyhash import text_hashing_function

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "url.yaml")


class PyfficeURL(PyfficeUnit):
    """"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeURL").override(cfg))
        self.active_url = None
        self.block_ads = None
        self.block_adult = None
        self.default_url = None
        self.domain = None
        self.filters = None
        self.found_url = None
        self.fragment = None
        self.geofence_active = None
        self.geofence_region = None
        self.given_url = None
        self.hostname = None
        self.level_of_trust = None
        self.link_style = None
        self.netloc = None
        self.path = None
        self.parameters = None
        self.parsed = None
        self.query = None
        self.password = None
        self.port = None
        self.redirect_affiliates = None
        self.scheme = None
        self.sub_domain = None
        self.twofdns = None
        self.username = None
        self.whois = None
        if self.active_url is not None:
            self._parse(self.active_url)
        self.doc_type = "url"

    def build_url(self):
        """"""

    def check_pattern(self, pattern):
        """"""
        if pattern in self.given_url:
            return True
        if pattern in self.active_url:
            return True
        if pattern in self.found_url:
            return True
        return False

    def filter(self, url):
        """"""
        for filter_ in self.filters:
            if filter_ in url:
                return url
        return False

    def get_domain_and_subdomain(self, netloc):
        """"""
        if ":" in netloc:  # Remove port number if present in netloc
            netloc = netloc.split(":")[0]
        # Split the hostname into parts
        parts = netloc.split(".")
        if len(parts) >= 3:  # Check if there is a subdomain
            subdomain = ".".join(parts[:-2])
            domain = ".".join(parts[-2:])
        elif len(parts) == 2:  # No subdomain, just domain
            subdomain = None
            domain = netloc
        else:  # Malformed netloc
            subdomain = None
            domain = None
        return domain, subdomain

    def get_parameters(self):
        """"""
        if not self.parsed:
            self._parse(self.active_url)
        return self.parameters

    def get_domain(self):
        """"""
        if not self.parsed:
            self._parse(self.active_url)
        return self.domain

    def get_sub_domain(self):
        """"""
        if not self.parsed:
            self._parse(self.active_url)
        return self.sub_domain

    def get_url(self):
        """"""
        url = f"{self.scheme}{self.netloc}{self.path}{self.params}{self.query}{self.fragment}"
        if self.block_ads:
            self.check_pattern(self.block_patterns)
        if self.redirect_affiliates:
            self.check_pattern(self.affiliate_patterns)
        return self.found_url

    def initialize_ad_blocking(self):
        """"""
        self.block_ads = True
        return self

    def is_changed(self):
        """"""
        return self.found_url != self.given_url

    def is_valid(self):
        """"""
        if self.active_url is not None:
            if self.get_domain():
                return True
        return False

    def load_unit(self, unit=None):
        """"""
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        logma.info(f"Unit {unit}")
        super().load_unit(unit)
        self.set_given_url(unit.get("original_path", unit.get("url", self.default_url)))
        self.set_active_url(self.given_url)
        active_url = unit.get("active_url", unit.get("url", None))
        if active_url is not None:
            self.set_active_url(active_url)
        self.set_block_ads(unit.get("block_ads", False))
        self.set_block_adult(unit.get("block_adult", True))
        self.set_default_url(unit.get("default_url", "https://www.duckduckgo.com/search?q="))
        self.set_domain(unit.get("domain", ""))
        self.set_filters(unit.get("filters", []))
        self.set_fragment(unit.get("fragment", ""))
        self.set_geofence(unit.get("geofence_region", None), unit.get("geofence_active", False))
        self.set_hostname(unit.get("hostname", ""))
        self.set_level_of_trust(unit.get("level_of_trust", 0))
        self.set_link_style(unit.get("link_style", "path"))
        self.set_netloc(unit.get("netloc", ""))
        self.set_path(unit.get("path", ""))
        self.set_parameters(unit.get("parameters", ""))
        self.set_query(unit.get("query", ""))
        self.set_password(unit.get("password", ""))
        self.set_port(unit.get("port", ""))
        self.set_redirect_affiliates(unit.get("redirect_affiliates", True))
        self.set_scheme(unit.get("scheme", ""))
        self.set_sub_domain(unit.get("sub_domain", ""))
        self.set_twofdns(unit.get("twofdns", False))
        self.set_username(unit.get("username", ""))
        self._parse(self.active_url if self.active_url else self.config.dikt.get("url", self.default_url))
        return self

    def sanitize_url(self):
        """"""
        if "https" != self.found_url[:4]:
            self.found_url = f"https://{self.found_url}"
        self.found_url = self.filter(self.found_url)
        return self

    def set_active_url(self, url=None):
        """"""
        if url is None:
            url = self.default_url
        if url != self.active_url:
            self.add_change("active_url", self.active_url, url)
            self.active_url = url
            if not "127.0.0.1" in self.active_url or "chrome://version" in self.active_url:  # TODO complete local host
                self.set_secure()
        logma.info(f"Active Url {self.active_url}")
        return self

    def set_block_ads(self, block_ads):
        """"""
        if block_ads != self.block_ads:
            self.add_change("block_ads", self.block_ads, block_ads)
            self.block_ads = block_ads
        return self

    def set_block_adult(self, block_adult):
        """"""
        if block_adult != self.block_adult:
            self.add_change("block_adult", self.block_adult, block_adult)
            self.block_adult = block_adult
        return self

    def set_default_url(self, url):
        """"""
        if url != self.default_url:
            self.add_change("default_url", self.default_url, url)
            self.default_url = url
        return self

    def set_domain(self, domain):
        """"""
        if domain != self.domain:
            self.add_change("domain", self.domain, domain)
            self.domain = domain
        return self

    def set_filters(self, filters):
        """"""
        if filters != self.filters:
            self.add_change("filters", self.filters, filters)
            self.filters = filters
        return self

    def set_fragment(self, fragment):
        """"""
        if fragment != self.fragment:
            self.add_change("fragment", self.fragment, fragment)
            self.fragment = fragment
        return self

    def set_geofence(self, region, active=True):
        """"""
        self.geofence_active = active
        self.geofence_region = region
        return self

    def set_given_url(self, url=None):
        """"""
        # logma.inspect_caller()
        if url != self.given_url:
            self.add_change("given_url", self.given_url, url)
            self.given_url = url
        logma.info(f"Given URL {self.given_url}")
        return self

    def set_hostname(self, hostname):
        """"""
        if hostname != self.hostname:
            self.add_change("hostname", self.hostname, hostname)
            self.hostname = hostname
        return self

    def set_level_of_trust(self, level_of_trust):
        """"""
        if level_of_trust != self.level_of_trust:
            self.add_change("level_of_trust", self.level_of_trust, level_of_trust)
            self.level_of_trust = level_of_trust
        return self

    def set_link_style(self, link_style):
        """"""
        if link_style != self.link_style:
            self.add_change("link_style", self.link_style, link_style)
            self.link_style = link_style
        return self

    def set_netloc(self, netloc):
        """"""
        if netloc != self.netloc:
            self.add_change("netloc", self.netloc, netloc)
            self.netloc = netloc
        return self

    def set_path(self, path):
        """"""
        if path != self.path:
            self.add_change("path", self.path, path)
            self.path = path
        return self

    def set_parameters(self, parameters):
        """"""
        if parameters != self.parameters:
            self.add_change("parameters", self.parameters, parameters)
            self.parameters = parameters
        return self

    def set_parsed(self, parsed):
        """"""
        if parsed != self.parsed:
            self.add_change("parsed", self.parsed, parsed)
            self.parsed = parsed
        return self

    def set_query(self, query):
        """"""
        if query != self.query:
            self.add_change("query", self.query, query)
            self.query = query
        return self

    def set_password(self, password):
        """"""
        if password is None:
            password = ""
        password = text_hashing_function(password)
        if password != self.password:
            self.add_change("password", self.password, password)
            self.password = password
        return self

    def set_port(self, port):
        """"""
        if port != self.port:
            self.add_change("port", self.port, port)
            self.port = port
        return self

    def set_redirect_affiliates(self, redirect_affiliates):
        """"""
        if redirect_affiliates != self.redirect_affiliates:
            self.add_change("redirect_affiliates", self.redirect_affiliates, redirect_affiliates)
            self.redirect_affiliates = redirect_affiliates
        return self

    def set_secure(self):
        """"""
        logma.info(f"Active Url {self.active_url}")
        if self.active_url[:7] == "http://":
            self.secure_url = self.active_url.replace("http://", "https://")
        elif self.active_url[:8] == "https://":
            self.secure_url = self.active_url
        else:
            self.secure_url = f"https://{self.active_url}"
        self.active_url = self.secure_url
        return self

    def set_scheme(self, scheme):
        """"""
        if scheme != self.scheme:
            self.add_change("scheme", self.scheme, scheme)
            self.scheme = scheme
        return self

    def set_sub_domain(self, sub_domain):
        """"""
        if sub_domain != self.sub_domain:
            self.add_change("sub_domain", self.sub_domain, sub_domain)
            self.sub_domain = sub_domain
        return self

    def set_twofdns(self, twofdns):
        """"""
        if twofdns != self.twofdns:
            self.add_change("twofdns", self.twofdns, twofdns)
            self.twofdns = twofdns
        return self

    def set_username(self, username):
        """"""
        if username != self.username:
            self.add_change("username", self.username, username)
            self.username = username
        return self

    def set_whois(self, whois):
        """"""
        self.whois = whois
        return self

    def remove_www(self):
        """"""
        if "www." == self.active_url[:4]:
            self.no_www = self.active_url[4:]
        if "http://www." == self.active_url[:11]:
            self.no_www = f"http://{self.active_url[11:]}"
        if "https://www." == self.active_url[:12]:
            self.no_www = f"https://{self.active_url[12:]}"
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["unit"] = {
            "original_path": self.given_url,
            "active_url": self.active_url,
            "trust_level": self.level_of_trust,
            "qualified_path": self.found_url,
            "domain": self.domain,
            "redirect_path": self.redirect_affiliates,
        }
        return doc

    def validate(self):
        """Ensure that url is validdly construccted"""

    def verify(self):
        """attempt to ensure web address is correct
        this will be the first stemp towards TwoFDNS integration
        who provides data from the blockchain for TwoFDNS?
        """
        if self.library.verify(self.active_url):
            return True
        return False

    def verify_full_address(self, url):
        """
        :return:
        """

        return url

    def _parse(self, url):
        """"""
        try:
            parsed = urlparse(url)
        except Exception as e:
            return self
        # logma.info(f"Netloc {parsed.netloc}")
        self.set_netloc(parsed.netloc)
        try:
            domain, sub = self.get_domain_and_subdomain(self.netloc)
        except Exception as e:
            return self
        try:
            self.set_domain(domain)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_sub_domain(sub)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_scheme(parsed.scheme)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_hostname(parsed.hostname)
        except Exception as e:
            logma.warning(e)
        # try:
        #     self.set_given_url(url)
        # except Exception as e:
        #     logma.warning(e)
        try:
            self.set_port(parsed.port)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_path(parsed.path)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_query(parsed.query)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_parameters(parsed.params)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_fragment(parsed.fragment)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_username(parsed.username)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_password(parsed.password)
        except Exception as e:
            logma.warning(e)
        try:
            self.set_parsed(True)
        except Exception as e:
            logma.warning(e)
        # furled = furl.furl(url) TODO not sure if this is needed urlparse may handle it all
        return self


class PyfficeURLLibrary(PyfficeDocumentManager):
    """URL Library is a data object for integrating affilate links into the web apps and browsing features provided
    within Pyffice"""

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(condor.Instruct(pxcfg).select("PyfficeURLLibrary").override(cfg))
        self.urls = None
        self.affiliate_patterns = None
        self.block_patterns = None

    def add_url(self, url):
        """"""
        self.add_document(PyfficeURL(url))
        return self

    def find_affiliate_link(self, link=None, urllib=None):
        """"""
        self.given_link = link
        self.found_data = urllib.search(link)
        self.found_link = self.found_data[self.link_style]
        self.sanitize_link()
        return self

    def find_webapp_link(self, link=None, urllib=None):
        """"""
        if link is None:
            link = self.given_link
        self.found_data = urllib.search(link)
        self.found_link = self.found_data[self.link_style]
        self.sanitize_link()
        return self

    def get_affiliate_patterns(self):
        """
        get affiliate urls from pyffice sercies and store locally
        :return:
        """

    def get_block_patterns(self):
        """"""
        return self

    def get_domain(self):
        """"""
        return self

    def get_region_patterns(self, region):
        """"""

    def get_malware_ad_patterns(self):
        """"""
        for service in self.services:
            if service.get("key", False):
                self.given_malware += get_data(service)

    def get_url_by_id(self, url_id):
        """"""
        url = self.known_urls[url_id].found_url
        return url

    def get_urls(self):
        """"""
        table = "urls"
        cfg = {"table": table}
        params = {table: {"WHERE": {"EQUAL": {"substitute_bit": 1}}}}
        reader = self.app.model.store.docs["db"].read(cfg, params)
        self.urls = next(reader).dikt[table]["df"]

    def load_document(self, document=None):
        """"""
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        self.set_urls(document.get("urls", {}))
        return self

    def lookup(self, code):
        """"""
        if self.known_urls is None:
            self.known_urls = self.app.model.store["db"].get_urls()
        url = self.known_urls.get(code, None)
        if url is not None:
            self.url = url
        return self

    def search(self, url):
        """"""
        if self.urls is None:
            self.get_urls()
        logma.info(f"URLs {self.urls}")
        url_data = self.urls[self.urls["code_txt"] == url]
        logma.info(f"URL Data {url_data}")
        if not url_data.empty:
            url_row = url_data.iloc[0]
            return url_row

    def set_affiliate_patterns(self, patterns):
        """"""
        if patterns != self.affiliate_patterns:
            self.add_change("affiliate_patterns", self.affiliate_patterns, patterns)
            self.affiliate_patterns = patterns
        return self

    def set_block_patterns(self, patterns):
        """"""
        if patterns != self.block_patterns:
            self.add_change("block_patterns", self.block_patterns, patterns)
            self.block_patterns = patterns
        return self

    def set_urls(self, urls):
        """"""
        if urls != self.urls:
            self.add_change("urls", self.urls, urls)
            self.urls = urls
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc

    def update_from_service(self, service_name):
        """"""
        stone = self.get_stone(service_name)
        data = stone.get_urls(cfg)

    def verify(self, url):
        """"""
        if url not in self.block_patterns:
            if TwoFDNS(self.url):
                return True
        return False


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
