"""RTF (Rich Text Format) support."""
from typing import Any, Optional
import io


def load(path: str) -> str:
    """Load RTF file contents."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def read(path: str) -> str:
    """Read RTF file contents."""
    return load(path)


def write(data: str, path: str) -> None:
    """Write data to RTF file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def dump(data: str, path: str) -> None:
    """Dump data to RTF file."""
    write(data, path)
