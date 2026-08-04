#!/usr/bin/env python3
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
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
import xml.etree.ElementTree as ET
from typing_extensions import Self

# ======================================3rd Party Library Modules=====================================================||


# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pycurity.pymatch import extract_urls
from pyffice.images.images import PyfficeImage
from pyffice.items.items import PyfficeTable
from pyffice.ports.ports import PyfficePort
from pyffice.script.script import PyfficeScript
from pyffice.web.web import PyfficeWebBrowser

# ====================================================================================================================||
HERE = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
PXCFG = join(HERE, "../config/_data_", ".yaml")
pxcfg = PXCFG


class PyfficePortCherryTree(PyfficePort):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """"""
        logma.info(f"Init Cherry Tree {cfg}")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficePortCherryTree")).override(cfg)
        logma.info(f"Init Cherry Tree {self.config.dikt}")
        self.nodes = None
        self.root = None
        self.tree = None
        self.codeboxes = None
        self.links = None
        self.tables = None
        self.images = None

    def extract_codeboxes(self, node) -> Self:
        """Extract codeboxes.

        Args:
            node: Parameter.

        Returns:
            Self for chaining.
        """
        codeboxes = node.findall("codebox")
        self.codeboxes = []
        for code in codeboxes:
            cfg = {"document": {"content": code.text, "syntax": code.attrib.get("prog_lang", "")}}
            box = PyfficeScript(cfg)
            box.load_document()
            self.codeboxes.append(box)
        return self

    def extract_images(self, node) -> Self:
        """Extract images.

        Args:
            node: Parameter.

        Returns:
            Self for chaining.
        """
        images = node.findall("encoded_png")
        self.images = []
        for image in images:
            if image.attrib.get("filename", "") == "__ct_special.tex":
                continue
            logma.info(f"Image {image.text}")
            cfg = {
                "data": {
                    "content": {"L0": {"bytes": image.text}},
                },
                "location": "internal",
            }
            image_ = PyfficeImage({"document": cfg})
            image_.load_document()
            self.images.append(image_)
        return self

    def extract_tables(self, node) -> Any:
        """Extract tables.

        Args:
            node: Parameter.

        Returns:
            Self for chaining.
        """
        tables = node.findall("table")
        tables_ = []
        for table in tables:
            rows = table.findall("row")
            rows_ = []
            for i, row in enumerate(rows):
                cells = row.findall("cell")
                row_ = []
                for j, cell in enumerate(cells):
                    row_.append(cell.text)
                    # if i == 0:
                    #     tables_[j] = cell.text if j < len(tables_) else cell.text + "|"
                    # else:
                    #     tables_[j] = tables_[j] + "\n" + cell.text + "|"
                rows_.append(row_)
            cfg = {"rows": rows}
            table_ = PyfficeTable(cfg)
            table_.load_unit()
            tables_.append(table_)
        return tables_

    def extract_text(self, node) -> Any:
        """Extract text.

        Args:
            node: Parameter.

        Returns:
            Self for chaining.
        """
        full_text = ""
        script = None
        if node.text is not None:
            full_text = self.parse_text(node)
            logma.info(f"Full Text {full_text}")
            script = PyfficeScript({})
            script.load_document()
            script.parse_content(full_text)
        logma.info(f"Full Text {full_text}")
        return script

    def file_import(self, file_path=None) -> Self:
        """File import.

        Args:
            file_path: Parameter.

        Returns:
            Self for chaining.
        """
        self.file_open(file_path)
        return self.to_dict()

    def file_open(self, file_path) -> Self:
        """File open.

        Args:
            file_path: Parameter.

        Returns:
            Self for chaining.
        """
        # logma.info(f"Open Cherry Tree {self.config.dikt["file_path"]}")
        self.load_document(self.config.dikt.get("document", {}))
        if file_path is None:
            file_path = self.file_path
        logma.info(f"Open Cherry Tree {self.file_path}")
        xml_string = super().file_open(file_path)
        self.tree = ET.ElementTree(ET.fromstring(xml_string))
        self.root = self.tree.getroot()
        self.parse()
        return self

    def load_document(self, document=None) -> Self:
        """Load document into this document.

        Args:
            document: Parameter.

        Returns:
            Self for chaining.
        """
        logma.info(f"Load Cherry Tree {document}")
        super().load_document(document)
        return self

    def parse(self) -> Self:
        """
        Parse the entire XML structure starting from the root.

        :return: A list of parsed nodes.
        """
        self.nodes = [self.parse_node(node) for node in self.root.findall("node")]
        return self

    def parse_links(self, text) -> Self:
        # extract urls
        """Parse URL links from the document content.

        Args:
            text: Parameter.

        Returns:
            Self for chaining.
        """
        links = extract_urls(text)
        logma.info(f"Links: {links}")
        self.links = []
        if links is not None:
            for link in links:
                logma.info(f"Link: {link}")
                link = link.replace("}", "").replace("{", "").strip()
                if not link.startswith("http"):
                    continue
                DOWNLOAD_EXTENSIONS = [".zip", ".exe", ".pdf", ".jpg", ".png", ".mp4"]
                url_string = link  # If this is a QUrl object
                for ext in DOWNLOAD_EXTENSIONS:
                    if url_string.endswith(ext):
                        continue
                # try:
                # browser = PyfficeWebBrowser({"url": link}) Not sure how this should be organized at this level
                # due to the PyfficeWebBrowser-PyfficeWebPage-PyfficeURL hiearchy
                cfg = {"document": {"data": {"original_path": link}}}
                browser = PyfficeWebBrowser(cfg)
                browser.load_document()
                browser.set_url_active(link)
                # except Exception as e:
                #     logma.info(f"Link: {link}")
                #     continue
                logma.info(f"Link {browser.to_dict()}")
                logma.info(f"Active URL {browser.active_url.to_dict()}")
                if browser.active_url.domain is None:
                    continue
                logma.info(f"Active Link {browser.active_url} {browser.active_url.domain}")
                self.links.append(browser)
        return self

    def parse_node(self, node) -> Any:
        """
        Parse a single node and its children recursively.

        :param node: The XML element representing the node.
        :return: A dictionary representation of the node.
        """
        tab_id = uuid()
        name = node.attrib.get("name", None)
        if name is None or name == "":
            name = tab_id[len(tab_id) - 5 :]
        script = self.extract_text(node)
        script_dict = {}
        if script is not None:
            script_dict = script.to_dict()
            self.parse_links(script.full_text)
        self.extract_images(node)
        # self.codeboxes = self.extract_codeboxes(node)
        # self.tables = self.extract_tables(node)
        # is this needed?
        node_ = {
            "name": name,
            "custom_icon_id": node.attrib.get("custom_icon_id", ""),
            "readonly": node.attrib.get("readonly", ""),
            "tags": node.attrib.get("tags", ""),
            "creation_dttm": node.attrib.get("ts_creation", self.time.get_current_datetime_str()),
            "last_save_dttm": node.attrib.get("ts_lastsave", self.time.get_current_datetime_str()),
            "unique_id": node.attrib.get("unique_id", uuid()),
            "is_bold": node.attrib.get("is_bold", ""),
            "foreground": node.attrib.get("foreground", ""),
            "tabs": [
                {
                    "tags": node.attrib.get("tags", ""),
                    "readonly": node.attrib.get("readonly", ""),
                    "prog_lang": node.attrib.get("prog_lang", ""),
                    "name": name,
                    "unique_id": tab_id,
                    "rich_text": script_dict,
                    "type": "script",
                    "creation_dttm": node.attrib.get("ts_creation", self.time.store_now()),
                    "last_save_dttm": node.attrib.get("ts_lastsave", self.time.store_now()),
                }
            ],
        }
        logma.info(f"Links: {self.links}")
        if self.links is not None:
            for i, link in enumerate(self.links):
                logma.info(f"Link: {link.active_url} {link.active_url.domain}")
                name = link.active_url.domain[:30]
                if name is None or name == "":
                    name = tab_id[len(tab_id) - 5 :] + f"_{i}"
                node_["tabs"].append(
                    {
                        "tags": "",
                        "readonly": "",
                        "prog_lang": "",
                        "name": link.active_url.domain[:30],
                        "unique_id": link.did,
                        "type": "browser",
                        "rich_text": link.to_dict(),
                        "creation_timestamp": self.time.store_now(),
                        "last_save_timestamp": self.time.store_now(),
                    }
                )
        self.links = None
        if self.images is not None:
            for image in self.images:
                node_["tabs"].append(
                    {
                        "tags": "",
                        # "widget": "widgets.documents.media.images.NchantdOfficeImage",
                        "readonly": "",
                        "prog_lang": "",
                        "name": image.did[-8:],
                        "unique_id": image.did,
                        "type": "image",
                        "rich_text": image.to_dict(),
                        "creation_timestamp": self.time.store_now(),
                        "last_save_timestamp": self.time.store_now(),
                    }
                )
                logma.info(f"Image: {image.to_dict()}")
        if self.tables is not None:
            for table in self.tables:
                node_["tabs"].append(
                    {
                        "tags": "",
                        # "widget": "widgets.documents.workbooks.matricies.NchantdOfficeMatrix",
                        "readonly": "",
                        "prog_lang": "",
                        "name": table.name[:30],
                        "unique_id": table.did,
                        "type": "table",
                        "rich_text": table.to_dict(),
                        "creation_timestamp": self.time.store_now(),
                        "last_save_timestamp": self.time.store_now(),
                    }
                )
        if self.codeboxes is not None:
            for codebox in self.codeboxes:
                logma.info(f"Codebox: {codebox}")
                node_["tabs"].append(
                    {
                        "tags": "",
                        # "widget": "widgets.documents.media.scripts.NchantdOfficeScript",
                        "readonly": "",
                        "prog_lang": codebox.syntax,
                        "name": codebox.name[:30],
                        "unique_id": codebox.did,
                        "type": "script",
                        "rich_text": codebox.to_dict(),
                        "creation_timestamp": self.time.store_now(),
                        "last_save_timestamp": self.time.store_now(),
                    }
                )
        node_["nodes"] = [self.parse_node(child) for child in node.findall("node")]
        return node_

    def parse_tables(self, node) -> Self:
        """Parse tables.

        Args:
            node: Parameter.

        Returns:
            Self for chaining.
        """
        # extract tables
        tables = node.findall("table")
        for table in tables:
            cfg = {"document": {"content": table}}
            table_ = PyfficeMatrix(cfg)
            table_.load_document()
        return self

    def parse_text(self, node) -> Any:
        """Parse text.

        Args:
            node: Parameter.

        Returns:
            Self for chaining.
        """
        text = node.findall("rich_text")
        all_combined_text = []
        if len(text) > 0:
            for i, tag in enumerate(text):
                tag_text = tag.text
                if tag_text is None:
                    tag_text = ""
                tag_text = html.escape(tag_text).replace("\n", "<br>")
                all_combined_text.append(tag_text)
        combined_text = " ".join(filter(None, all_combined_text))
        return combined_text

    def to_dict(self) -> Self:
        """Convert this document to dict.

        Returns:
            Self for chaining.
        """
        doc = super().to_dict()
        for node in self.nodes:
            doc["data"]["documents"].append(node)
        return self._canonicalize(doc)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
