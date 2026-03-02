"""
Pyffice ZIP Container Handler
"""

import zipfile
from pathlib import Path
from typing import List, Optional


def compress(source: str, output: str, compression: int = zipfile.ZIP_DEFLATED) -> None:
    """Compress file or directory to ZIP."""
    source_path = Path(source)
    with zipfile.ZipFile(output, "w", compression=compression) as zf:
        if source_path.is_file():
            zf.write(source, source_path.name)
        else:
            for file in source_path.rglob("*"):
                if file.is_file():
                    zf.write(file, file.relative_to(source_path))


def extract(zip_path: str, output_dir: str) -> None:
    """Extract ZIP archive."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(output_dir)


def list_files(zip_path: str) -> List[str]:
    """List files in ZIP archive."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        return zf.namelist()


def add(zip_path: str, file_path: str, arcname: Optional[str] = None) -> None:
    """Add file to existing ZIP."""
    with zipfile.ZipFile(zip_path, "a") as zf:
        zf.write(file_path, arcname or Path(file_path).name)


def read(zip_path: str, member: str) -> bytes:
    """Read file from ZIP archive."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        return zf.read(member)
