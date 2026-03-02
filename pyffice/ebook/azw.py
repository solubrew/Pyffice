"""
Pyffice AZW eBook Handler
"""

import subprocess
from pathlib import Path
from typing import Optional


def convert(epub_path: str, azw_path: str) -> None:
    """Convert EPUB to AZW3 format."""
    cmd = ["ebook-convert", epub_path, azw_path]
    subprocess.run(cmd, check=True, capture_output=True)


def convert_from_mobi(mobi_path: str, azw_path: str) -> None:
    """Convert MOBI to AZW3 format."""
    cmd = ["ebook-convert", mobi_path, azw_path]
    subprocess.run(cmd, check=True, capture_output=True)


def extract(azw_path: str, output_dir: str) -> None:
    """Extract AZW content."""
    try:
        cmd = ["kindleunpack", "-s", azw_path, output_dir]
        subprocess.run(cmd, check=True, capture_output=True)
    except:
        pass
