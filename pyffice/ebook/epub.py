"""
Pyffice EPUB eBook Handler
"""

import zipfile
from pathlib import Path
from typing import List, Optional
import xml.etree.ElementTree as ET


def create(title: str, author: str, content: str, output: str) -> None:
    """Create EPUB file from content."""
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/container.xml", _container_xml())
        zf.writestr("OEBPS/content.opf", _opf(title, author))
        zf.writestr("OEBPS/toc.ncx", _toc_ncx(title))
        zf.writestr("OEBPS/Styles/style.css", "body { font-family: serif; margin: 1em; }")
        zf.writestr("OEBPS/Text/chapter1.xhtml", _xhtml(content))


def read(epub_path: str) -> str:
    """Extract text content from EPUB."""
    text_parts = []
    with zipfile.ZipFile(epub_path, "r") as zf:
        for name in zf.namelist():
            if name.endswith(".xhtml") or name.endswith(".html"):
                try:
                    content = zf.read(name).decode("utf-8")
                    text_parts.append(content)
                except:
                    pass
    return "\n".join(text_parts)


def list_chapters(epub_path: str) -> List[str]:
    """List chapters in EPUB."""
    chapters = []
    with zipfile.ZipFile(epub_path, "r") as zf:
        for name in zf.namelist():
            if "Text/" in name and (name.endswith(".xhtml") or name.endswith(".html")):
                chapters.append(name)
    return chapters


def _container_xml() -> str:
    return '''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''


def _opf(title: str, author: str) -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
  <metadata>
    <dc:title>{title}</dc:title>
    <dc:creator>{author}</dc:creator>
    <dc:language>en</dc:language>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="style" href="Styles/style.css" media-type="text/css"/>
    <item id="chapter1" href="Text/chapter1.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine toc="ncx">
    <itemref idref="chapter1"/>
  </spine>
</package>'''


def _toc_ncx(title: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="pyffice-generated"/>
  </head>
  <docTitle><text>{title}</text></docTitle>
  <navMap>
    <navPoint id="navpoint-1" playOrder="1">
      <navLabel><text>Chapter 1</text></navLabel>
      <content src="Text/chapter1.xhtml"/>
    </navPoint>
  </navMap>
</ncx>'''


def _xhtml(content: str) -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Chapter 1</title><link href="../Styles/style.css" type="text/css" rel="stylesheet"/></head>
<body><p>{"</p><p>".join(content.split("\\n"))}</p></body>
</html>'''
