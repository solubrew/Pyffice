"""
Pyffice MOBI eBook Handler
"""

import subprocess
from pathlib import Path
from typing import Optional


def create(title: str, author: str, content: str, output: str, epub_template: Optional[str] = None) -> None:
    """Create MOBI file from content (requires ebook-convert)."""
    import tempfile
    import os
    
    if epub_template:
        cmd = ["ebook-convert", epub_template, output]
    else:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write(f"<html><head><title>{title}</title></head><body><pre>{content}</pre></body></html>")
            temp_html = f.name
        
        try:
            cmd = ["ebook-convert", temp_html, output]
            subprocess.run(cmd, check=True, capture_output=True)
        finally:
            if os.path.exists(temp_html):
                os.unlink(temp_html)


def convert(epub_path: str, mobi_path: str) -> None:
    """Convert EPUB to MOBI."""
    cmd = ["ebook-convert", epub_path, mobi_path]
    subprocess.run(cmd, check=True, capture_output=True)


def extract(mobi_path: str, output_dir: str) -> None:
    """Extract MOBI content (uses KindleUnpack if available."""
    try:
        cmd = ["kindleunpack", "-s", mobi_path, output_dir]
        subprocess.run(cmd, check=True, capture_output=True)
    except:
        pass
