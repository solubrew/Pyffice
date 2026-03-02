"""
Pyffice ODT (Open Document Text) Handler
"""
from pathlib import Path
from typing import Optional, List
import zipfile
import xml.etree.ElementTree as ET


def create(odt_path: str, title: str, content: str) -> None:
    """Create ODT file."""
    with zipfile.ZipFile(odt_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mimetype", "application/vnd.oasis.opendocument.text", compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/manifest.xml", _manifest())
        zf.writestr("content.xml", _content(title, content))
        zf.writestr("styles.xml", _styles())


def read(odt_path: str) -> str:
    """Extract text from ODT."""
    with zipfile.ZipFile(odt_path, "r") as zf:
        content = zf.read("content.xml").decode("utf-8")
    root = ET.fromstring(content)
    ns = {'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}
    paragraphs = root.iterfind(".//text:p", ns)
    return "\n".join(p.text or "" for p in paragraphs)


def list_styles(odt_path: str) -> List[str]:
    """List styles in ODT."""
    with zipfile.ZipFile(odt_path, "r") as zf:
        styles = zf.read("styles.xml").decode("utf-8")
    root = ET.fromstring(styles)
    return [s.get("{http://purl.org/dc/elements/1.1/}title", "") for s in root.iter("style:style")]


def _manifest() -> str:
    return '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
</manifest:manifest>'''


def _content(title: str, content: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h text:outline-level="1">{title}</text:h>
      <text:p>{"</text:p><text:p>".join(content.split(chr(10)))}</text:p>
    </office:text>
  </office:body>
</office:document-content>'''


def _styles() -> str:
    return '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties style:tab-stop-distance="12.5pt"/>
    </style:default-style>
  </office:styles>
</office:document-styles>'''
